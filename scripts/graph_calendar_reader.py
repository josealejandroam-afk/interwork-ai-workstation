#!/usr/bin/env python3
"""
Microsoft Graph delegated read-only calendar reader.
Uses the same local token cache as graph_mail_reader.py.

Rules (hard-coded):
  - Never creates, updates, or deletes calendar events
  - Never prints access or refresh tokens
  - Stops if signed-in account != TARGET_ACCOUNT
  - Output stays in gitignored local_sources/graph_calendar/
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import msal
except ImportError:
    print("ERROR: msal not installed. Run: uv pip install msal")
    sys.exit(1)

CLIENT_ID = "de8bc8b5-d9f9-48b1-a8ad-b748da725064"
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["User.Read", "Calendars.Read"]
TARGET_ACCOUNT = "alejandroa@interworkoffice.com"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO_ROOT / "local_sources" / "graph_cache"
CACHE_FILE = CACHE_DIR / "msal_cache.bin"
CAL_DIR = REPO_ROOT / "local_sources" / "graph_calendar"


def _load_cache():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text(encoding="utf-8"))
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(cache.serialize(), encoding="utf-8")


def authenticate():
    cache = _load_cache()
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if result and "access_token" in result:
        _save_cache(cache)
        return result["access_token"]

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "message" not in flow:
        print(f"ERROR: {flow.get('error_description', flow)}")
        return None

    print()
    print("=" * 62)
    print("  SIGN-IN REQUIRED")
    print("=" * 62)
    print(flow["message"])
    print("=" * 62)
    print("Waiting for sign-in...")

    result = app.acquire_token_by_device_flow(flow)
    _save_cache(cache)

    if "access_token" not in result:
        print(f"AUTH FAILED: {result.get('error_description', result.get('error'))}")
        return None

    return result["access_token"]


def verify_account(token):
    data = _graph_get(token, "/me", {"$select": "mail,userPrincipalName,displayName"})
    if not data:
        print("ERROR: Cannot verify account.")
        return False
    actual = (data.get("mail") or data.get("userPrincipalName") or "").lower().strip()
    print(f"Signed in as: {data.get('displayName', '?')} <{actual}>")
    if actual != TARGET_ACCOUNT.lower():
        print(f"WRONG ACCOUNT: expected {TARGET_ACCOUNT}. Stopping.")
        return False
    print("Account verified.")
    return True


def _graph_get(token, endpoint, params=None):
    url = GRAPH_BASE + endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Graph API error {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}")
        return None
    except Exception as ex:
        print(f"Request error: {ex}")
        return None


def read_calendar(token, days=14, dry_run=False):
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)
    start_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"\nReading calendar: {start_str[:10]} to {end_str[:10]} ({days} days)")

    params = {
        "startdatetime": start_str,
        "enddatetime": end_str,
        "$top": "50",
        "$select": "subject,start,end,organizer,location,attendees,bodyPreview,isAllDay",
        "$orderby": "start/dateTime",
    }

    data = _graph_get(token, "/me/calendarview", params)
    if data is None:
        return

    events = data.get("value", [])
    print(f"Found {len(events)} event(s).")

    if not events:
        print("No events in this window.")
        return

    out_dir = CAL_DIR
    summaries = []

    for i, ev in enumerate(events, 1):
        subject = ev.get("subject") or "(no subject)"
        start_obj = ev.get("start", {})
        end_obj = ev.get("end", {})
        start_dt = start_obj.get("dateTime", "?")[:16].replace("T", " ")
        end_dt = end_obj.get("dateTime", "?")[:16].replace("T", " ")
        organizer = ev.get("organizer", {}).get("emailAddress", {}).get("name", "?")
        location = ev.get("location", {}).get("displayName", "")
        is_all_day = ev.get("isAllDay", False)
        preview = (ev.get("bodyPreview") or "").strip()[:200]

        attendees = [
            a.get("emailAddress", {}).get("name", "?")
            for a in (ev.get("attendees") or [])[:8]
        ]

        summary_lines = [
            f"[{i}] {subject}",
            f"    Start: {start_dt}{'  (all day)' if is_all_day else ''}",
            f"    End:   {end_dt}",
            f"    Organizer: {organizer}",
        ]
        if location:
            summary_lines.append(f"    Location: {location}")
        if attendees:
            summary_lines.append(f"    Attendees: {', '.join(attendees)}")
        if preview:
            summary_lines.append(f"    Preview: {preview[:150]}")

        block = "\n".join(summary_lines)
        summaries.append(block)
        print(block)
        print()

    if dry_run:
        print(f"[DRY RUN - would save {len(events)} events to local_sources/graph_calendar/]")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    today = now.strftime("%Y-%m-%d")
    out_file = out_dir / f"calendar_{today}_{days}days.txt"
    out_file.write_text("\n\n".join(summaries) + "\n", encoding="utf-8")
    print(f"Saved: {out_file.relative_to(REPO_ROOT)}")
    print("No events were created, updated, or deleted.")


def main():
    parser = argparse.ArgumentParser(description="Microsoft Graph read-only calendar reader")
    parser.add_argument("--days", type=int, default=14,
                        help="Number of days ahead to read (default: 14)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print events but save nothing")
    args = parser.parse_args()

    print("Microsoft Graph Calendar Reader — read-only")
    print(f"Target account: {TARGET_ACCOUNT}")
    print(f"Window: next {args.days} days")
    if args.dry_run:
        print("[DRY RUN]")
    print()

    token = authenticate()
    if not token:
        sys.exit(1)

    if not verify_account(token):
        sys.exit(1)

    read_calendar(token, days=args.days, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
