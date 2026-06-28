"""
send_to_chatgpt.py — send a message to an existing ChatGPT conversation.

Targets a specific conversation URL saved in chatgpt_target_url.txt.
Never opens a new blank chat. Always reuses an existing tab.

Profile stored at: C:/Users/Owner/.playwright-profile/
Target URL file:   D:/ai-workstation/scripts/chatgpt_target_url.txt

Usage:
    python send_to_chatgpt.py --file path/to/message.txt
    python send_to_chatgpt.py "inline message"
    python send_to_chatgpt.py  (reads from stdin)

To set the target conversation:
    Copy the ChatGPT conversation URL and save it to chatgpt_target_url.txt
"""

import sys
import time
from pathlib import Path

PROFILE_DIR    = Path(r"C:\Users\Owner\.playwright-profile")
TARGET_URL_FILE = Path(r"D:\ai-workstation\scripts\chatgpt_target_url.txt")
SCREENSHOT_DIR  = Path(r"C:\Users\Owner\AppData\Local\Temp\claude")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

INPUT_SELECTOR       = "#prompt-textarea"
SEND_BUTTON_SELECTOR = "[data-testid='send-button']"


def load_target_url() -> str | None:
    """Read the saved conversation URL, if any."""
    if TARGET_URL_FILE.exists():
        url = TARGET_URL_FILE.read_text(encoding="utf-8").strip()
        return url if url else None
    return None


def find_target_page(pages, target_url: str | None):
    """
    Find the best matching open page:
    1. Exact URL match with the saved conversation URL
    2. URL starts-with match (handles query params / anchors)
    3. Any chatgpt.com tab (last resort, only if no target URL saved)
    Returns (page, match_type) or (None, None).
    """
    if target_url:
        # Exact or prefix match
        for p in pages:
            if p.url == target_url or p.url.startswith(target_url.rstrip("/")):
                return p, "exact"
        # Partial path match (e.g. same conversation ID even if params differ)
        target_path = target_url.split("chatgpt.com")[-1].rstrip("/")
        for p in pages:
            if "chatgpt.com" in p.url and target_path in p.url:
                return p, "path"
        return None, None   # target URL set but not found — do not fall back to wrong chat
    else:
        # No target URL saved — find any ChatGPT tab
        for p in pages:
            if "chatgpt.com" in p.url:
                return p, "any"
        return None, None


def send_via_playwright(message: str) -> bool:
    """
    Find the target ChatGPT conversation tab and send the message.
    Never opens a new blank chat. Returns True on success.
    """
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

    target_url = load_target_url()
    if target_url:
        print(f"Target URL: {target_url}")
    else:
        print("No target URL configured. Will use any open ChatGPT tab.")
        print(f"To set one: save the conversation URL to {TARGET_URL_FILE}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True,
        )

        page, match_type = find_target_page(browser.pages, target_url)

        if page is None:
            if target_url:
                print(
                    "\nChatGPT target conversation not found.\n"
                    "The saved URL is not open in any browser tab.\n"
                    f"  Saved URL: {target_url}\n"
                    "Open that conversation in Chrome, then retry.\n"
                    "Or update the target URL by editing:\n"
                    f"  {TARGET_URL_FILE}"
                )
            else:
                print(
                    "\nNo ChatGPT tab found and no target URL configured.\n"
                    "Open the desired ChatGPT conversation in Chrome, then save its URL:\n"
                    f"  {TARGET_URL_FILE}"
                )
            browser.close()
            return None   # None = intentional stop; do not trigger ui.py fallback

        print(f"Found ChatGPT tab ({match_type} match): {page.url}")
        page.bring_to_front()

        # Scroll to bottom so the input is visible
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.4)

        try:
            page.wait_for_selector(INPUT_SELECTOR, timeout=15_000)
        except PWTimeout:
            print("Timed out waiting for ChatGPT input — may need to log in.")
            shot = str(SCREENSHOT_DIR / "chatgpt_timeout.png")
            page.screenshot(path=shot)
            print(f"Screenshot: {shot}")
            browser.close()
            return False

        input_box = page.locator(INPUT_SELECTOR)
        input_box.click()
        input_box.fill(message)
        time.sleep(0.3)

        try:
            page.click(SEND_BUTTON_SELECTOR, timeout=3_000)
        except PWTimeout:
            page.keyboard.press("Enter")

        time.sleep(1.0)

        shot = str(SCREENSHOT_DIR / f"chatgpt_sent_{int(time.time())}.png")
        page.screenshot(path=shot)
        print(f"Sent. Screenshot: {shot}")

        # Wait for response to start streaming
        time.sleep(5)
        shot2 = str(SCREENSHOT_DIR / f"chatgpt_response_{int(time.time())}.png")
        page.screenshot(path=shot2)
        print(f"Response screenshot: {shot2}")

        browser.close()
        return True


def send_via_ui_fallback(message: str) -> bool:
    """
    Last-resort fallback using ui.py + window-relative coordinates.
    Only reached if Playwright itself fails (not if tab not found — that's a hard stop).
    """
    sys.path.insert(0, str(Path(__file__).parent))
    from ui import get_window_rect, bring_window_to_front, click, paste_text, press, screenshot

    rect = (
        get_window_rect("ChatGPT")
        or get_window_rect("chrome")
        or get_window_rect("Google Chrome")
    )
    if not rect:
        print("No browser window found for fallback.")
        return False

    x, y, w, h = rect
    input_x = x + w // 2
    input_y = y + h - 80

    bring_window_to_front("ChatGPT") or bring_window_to_front("chrome")
    time.sleep(0.4)
    click(input_x, input_y)
    time.sleep(0.4)
    paste_text(message)
    time.sleep(0.3)
    press("enter")

    time.sleep(1)
    shot = screenshot(str(SCREENSHOT_DIR / f"chatgpt_fallback_{int(time.time())}.png"))
    print(f"Fallback sent. Screenshot: {shot}")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Send a message to a ChatGPT conversation.")
    parser.add_argument("message", nargs="*", help="Message text (inline)")
    parser.add_argument("--file", "-f", help="Path to a text file containing the message")
    args = parser.parse_args()

    if args.file:
        message = Path(args.file).read_text(encoding="utf-8").strip()
    elif args.message:
        message = " ".join(args.message)
    else:
        print("Paste message (Ctrl+Z / Ctrl+D to finish):")
        message = sys.stdin.read().strip()

    if not message:
        print("No message provided.")
        sys.exit(1)

    print(f"Sending ({len(message)} chars) via Playwright...")
    result = send_via_playwright(message)
    if result is None:
        # Intentional stop: tab not found. Error already printed. Do not fall back.
        sys.exit(1)
    if not result:
        # Technical failure: try ui.py fallback
        print("Playwright error — trying ui.py fallback...")
        result = send_via_ui_fallback(message)

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
