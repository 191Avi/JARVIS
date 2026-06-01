import os
import importlib.util

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_module(name, rel_path):
    path = os.path.join(BASE_DIR, *rel_path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tools = load_module("jarvis_v3_tools", ["TOOL SYSTEM (REAL POWER CORE)", "tools.py"])
engine = load_module("jarvis_v3_engine", ["AI BRAIN (TOOL DECISION ENGINE)", "engine.py"])
wake = load_module("jarvis_v3_detection", ["WAKE WORD SYSTEM (IMPROVED VERSION)", "detection.py"])
memory = load_module("jarvis_v3_memory", ["MEMORY SYSTEM (NEW)", "memory.py"])

try:
    import pyttsx3
    voice_engine = pyttsx3.init()
    voice_engine.setProperty("rate", 175)
except Exception:
    voice_engine = None

try:
    import openai
except ImportError:
    openai = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_api_key_here")


def speak(text):
    print("JARVIS:", text)
    if voice_engine:
        try:
            voice_engine.say(text)
            voice_engine.runAndWait()
        except Exception:
            pass


def ask_ai(prompt):
    if openai is None:
        return "OpenAI is not installed. I can only run built-in commands."
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
        return "I don't have an AI key configured yet. Set OPENAI_API_KEY in your environment to enable AI mode."

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
        return f"AI error: {e}"


def jarvis():
    memory_data = memory.load_memory()
    user_name = memory_data.get("user_name", "Sir")

    speak(f"Jarvis system online. Good to see you, {user_name}.")
    print("\n  Say 'Hey Jarvis' followed by a command.")
    print("  Commands: time, open youtube, open google, open notepad,")
    print("            search wikipedia [topic], stop / exit\n")

    while True:
        print("Waiting for wake word ('Hey Jarvis')...")

        if not wake.listen_for_wake():
            continue

        speak("Yes?")
        command = wake.listen()

        if not command:
            speak("I didn't catch that. Try again.")
            continue

        if "stop" in command or "exit" in command or "shutdown" in command:
            speak("Shutting down. Goodbye.")
            break

        action = engine.decide_action(command)

        if "youtube" in action:
            speak("Opening YouTube")
            tools.open_youtube()

        elif "google" in action:
            speak("Opening Google")
            tools.open_google()

        elif "notepad" in action:
            speak("Opening Notepad")
            tools.open_notepad()

        elif "time" in action:
            speak(tools.get_time())

        elif "wikipedia" in action:
            speak("Searching Wikipedia")
            result = tools.search_wikipedia(command)
            speak(result)

        else:
            speak("Thinking...")
            response = ask_ai(command)
            speak(response)


if __name__ == "__main__":
    jarvis()
