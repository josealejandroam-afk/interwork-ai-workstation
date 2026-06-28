"""
ui.py — screen automation abstraction layer.

Callers import from here and never from pyautogui directly.
The implementation can be swapped (e.g. to pywinauto or WinAppDriver)
without changing any higher-level workflow code.

Priority for any given task:
  1. MCP / APIs          — handled by the caller, not here
  2. Playwright          — handled by the caller, not here
  3. Windows UI Automation (pywinauto) — element-based; use when available
  4. Mouse / keyboard    — this module
  5. Absolute coordinates — last resort; document the reason at the call site

Public API:
  Mouse:    click, double_click, right_click, scroll
  Keyboard: type_text, paste_text, hotkey, press, key_down, key_up
  Vision:   screenshot, find_image, wait_for_image, click_image
  Window:   bring_window_to_front, get_window_rect, screen_size
  Clip:     set_clipboard, get_clipboard
"""

import ctypes
import ctypes.wintypes
import time
from pathlib import Path
from typing import Optional, Tuple

import pyautogui

pyautogui.FAILSAFE = True   # move mouse to top-left corner to abort a run
pyautogui.PAUSE = 0.04      # small inter-action pause

SCREENSHOT_DIR = Path(r"C:\Users\Owner\AppData\Local\Temp\claude")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


# ── Clipboard (Windows API — no subprocess) ──────────────────────────────────

def _setup_k32_u32():
    k32, u32 = ctypes.windll.kernel32, ctypes.windll.user32
    # HGLOBAL is an opaque handle — use c_size_t so it stays pointer-sized on 64-bit
    k32.GlobalAlloc.restype  = ctypes.c_size_t
    k32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
    k32.GlobalLock.restype   = ctypes.c_void_p       # actual writable memory pointer
    k32.GlobalLock.argtypes  = [ctypes.c_size_t]
    k32.GlobalUnlock.argtypes = [ctypes.c_size_t]
    u32.GetClipboardData.restype  = ctypes.c_size_t  # returns HGLOBAL
    u32.GetClipboardData.argtypes = [ctypes.c_uint]
    u32.SetClipboardData.restype  = ctypes.c_size_t
    u32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_size_t]
    return k32, u32


def set_clipboard(text: str) -> None:
    """Write text to the Windows clipboard using the Win32 API (no subprocess)."""
    CF_UNICODETEXT = 13
    GMEM_MOVEABLE  = 0x0002
    encoded = text.encode("utf-16-le") + b"\x00\x00"
    k32, u32 = _setup_k32_u32()
    if not u32.OpenClipboard(0):
        raise OSError("OpenClipboard failed")
    try:
        u32.EmptyClipboard()
        h = k32.GlobalAlloc(GMEM_MOVEABLE, len(encoded))
        if not h:
            raise OSError("GlobalAlloc failed")
        p = k32.GlobalLock(h)
        if not p:
            raise OSError("GlobalLock returned NULL")
        ctypes.memmove(p, encoded, len(encoded))
        k32.GlobalUnlock(h)
        u32.SetClipboardData(CF_UNICODETEXT, h)
    finally:
        u32.CloseClipboard()


def get_clipboard() -> str:
    """Read text from the Windows clipboard."""
    CF_UNICODETEXT = 13
    k32, u32 = _setup_k32_u32()
    if not u32.OpenClipboard(0):
        raise OSError("OpenClipboard failed")
    try:
        h = u32.GetClipboardData(CF_UNICODETEXT)
        if not h:
            return ""
        p = k32.GlobalLock(h)
        if not p:
            return ""
        text = ctypes.wstring_at(p)
        k32.GlobalUnlock(h)
        return text
    finally:
        u32.CloseClipboard()


# ── Mouse ────────────────────────────────────────────────────────────────────

def click(x: int, y: int, delay: float = 0.12) -> None:
    pyautogui.moveTo(x, y, duration=0.08)
    time.sleep(delay)
    pyautogui.click()


def double_click(x: int, y: int) -> None:
    pyautogui.moveTo(x, y, duration=0.08)
    pyautogui.doubleClick()


