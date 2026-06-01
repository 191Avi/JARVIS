import webbrowser
import os
import subprocess
import datetime
import urllib.parse
import wikipedia
import requests

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False


def open_youtube():
    webbrowser.open("https://youtube.com")


def open_google():
    webbrowser.open("https://google.com")


def open_notepad():
    subprocess.Popen("notepad")


def get_time():
    return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"


def get_date():
    return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"


def search_web(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    webbrowser.open(url)


def search_wikipedia(query):
    if not query:
        return "No query provided."
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        return "That topic is ambiguous. Please be more specific."
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"Wikipedia error: {e}"


def take_screenshot():
    if not PYAUTOGUI_AVAILABLE:
        return "pyautogui is not installed. Run: pip install pyautogui"
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved as {filename}"


def type_text(text):
    if not PYAUTOGUI_AVAILABLE:
        return "pyautogui is not installed. Run: pip install pyautogui"
    pyautogui.write(text)
    return f"Typed: {text}"
