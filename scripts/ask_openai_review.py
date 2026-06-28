"""
ask_openai_review.py — Send a review packet to OpenAI and save the response.

Reads:  C:/Users/1/.claude/feedback_loop/to_chatgpt.md
Writes: C:/Users/1/.claude/feedback_loop/from_chatgpt.md
        C:/Users/1/.claude/feedback_loop/action_plan.md

API key is read from the OPENAI_API_KEY environment variable.
The key is never printed, stored, or exposed in output.

Usage:
    python ask_openai_review.py
    python ask_openai_review.py --model gpt-4o
    python ask_openai_review.py --model o4-mini
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

FEEDBACK_DIR   = Path(r"C:\Users\1\.claude\feedback_loop")
INPUT_FILE     = FEEDBACK_DIR / "to_chatgpt.md"
RESPONSE_FILE  = FEEDBACK_DIR / "from_chatgpt.md"
PLAN_FILE      = FEEDBACK_DIR / "action_plan.md"
MASTER_CONTEXT = Path(r"C:\Users\1\.claude\projects\C--Users-1\memory\references\interwork_ai_ops_master_context.md")

# Patterns that must never appear in outbound content
_SECRET_PATTERNS = [
    r"eyJ[A-Za-z0-9_-]{20,}",          # JWT tokens
    r"sk-[A-Za-z0-9]{20,}",             # OpenAI keys
    r"service_role",                     # Supabase service role
    r"SUPABASE_SERVICE",
    r"SUPABASE_KEY",
    r"OPENAI_API_KEY\s*=\s*\S+",        # key assignment
    r"-----BEGIN",                       # PEM blocks
]

SYSTEM_INSTRUCTIONS = """\
You are an expert operations reviewer and AI systems architect for InterWork Office,
a commercial furniture and office relocation company. You are reviewing the current
state of an AI command center built in Claude Code that manages project operations.

Your role is to:
- Review what was built or found and evaluate whether it is correct and on-track
- Identify any risks, gaps, or misalignments with best practices
- Answer specific questions clearly and practically
- Propose a prioritized action plan

Format your response in two clearly labeled sections:

## Review & Analysis
Your full analysis and answers here.

## Action Plan
A numbered list of concrete next steps, in priority order.
Each item must be in this format:
  N. [PRIORITY: high/medium/low] Action description — reason

Do not include steps that require information you don't have.
Do not recommend steps that are already done or in progress unless you see a gap.
Keep action items specific enough that an AI agent can act on them without ambiguity.

Permission boundary (must be respected):
- Supabase writes, status updates, and schema changes require Alejandro approval
- Sending emails or Teams messages requires explicit approval
- Never set vendor_confirmed, client_confirmed, or access_confirmed automatically
- All reads are allowed; memory writes to local files are allowed
"""


def load_review_context() -> str:
    """Extract the ## Review Context Summary section from the master context file."""
    if not MASTER_CONTEXT.exists():
        return ""
    text = MASTER_CONTEXT.read_text(encoding="utf-8")
    marker = "## Review Context Summary"
    start = text.find(marker)
    if start == -1:
        return ""
    # Find the next ## heading after the summary
    end = text.find("\n## ", start + len(marker))
    section = text[start:end].strip() if end != -1 else text[start:].strip()
    return section


def scrub_secrets(text: str) -> str:
    """Raise if any secret patterns are detected in outbound text."""
    for pattern in _SECRET_PATTERNS:
        if re.search(pattern, text):
            raise ValueError(
                f"SECRET DETECTED in outbound content (pattern: {pattern[:30]}). "
                "Aborting. Remove secrets before sending."
            )
    return text


def build_packet(content: str) -> str:
    """Prepend the Review Context Summary to the review packet content."""
    context = load_review_context()
    if context:
        packet = f"{context}\n\n---\n\n## Review Packet\n\n{content}"
        print(f"Context: {len(context)} chars prepended from master context file.")
    else:
        print("Warning: master context file not found or has no Review Context Summary.")
        packet = content
    return scrub_secrets(packet)


def get_client(model: str):
    """Return an OpenAI client. Raises if OPENAI_API_KEY is not set."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    key = os.environ.get("OPENAI_API_KEY")
    if not key and sys.platform == "win32":
        # Try reading from Windows User environment (set via System Properties)
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as reg:
                key, _ = winreg.QueryValueEx(reg, "OPENAI_API_KEY")
            os.environ["OPENAI_API_KEY"] = key  # inject for openai client
        except (FileNotFoundError, OSError):
            pass
    if not key:
        print("ERROR: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    return OpenAI()  # reads OPENAI_API_KEY from env automatically


def call_responses_api(client, model: str, content: str) -> str:
    """Call the OpenAI Responses API and return the text output."""
    try:
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=content,
        )
        return response.output_text
    except AttributeError:
        # Responses API not available in this SDK version — fall back to Chat Completions
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user",   "content": content},
            ],
        )
        return response.choices[0].message.content


def extract_action_plan(full_response: str) -> str:
    """Pull out the Action Plan section from the response text."""
    marker = "## Action Plan"
    idx = full_response.find(marker)
    if idx == -1:
        # Try alternate headings
        for alt in ["# Action Plan", "**Action Plan**", "Action Plan\n"]:
            idx = full_response.find(alt)
            if idx != -1:
                break
    if idx == -1:
        return "(No structured action plan found in response.)\n\nFull response saved to from_chatgpt.md."
    return full_response[idx:].strip()


def main():
    parser = argparse.ArgumentParser(description="Send a review packet to OpenAI and save the response.")
    parser.add_argument("--model", default="gpt-4o", help="Model to use (default: gpt-4o)")
    args = parser.parse_args()

    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}", file=sys.stderr)
        print("Create the file with content to review, then retry.", file=sys.stderr)
        sys.exit(1)

    content = INPUT_FILE.read_text(encoding="utf-8").strip()
    if not content:
        print(f"ERROR: Input file is empty: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    print(f"Model:  {args.model}")
    print(f"Input:  {len(content)} chars from {INPUT_FILE.name}")

    try:
        packet = build_packet(content)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Packet: {len(packet)} chars total (content + context)")
    print("Sending to OpenAI...")

    client = get_client(args.model)
    try:
        full_response = call_responses_api(client, args.model, packet)
    except Exception as e:
        err = str(e)
        if "insufficient_quota" in err or "429" in err:
            print("ERROR: OpenAI quota exceeded.", file=sys.stderr)
            print("Add billing credits at: https://platform.openai.com/account/billing", file=sys.stderr)
        elif "401" in err or "authentication" in err.lower():
            print("ERROR: API key rejected. Check OPENAI_API_KEY.", file=sys.stderr)
        elif "model" in err.lower() and "not found" in err.lower():
            print(f"ERROR: Model '{args.model}' not available on this account.", file=sys.stderr)
            print("Try: --model gpt-4o-mini", file=sys.stderr)
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = f"<!-- Generated {now} | Model: {args.model} -->\n\n"

    RESPONSE_FILE.write_text(header + full_response, encoding="utf-8")
    print(f"Response saved → {RESPONSE_FILE}")

    action_plan = extract_action_plan(full_response)
    plan_content = f"# Action Plan\n_Generated {now} | Model: {args.model}_\n\n{action_plan}\n"
    PLAN_FILE.write_text(plan_content, encoding="utf-8")
    print(f"Action plan saved → {PLAN_FILE}")

    # Print action plan to stdout for immediate review
    print("\n" + "="*60)
    print(action_plan)
    print("="*60)
    print("\nDone. Review action_plan.md and approve steps before executing.")


if __name__ == "__main__":
    main()