def right_click(x: int, y: int) -> None:
    pyautogui.moveTo(x, y, duration=0.08)
    pyautogui.rightClick()


def scroll(x: int, y: int, clicks: int) -> None:
    """Scroll at (x, y). clicks > 0 = up, clicks < 0 = down."""
    pyautogui.moveTo(x, y, duration=0.08)
    pyautogui.scroll(clicks)


# ── Keyboard ─────────────────────────────────────────────────────────────────

def type_text(text: str, interval: float = 0.02) -> None:
    """Type short strings character-by-character. Use paste_text() for long or special-char strings."""
    pyautogui.typewrite(text, interval=interval)


def paste_text(text: str, delay: float = 0.15) -> None:
    """
    Set clipboard then Ctrl+V — handles any characters, no subprocess needed.
    Preferred over type_text() for anything more than a few words.
    """
    set_clipboard(text)
    time.sleep(delay)
    pyautogui.hotkey("ctrl", "v")


def hotkey(*keys: str) -> None:
    pyautogui.hotkey(*keys)


def press(key: str) -> None:
    pyautogui.press(key)


def key_down(key: str) -> None:
    pyautogui.keyDown(key)


def key_up(key: str) -> None:
    pyautogui.keyUp(key)


# ── Screenshot / vision ──────────────────────────────────────────────────────

def screenshot(path: Optional[str] = None) -> str:
    """Capture the full screen. Returns the saved file path."""
    if path is None:
        path = str(SCREENSHOT_DIR / f"screen_{int(time.time())}.png")
    img = pyautogui.screenshot()
    img.save(path)
    return path


def find_image(
    template: str,
    confidence: float = 0.9,
    region: Optional[Tuple[int, int, int, int]] = None,
) -> Optional[Tuple[int, int]]:
    """
    Locate a template image on screen. Returns (cx, cy) or None.
    Requires: pip install opencv-python
    template: path to a PNG/BMP crop of what to find.
    region: (left, top, width, height) to restrict search area.
    """
    try:
        loc = pyautogui.locateCenterOnScreen(template, confidence=confidence, region=region)
        return (int(loc.x), int(loc.y)) if loc else None
    except pyautogui.ImageNotFoundException:
        return None


def wait_for_image(
    template: str,
    timeout: float = 10.0,
    confidence: float = 0.9,
    poll: float = 0.5,
    region: Optional[Tuple[int, int, int, int]] = None,
) -> Optional[Tuple[int, int]]:
    """
    Poll until template image appears or timeout expires.
    Returns (cx, cy) or None.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        loc = find_image(template, confidence=confidence, region=region)
        if loc:
            return loc
        time.sleep(poll)
    return None


def click_image(
    template: str,
    confidence: float = 0.9,
    timeout: float = 5.0,
) -> bool:
    """Find a template image on screen and click its center. Returns True if clicked."""
    loc = wait_for_image(template, timeout=timeout, confidence=confidence)
    if loc:
        click(*loc)
        return True
    return False


# ── Window management ─────────────────────────────────────────────────────────

def _enum_windows(title_substring: str) -> list:
    """Return list of (hwnd, title) for visible windows matching substring."""
    results = []
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    def _cb(hwnd, _):
        if IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(512)
            GetWindowText(hwnd, buf, 512)
            if title_substring.lower() in buf.value.lower():
                results.append((hwnd, buf.value))
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
    ctypes.windll.user32.EnumWindows(WNDENUMPROC(_cb), 0)
    return results


def bring_window_to_front(title_substring: str) -> bool:
    """
    Bring a window to the foreground by partial title match.
    Returns True if a window was found and activated.
    """
    matches = _enum_windows(title_substring)
    if not matches:
        return False
    hwnd = matches[0][0]
    ctypes.windll.user32.ShowWindow(hwnd, 9)        # SW_RESTORE
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    return True


def get_window_rect(title_substring: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Return (x, y, width, height) of the first matching window, or None.
    """
    matches = _enum_windows(title_substring)
    if not matches:
        return None
    hwnd = matches[0][0]
    r = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(r))
    return (r.left, r.top, r.right - r.left, r.bottom - r.top)


def screen_size() -> Tuple[int, int]:
    return pyautogui.size()
