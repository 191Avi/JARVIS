import webbrowser
import subprocess
import urllib.parse
import datetime
import os

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False

try:
    import wikipedia
    WIKI_AVAILABLE = True
except ImportError:
    wikipedia = None
    WIKI_AVAILABLE = False


# ===== TOOL FUNCTIONS =====
def _youtube():
    webbrowser.open("https://youtube.com")
    return "Opened YouTube."

def _google(query=""):
    q = urllib.parse.quote_plus(query) if query else ""
    webbrowser.open(f"https://google.com/search?q={q}" if q else "https://google.com")
    return f"Searched Google for: {query}" if query else "Opened Google."

def _notepad():
    subprocess.Popen("notepad")
    return "Opened Notepad."

def _wikipedia(query=""):
    if not WIKI_AVAILABLE:
        return "wikipedia package not installed."
    if not query:
        return "No query provided for Wikipedia."
    try:
        return wikipedia.summary(query, sentences=3)
    except wikipedia.exceptions.DisambiguationError:
        return "Ambiguous topic. Please be more specific."
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"Wikipedia error: {e}"

def _screenshot():
    if not PYAUTOGUI_AVAILABLE:
        return "pyautogui not installed. Run: pip install pyautogui"
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved as {filename}."


# ===== TOOL REGISTRY =====
TOOLS = {
    "youtube":    {"fn": _youtube,    "description": "Opens YouTube in browser"},
    "google":     {"fn": _google,     "description": "Searches Google (optional: query)"},
    "notepad":    {"fn": _notepad,    "description": "Opens Notepad"},
    "wikipedia":  {"fn": _wikipedia,  "description": "Searches Wikipedia (requires: query)"},
    "screenshot": {"fn": _screenshot, "description": "Takes a screenshot"},
}


def execute_tool(name: str, arg: str = "") -> str:
    tool = TOOLS.get(name.lower())
    if not tool:
        return f"Unknown tool: '{name}'. Available: {', '.join(TOOLS)}"
    try:
        return tool["fn"](arg) if arg else tool["fn"]()
    except TypeError:
        return tool["fn"]()


def list_tools() -> list:
    return [{"name": k, "description": v["description"]} for k, v in TOOLS.items()]
