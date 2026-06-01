import webbrowser
import subprocess
import os
import datetime
import wikipedia

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


def type_text(text):
    if not PYAUTOGUI_AVAILABLE:
        raise RuntimeError("pyautogui is not installed. Install it to use text typing features.")
    pyautogui.write(text)


def take_screenshot():
    if not PYAUTOGUI_AVAILABLE:
        raise RuntimeError("pyautogui is not installed. Install it to use screenshot features.")
    pyautogui.screenshot("screen.png")


def search_wikipedia(query):
    if not query:
        return "No query provided for Wikipedia search."
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        return "That topic is ambiguous. Please be more specific."
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"Wikipedia error: {e}"


def open_notepad():
    subprocess.Popen("notepad")


def get_time():
    return datetime.datetime.now().strftime("%H:%M")
