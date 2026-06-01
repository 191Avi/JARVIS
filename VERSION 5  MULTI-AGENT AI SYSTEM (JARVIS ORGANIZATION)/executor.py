import webbrowser
import subprocess
import urllib.parse
import os

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False


def executor_agent(action):
    action_lower = action.lower()

    if "youtube" in action_lower:
        webbrowser.open("https://youtube.com")
        return "Opened YouTube"

    elif "google" in action_lower:
        webbrowser.open("https://google.com")
        return "Opened Google"

    elif "notepad" in action_lower:
        subprocess.Popen("notepad")
        return "Opened Notepad"

    elif action_lower.startswith("type ") or action_lower.startswith("write "):
        if not PYAUTOGUI_AVAILABLE:
            return "pyautogui not installed. Run: pip install pyautogui"
        text = action_lower.replace("type", "", 1).replace("write", "", 1).strip()
        pyautogui.write(text)
        return f"Typed: {text}"

    elif "search" in action_lower or "find" in action_lower:
        query = (
            action_lower
            .replace("search for", "")
            .replace("search", "")
            .replace("find", "")
            .strip()
        )
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
        webbrowser.open(url)
        return f"Searched for: {query}"

    elif "open " in action_lower:
        # Generic URL or site open
        site = action_lower.replace("open", "").strip()
        if not site.startswith("http"):
            site = "https://" + site
        webbrowser.open(site)
        return f"Opened: {site}"

    else:
        return f"No executor action matched for: {action}"
