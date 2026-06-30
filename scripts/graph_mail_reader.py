#!/usr/bin/env python3
"""
Microsoft Graph delegated read-only mail reader.
Device code flow — user signs in once, token cached locally.

Rules (hard-coded, not overridable by args):
  - Never sends email
  - Never deletes, moves, archives, flags, or modifies email
  - Never downloads attachments
  - Never prints access or refresh tokens
  - Stops immediately if signed-in account != TARGET_ACCOUNT
  - Raw full bodies are never saved (bodyPreview only, max 255 chars)
  - All output stays in gitignored local_sources/
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

try:
    import msal
except ImportError:
    print("ERROR: msal not installed. Run: uv pip install msal")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# PLACEHOLDER: Replace with a proper app client_id registered in your Azure AD tenant by IT.
# Using Microsoft Graph Explorer client_id as placeholder only — it will fail with
# AADSTS1001010 if the tenant hasn't consented to it. That failure is expected and
# produces a clear IT escalation message. Do not substitute other first-party client IDs.
# Preferred path: use scripts/graph_powershell_readonly_test.ps1 (Graph PowerShell module).
CLIENT_ID = "de8bc8b5-d9f9-48b1-a8ad-b748da725064"
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["User.Read", "Mail.Read"]
TARGET_ACCOUNT = "alejandroa@interworkoffice.com"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO_ROOT / "local_sources" / "graph_cache"
CACHE_FILE = CACHE_DIR / "msal_cache.bin"
MAIL_DIR = REPO_ROOT / "local_sources" / "graph_mail"


# ---------------------------------------------------------------------------
# Token cache (local file, gitignored)
# ---------------------------------------------------------------------------
def _load_cache():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text(encoding="utf-8"))
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(cache.serialize(), encoding="utf-8")


def _get_app(cache):
    return msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache,
    )


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
def authenticate():
    """Return access token via cache or device code flow. Never prints token."""
    cache = _load_cache()
    app = _get_app(cache)

    # Try silent (cached) first
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if result and "access_token" in result:
        _save_cache(cache)
        return result["access_token"]

    # Device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "message" not in flow:
        error = flow.get("error_description", flow.get("error", str(flow)))
        print(f"ERROR: Could not start device flow.\n{error}")
        _handle_auth_error(error)
        return None

    print()
    print("=" * 62)
    print("  SIGN-IN REQUIRED")
    print("=" * 62)
    print(flow["message"])
    print("=" * 62)
    print("Waiting for sign-in (up to 15 minutes)...")

    result = app.acquire_token_by_device_flow(flow)
    _save_cache(cache)

    if "access_token" not in result:
        error = result.get("error_description", result.get("error", str(result)))
        print(f"\nAUTH FAILED: {error}")
        _handle_auth_error(error)
        return None

    return result["access_token"]


def _handle_auth_error(error_text):
    error_text = str(error_text)
    if "AADSTS65001" in error_text:
        print("\nTENANT POLICY: Admin consent is required for this application.")
        print("This means your IT admin has restricted which apps users can authorize.")
        print("Next step: escalate to VMX/IT — request a registered Graph app or the")
        print("Claude Microsoft 365 connector. Draft is at docs/drafts/m365_access_request.md")
    elif "AADSTS700016" in error_text:
        print("\nAPP NOT FOUND in tenant. The public client ID may be restricted.")
        print("Next step: escalate to IT for a tenant-registered app registration.")
    elif "AADSTS50076" in error_text or "AADSTS50079" in error_text:
        print("\nMFA REQUIRED. Complete multi-factor authentication in the browser.")
    elif "AADSTS50158" in error_text:
        print("\nCONDITIONAL ACCESS POLICY is blocking this sign-in.")
        print("Your tenant may restrict device code flow. Escalate to IT.")
    elif "declined" in error_text.lower() or "cancel" in error_text.lower():
        print("\nSign-in was cancelled.")


# ---------------------------------------------------------------------------
# Account verification
# ---------------------------------------------------------------------------
def verify_account(token):
    """Verify the signed-in account matches TARGET_ACCOUNT. Hard stop if not."""
    data = _graph_get(token, "/me", {"$select": "mail,userPrincipalName,displayName"})
    if not data:
        print("ERROR: Could not verify signed-in account.")
        return False

    actual = (data.get("mail") or data.get("userPrincipalName") or "").lower().strip()
    display = data.get("displayName", "?")

    print(f"Signed in as: {display} <{actual}>")

    if actual != TARGET_ACCOUNT.lower():
        print(f"WRONG ACCOUNT: Expected {TARGET_ACCOUNT}, got {actual}.")
        print("Stopping. Sign out and re-run, or delete the cache file:")
        print(f"  {CACHE_FILE}")
        return False

    print("Account verified.")
    return True


# ---------------------------------------------------------------------------
# Graph HTTP helper
# ---------------------------------------------------------------------------
def _graph_get(token, endpoint, params=None):
    """GET from Microsoft Graph. Never prints the token value."""
    url = GRAPH_BASE + endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "ConsistencyLevel": "eventual",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Graph API error {e.code}: {body[:300]}")
        return None
    except Exception as ex:
        print(f"Request error: {ex}")
        return None


# ---------------------------------------------------------------------------
# Mail search
# ---------------------------------------------------------------------------
def search_mail(token, query, max_results=10, dry_run=False, project_number=None):
    print(f"\nSearching mail for: '{query}' (max {max_results})")

    # $search requires the value in double-quotes for Graph KQL
    clean_query = query.strip('"')
    params = {
        "$search": f'"{clean_query}"',
        "$top": str(min(max_results, 50)),
        "$select": "subject,from,receivedDateTime,toRecipients,"
                   "hasAttachments,webLink,bodyPreview",
    }

    data = _graph_get(token, "/me/messages", params)
    if data is None:
        return

    messages = data.get("value", [])
    total = data.get("@odata.count", len(messages))
    print(f"Found {len(messages)} message(s) (API reported ~{total}).")

    if not messages:
        print("No results. Try a different query.")
        return

    tag = f"project_{project_number}" if project_number else "search"
    out_dir = MAIL_DIR / tag

    for i, msg in enumerate(messages, 1):
        subject = msg.get("subject") or "(no subject)"
        from_obj = msg.get("from", {}).get("emailAddress", {})
        sender_name = from_obj.get("name", "?")
        sender_addr = from_obj.get("address", "?")
        received = msg.get("receivedDateTime", "?")
        has_attach = msg.get("hasAttachments", False)
        web_link = msg.get("webLink", "")
        preview = (msg.get("bodyPreview") or "").strip()

        to_names = [
            r.get("emailAddress", {}).get("name", "?")
            for r in (msg.get("toRecipients") or [])[:5]
        ]

        summary_lines = [
            "---",
            f"project: {project_number or 'search'}",
            f"source: microsoft_graph_mail",
            f"query: {query}",
            "---",
            "",
            f"Subject: {subject}",
            f"From: {sender_name} <{sender_addr}>",
            f"Received: {received}",
            f"To: {', '.join(to_names) if to_names else '?'}",
            f"Has Attachments: {has_attach}",
            f"Web Link: {web_link}",
            "",
            "--- Body Preview (sanitized, max 255 chars) ---",
            preview,
            "",
        ]
        summary = "\n".join(summary_lines)

        print(f"\n  [{i}] {subject}")
        print(f"       From: {sender_name} | {received[:10] if len(received) >= 10 else received}")
        print(f"       Preview: {preview[:120]}{'...' if len(preview) > 120 else ''}")

        if dry_run:
            print(f"       [DRY RUN - would save to: local_sources/graph_mail/{tag}/]")
        else:
            out_dir.mkdir(parents=True, exist_ok=True)
            safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in subject)[:50]
            fpath = out_dir / f"{i:02d}_{safe}.txt"
            fpath.write_text(summary, encoding="utf-8")
            print(f"       Saved: {fpath.relative_to(REPO_ROOT)}")

    print()
    if dry_run:
        print(f"DRY RUN complete. {len(messages)} message(s) would be saved to local_sources/graph_mail/{tag}/")
    else:
        print(f"Saved {len(messages)} sanitized summary file(s) to local_sources/graph_mail/{tag}/")
    print("No emails were modified, moved, or deleted.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Microsoft Graph read-only mail reader")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview results only; save nothing to disk")
    parser.add_argument("--max-results", type=int, default=10,
                        help="Maximum emails to return (default: 10)")
    parser.add_argument("--project-number", type=str, default=None,
                        help="Project number tag for output folder (e.g. 7510)")
    parser.add_argument("--query", type=str, default=None,
                        help='Search query, e.g. "7510 OR Pear OR Frank Barrett"')
    args = parser.parse_args()

    print("Microsoft Graph Mail Reader — read-only")
    print(f"Target account: {TARGET_ACCOUNT}")
    print(f"Scopes: {', '.join(SCOPES)}")
    if args.dry_run:
        print("[DRY RUN — nothing will be written to disk]")
    print()

    query = args.query
    if not query and args.project_number:
        query = args.project_number
    if not query:
        query = "InterWork"

    token = authenticate()
    if not token:
        sys.exit(1)

    if not verify_account(token):
        sys.exit(1)

    search_mail(
        token,
        query=query,
        max_results=args.max_results,
        dry_run=args.dry_run,
        project_number=args.project_number,
    )


if __name__ == "__main__":
    main()
