import os
import re
import subprocess
import webbrowser
import urllib.parse
import wikipedia
import requests

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False

from memory import load_memory, save_memory
from planner import planner

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False

def open_browser(url):
    webbrowser.open(url)

def type_text(text):
    if PYAUTOGUI_AVAILABLE:
        pyautogui.write(text)

def open_app(name):
    subprocess.Popen(name, shell=True)

def search_web(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    webbrowser.open(url)

def wikipedia_search(query):
    return wikipedia.summary(query, sentences=2)

def ai_fallback(query):
    print("No direct tool for this step. Falling back to a web search.")
    search_web(query)


def normalize_step(step):
    step = step.strip()
    step = re.sub(r'^\s*\d+[\).]?\s*', '', step)
    return step


def choose_tool(step):
    step = normalize_step(step).lower()

    if "youtube" in step:
        return ("open_browser", "https://youtube.com")

    elif "google" in step:
        return ("search_web", step)

    elif "wikipedia" in step:
        return ("wikipedia_search", step)

    elif "open notepad" in step:
        return ("open_app", "notepad")

    elif step.startswith("type ") or step.startswith("write "):
        return ("type_text", re.sub(r'^(type|write)\s+', '', step, count=1))

    elif "search" in step:
        return ("search_web", step)

    elif "open" in step and "browser" in step:
        return ("open_browser", "https://www.google.com")

    else:
        return ("ai_fallback", step)

def execute(tool, arg):
    if tool == "open_browser":
        open_browser(arg)

    elif tool == "search_web":
        search_web(arg)

    elif tool == "wikipedia_search":
        print(wikipedia_search(arg))

    elif tool == "open_app":
        open_app(arg)

    elif tool == "type_text":
        type_text(arg)

    elif tool == "ai_fallback":
        ai_fallback(arg)

    else:
        print(f"No tool found for: {tool}")


def _handle_invalid_plan(plan):
    print("Error: planner(task) did not return a string. Got:", type(plan))


def autonomous_agent(task):
    memory = load_memory()

    print("Planning task...")
    plan = planner(task)
    print(plan)

    if not isinstance(plan, str):
        _handle_invalid_plan(plan)
        steps = []
    else:
        steps = plan.split("\n")

    for step in steps:
        if step.strip() == "":
            continue

        print("Executing:", step)

        tool, arg = choose_tool(step)
        execute(tool, arg)

        memory.setdefault("history", []).append(step)
        save_memory(memory)

    print("Task completed")


# ===== VOICE WRAPPER (from Version 2) =====
def _text_input():
    try:
        return input("Type your task: ").strip().lstrip('﻿').lower()
    except EOFError:
        return ""


def listen():
    if not SR_AVAILABLE:
        return input("Type your task: ").strip().lower()

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.pause_threshold = 1
            audio = r.listen(source, timeout=6, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        return ""
    except (AttributeError, OSError):
        print("Microphone unavailable. Falling back to text input.")
        return _text_input()
    except Exception as e:
        print(f"Microphone error: {e}. Falling back to text input.")
        return _text_input()

    try:
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Speech recognition service unavailable. Falling back to text input.")
        return _text_input()


def listen_task():
    task = listen()
    return task


if __name__ == "__main__":
    print("JARVIS Autonomous Agent - speak your task (or type if mic unavailable)")
    task = listen_task()
    if task:
        autonomous_agent(task)
    else:
        print("No task received.")