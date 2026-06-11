import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import json
import os

# Optional: OpenAI for AI brain
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Optional: pyautogui for screenshot
PYAUTOGUI_AVAILABLE = False
pyautogui = None
MIC_AVAILABLE = True
pending_command = None

def ensure_pyautogui():
    global pyautogui, PYAUTOGUI_AVAILABLE
    if PYAUTOGUI_AVAILABLE:
        return
    try:
        import pyautogui as _pyautogui
        pyautogui = _pyautogui
        PYAUTOGUI_AVAILABLE = True
    except ImportError:
        PYAUTOGUI_AVAILABLE = False

# ===== CONFIG =====
# Paste your OpenAI API key here to enable AI brain (optional)
OPENAI_API_KEY = "your_api_key_here"
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

# ===== VOICE ENGINE =====
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# ===== MEMORY =====
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

# ===== LISTEN =====
def listen():
    global MIC_AVAILABLE
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.pause_threshold = 1
            audio = r.listen(source, timeout=6, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        return ""
    except (AttributeError, OSError) as e:
        MIC_AVAILABLE = False
        print("PyAudio microphone not available. Trying sounddevice fallback.")
        return listen_with_sounddevice(r)
    except Exception as e:
        MIC_AVAILABLE = False
        print(f"Microphone error: {e}. Trying sounddevice fallback.")
        return listen_with_sounddevice(r)

    try:
        query = r.recognize_google(audio)
        print(f"You: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

def listen_with_sounddevice(recognizer):
    try:
        import sounddevice as sd
        import numpy as np
        sample_rate = 16000
        duration = 5
        print(f"Recording audio for {duration} seconds...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        audio_data = recording.tobytes()
        audio = sr.AudioData(audio_data, sample_rate, 2)
        query = recognizer.recognize_google(audio)
        print(f"You: {query}")
        return query.lower()
    except Exception as e:
        print(f"Sounddevice recording failed: {e}")
        print("Falling back to text input.")
        return input("Type your command: ").strip().lower()


# ===== WAKE WORD =====
def listen_for_wake():
    global pending_command
    pending_command = None
    query = listen()
    if not query:
        return False
    if "hey jarvis" in query:
        return True
    if not MIC_AVAILABLE:
        pending_command = query
        return True
    return False

# ===== AI BRAIN (optional - requires OpenAI key) =====
def ask_ai(prompt):
    if not OPENAI_AVAILABLE:
        return "OpenAI package is not installed. I can only run built-in commands."
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
        return "I don't have an AI key configured yet. Add your OpenAI key in jarvis_final.py to enable AI mode."

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a smart AI assistant. Be concise and helpful."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI error: {str(e)}"

# ===== TOOLS =====
def get_time():
    return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"

def get_date():
    return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"

def open_youtube():
    webbrowser.open("https://youtube.com")

def open_google():
    webbrowser.open("https://google.com")

def open_notepad():
    os.system("notepad")

def search_wikipedia(command):
    term = command.replace("search wikipedia", "").replace("wikipedia", "").strip()
    if not term:
        return "What should I search on Wikipedia?"
    try:
        return wikipedia.summary(term, sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        return "That topic is ambiguous. Please be more specific."
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{term}'."
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

def take_screenshot():
    if not PYAUTOGUI_AVAILABLE:
        return "pyautogui is not installed. Run: pip install pyautogui"
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(os.path.dirname(__file__), filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved as {filename}"

# ===== MAIN LOOP =====
def jarvis():
    global pending_command
    memory = load_memory()
    user_name = memory.get("user_name", "Sir")

    speak(f"Jarvis online. Good to see you, {user_name}.")
    print("\n  Say 'Hey Jarvis' followed by a command.")
    print("  If text fallback is active, you can also type commands directly.")
    print("  Commands: time, date, open youtube, open google, open notepad,")
    print("            search wikipedia [topic], screenshot,")
    print("            remember [something], what do you remember,")
    print("            stop / exit / shutdown\n")

    while True:
        print("Waiting for wake word ('Hey Jarvis')...")

        if not listen_for_wake():
            continue

        speak("Yes?")
        if pending_command:
            command = pending_command
            pending_command = None
        else:
            command = listen()

        if not command:
            speak("I didn't catch that. Try again.")
            continue

        # ===== COMMANDS =====
        if "time" in command:
            speak(get_time())

        elif "date" in command:
            speak(get_date())

        elif "open youtube" in command:
            speak("Opening YouTube")
            open_youtube()

        elif "open google" in command:
            speak("Opening Google")
            open_google()

        elif "open notepad" in command:
            speak("Opening Notepad")
            open_notepad()

        elif "wikipedia" in command:
            speak("Searching Wikipedia")
            result = search_wikipedia(command)
            speak(result)

        elif "screenshot" in command:
            speak("Taking a screenshot")
            result = take_screenshot()
            speak(result)

        elif "remember" in command:
            fact = command.replace("remember", "").strip()
            if fact:
                memory.setdefault("tasks", []).append(fact)
                save_memory(memory)
                speak(f"Got it. I'll remember that.")
            else:
                speak("Remember what exactly?")

        elif "what do you remember" in command or "what have you remembered" in command:
            tasks = memory.get("tasks", [])
            if tasks:
                speak(f"I remember: {'. '.join(tasks)}")
            else:
                speak("I don't have anything stored in memory yet.")

        elif "stop" in command or "exit" in command or "shutdown" in command:
            speak("Shutting down. Goodbye.")
            break

        else:
            speak("Thinking...")
            answer = ask_ai(command)
            speak(answer)

if __name__ == "__main__":
    jarvis()
