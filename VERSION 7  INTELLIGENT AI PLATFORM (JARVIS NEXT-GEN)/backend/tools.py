import webbrowser
import subprocess
import urllib.parse
import datetime
import os
import json

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

try:
    import requests as _requests
    REQUESTS_AVAILABLE = True
except ImportError:
    _requests = None
    REQUESTS_AVAILABLE = False


# ===== TOOL FUNCTIONS =====

def open_youtube(**kwargs):
    webbrowser.open("https://youtube.com")
    return "Opened YouTube."


def search_google(query: str = "", **kwargs):
    q = urllib.parse.quote_plus(query) if query else ""
    webbrowser.open(f"https://google.com/search?q={q}" if q else "https://google.com")
    return f"Searched Google for: {query}" if query else "Opened Google."


def open_notepad(**kwargs):
    subprocess.Popen("notepad")
    return "Opened Notepad."


def search_wikipedia(query: str = "", **kwargs):
    if not WIKI_AVAILABLE:
        return "wikipedia package not installed. Run: pip install wikipedia"
    if not query:
        return "No query provided for Wikipedia."
    try:
        return wikipedia.summary(query, sentences=3)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ambiguous topic. Did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"Wikipedia error: {e}"


def take_screenshot(**kwargs):
    if not PYAUTOGUI_AVAILABLE:
        return "pyautogui not installed. Run: pip install pyautogui"
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved as {filename}."


def get_weather(city: str = "", **kwargs):
    if not city:
        return "Please provide a city name."
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        # Fallback: open browser weather search
        webbrowser.open(f"https://wttr.in/{urllib.parse.quote_plus(city)}")
        return f"Opened weather for {city} in browser (no OPENWEATHER_API_KEY set)."
    if not REQUESTS_AVAILABLE:
        return "requests package not installed."
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = _requests.get(url, timeout=10)
        data = res.json()
        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'Unknown error')}"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        return f"Weather in {city}: {desc}, {temp}°C, humidity {humidity}%."
    except Exception as e:
        return f"Weather fetch error: {e}"


def set_reminder(message: str = "", minutes: int = 5, **kwargs):
    if not message:
        return "Please provide a reminder message."
    remind_at = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    # Save to a reminders file
    reminder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reminders.json")
    try:
        reminders = []
        if os.path.exists(reminder_path):
            with open(reminder_path) as f:
                reminders = json.load(f)
        reminders.append({
            "message": message,
            "remind_at": remind_at.isoformat(),
            "created": datetime.datetime.now().isoformat()
        })
        with open(reminder_path, "w") as f:
            json.dump(reminders, f, indent=2)
        return f"Reminder set: '{message}' at {remind_at.strftime('%H:%M:%S')} ({minutes} min from now)."
    except Exception as e:
        return f"Could not save reminder: {e}"


def open_file(filename: str = "", **kwargs):
    if not filename:
        return "Please provide a filename or path to open."
    # Try common locations
    search_dirs = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
    ]
    # If absolute path given
    if os.path.isabs(filename) and os.path.exists(filename):
        os.startfile(filename)
        return f"Opened: {filename}"
    # Search in common dirs
    for d in search_dirs:
        full = os.path.join(d, filename)
        if os.path.exists(full):
            os.startfile(full)
            return f"Opened: {full}"
    return f"File '{filename}' not found in Desktop, Documents, or Downloads."


def get_time(**kwargs):
    now = datetime.datetime.now()
    return f"Current time: {now.strftime('%I:%M %p')}, {now.strftime('%A, %B %d, %Y')}."


# ===== OPENAI FUNCTION SCHEMAS =====

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "open_youtube",
            "description": "Opens YouTube in the browser.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_google",
            "description": "Searches Google for a query or opens Google.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_notepad",
            "description": "Opens Notepad text editor.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Searches Wikipedia and returns a summary.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Topic to search on Wikipedia"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Takes a screenshot of the current screen.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. 'London' or 'New York'"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "Sets a reminder for a number of minutes from now.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "What to be reminded about"},
                    "minutes": {"type": "integer", "description": "Minutes from now (default 5)", "default": 5}
                },
                "required": ["message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_file",
            "description": "Opens a file by name. Searches Desktop, Documents, and Downloads.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Filename or full path to open"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Returns the current time and date.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
]


# ===== DISPATCH =====

TOOL_MAP = {
    "open_youtube":     open_youtube,
    "search_google":    search_google,
    "open_notepad":     open_notepad,
    "search_wikipedia": search_wikipedia,
    "take_screenshot":  take_screenshot,
    "get_weather":      get_weather,
    "set_reminder":     set_reminder,
    "open_file":        open_file,
    "get_time":         get_time,
}


def execute_tool(name: str, arguments: dict) -> str:
    fn = TOOL_MAP.get(name)
    if not fn:
        return f"Unknown tool: '{name}'. Available: {', '.join(TOOL_MAP)}"
    try:
        return fn(**arguments)
    except Exception as e:
        return f"Tool '{name}' error: {e}"


def list_tools() -> list:
    return [
        {
            "name": s["function"]["name"],
            "description": s["function"]["description"]
        }
        for s in TOOL_SCHEMAS
    ]
