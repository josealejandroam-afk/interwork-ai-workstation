"""
parse_completion_email.py — Extract completion evidence from email text.

Accepts pasted or file-based email content (Outlook forward, export, or raw text).
Matches to a project, proposes Supabase field updates, never writes anything.

Usage:
    python parse_completion_email.py --file path/to/email.txt
    python parse_completion_email.py --paste          (then paste + Ctrl-Z)
    python parse_completion_email.py --text "email body text"

Output: structured JSON with match result and proposed updates.
"""

import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# ── Completion signal patterns ────────────────────────────────────────────────

SUBJECT_PATTERNS = [
    r"work\s+completion",
    r"\bWCR\b",
    r"work\s+complete",
    r"job\s+complete",
    r"move\s+complete",
    r"project\s+complete",
    r"decom\s+complete",
    r"install\s+complete",
    r"walkthrough\s+complete",
    r"punch\s+list\s+complete",
    r"field\s+report",
    r"site\s+report",
    r"completion\s+report",
    r"wrap.?up",
    r"all\s+done",
    r"signed\s+off",
]

BODY_COMPLETION_PHRASES = [
    r"work\s+(has\s+been\s+)?completed",
    r"(job|project|move|install)\s+(is\s+)?complete",
    r"all\s+items?\s+(have\s+been\s+)?(moved|delivered|installed|completed)",
    r"site\s+(is\s+)?clear",
    r"punch\s+list\s+(is\s+)?(clear|done|complete)",
    r"signed\s+off",
    r"client\s+satisfied",
    r"no\s+further\s+action\s+required",
    r"wrap(ped)?\s+up",
]

PROJECT_NUMBER_PATTERN = re.compile(r"\b(7\d{3})\b")  # 7000–7999

DATE_PATTERNS = [
    r"(?:completed?|finished?|done)\s+(?:on\s+)?(\w+ \d{1,2},? \d{4})",
    r"(\d{1,2}/\d{1,2}/\d{4})",
    r"(\d{4}-\d{2}-\d{2})",
    r"(\w+ \d{1,2},? \d{4})",
]


# ── Parsing helpers ────────────────────────────────────────────────────────────

def detect_subject(text: str) -> tuple[str | None, bool]:
    """Return (subject_line, is_completion_subject)."""
    for line in text.splitlines()[:20]:
        if line.lower().startswith("subject:"):
            subject = line[8:].strip()
            is_completion = any(
                re.search(p, subject, re.IGNORECASE) for p in SUBJECT_PATTERNS
            )
            return subject, is_completion
    return None, False


def detect_completion_in_body(text: str) -> list[str]:
    """Return list of matching phrases found in body."""
    matches = []
    for pattern in BODY_COMPLETION_PHRASES:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            matches.append(m.group(0).strip())
    return matches


def extract_project_numbers(text: str) -> list[str]:
    """Return unique 7xxx project numbers found in text."""
    return sorted(set(PROJECT_NUMBER_PATTERN.findall(text)))


def extract_date_hint(text: str) -> str | None:
    """Try to find a completion date in the text."""
    for pattern in DATE_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            raw = m.group(1)
            # Sanity check: avoid matching very old or future dates
            for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%B %d, %Y", "%B %d %Y"):
                try:
                    dt = datetime.strptime(raw.replace(",", ""), fmt.replace(",", ""))
                    if 2024 <= dt.year <= 2027:
                        return dt.strftime("%Y-%m-%d")
                except ValueError:
                    continue
    return None


def extract_sender(text: str) -> str | None:
    for line in text.splitlines()[:20]:
        if line.lower().startswith("from:"):
            return line[5:].strip()
    return None


def score_confidence(subject_match: bool, body_matches: list, project_numbers: list) -> str:
    if subject_match and project_numbers:
        return "high"
    if subject_match or (body_matches and project_numbers):
        return "medium"
    if body_matches or project_numbers:
        return "low"
    return "none"


# ── Source-type detection ──────────────────────────────────────────────────────

def detect_source_type(text: str, subject: str | None) -> str:
    if subject and re.search(r"work\s+completion|WCR", subject or "", re.IGNORECASE):
        return "wc_report"
    if re.search(r"fastfield|fast\s+field", text, re.IGNORECASE):
        return "fastfield"
    if re.search(r"from:|to:|subject:|date:", text[:500], re.IGNORECASE):
        return "email"
    return "manual_note"


# ── Proposed field updates ─────────────────────────────────────────────────────

def build_proposals(source_type: str, confidence: str, completion_date: str | None) -> dict:
    """Return field update proposals based on evidence type and confidence."""
    proposals = {}

    if confidence == "none":
        return proposals

    if source_type == "fastfield":
        proposals["fastfield_submitted"] = True
    elif source_type == "wc_report":
        proposals["completion_report_sent"] = True

    if completion_date and confidence in ("high", "medium"):
        proposals["actual_end_at"] = completion_date

    # Only propose status=completed at high confidence with a completion date
    if confidence == "high" and completion_date:
        proposals["_status_candidate"] = "completed"

    return proposals


# ── Main ───────────────────────────────────────────────────────────────────────

def parse_email(text: str) -> dict:
    subject, subject_match = detect_subject(text)
    body_matches = detect_completion_in_body(text)
    project_numbers = extract_project_numbers(text)
    completion_date = extract_date_hint(text)
    sender = extract_sender(text)
    source_type = detect_source_type(text, subject)
    confidence = score_confidence(subject_match, body_matches, project_numbers)

    proposals = build_proposals(source_type, confidence, completion_date)

    # Excerpt: first 300 chars of meaningful content
    lines = [l for l in text.splitlines() if l.strip()]
    excerpt = " | ".join(lines[:5])[:300]

    return {
        "parsed": {
            "subject": subject,
            "sender": sender,
            "subject_is_completion": subject_match,
            "body_matches": body_matches,
            "project_numbers_found": project_numbers,
            "completion_date_hint": completion_date,
            "source_type": source_type,
            "confidence": confidence,
            "excerpt": excerpt,
        },
        "proposed_updates": proposals,
        "next_step": (
            "Match project number in Supabase, then review proposals before applying."
            if project_numbers
            else "No project number found — manual match required."
        ),
        "requires_approval": True,
    }


def main():
    parser = argparse.ArgumentParser(description="Parse completion evidence from email text.")
    parser.add_argument("--file", "-f", help="Path to email text file")
    parser.add_argument("--paste", action="store_true", help="Paste email text from stdin")
    parser.add_argument("--text", "-t", help="Email text inline (for testing)")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    elif args.text:
        text = args.text
    elif args.paste or not sys.stdin.isatty():
        print("Paste email text (Ctrl+Z on Windows / Ctrl+D on Unix to finish):")
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    text = text.strip()
    if not text:
        print("ERROR: No text provided.", file=sys.stderr)
        sys.exit(1)

    result = parse_email(text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
