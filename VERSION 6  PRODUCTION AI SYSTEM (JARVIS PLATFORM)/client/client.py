import requests

try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    TTS_AVAILABLE = True
except Exception:
    engine = None
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False

BACKEND_URL = "http://localhost:8000"


# ===== SPEAK =====
def speak(text):
    print(f"JARVIS: {text}")
    if TTS_AVAILABLE:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass


# ===== LISTEN =====
def _text_input(prompt="You: "):
    try:
        return input(prompt).strip()
    except EOFError:
        return "exit"


def listen():
    if not SR_AVAILABLE:
        return _text_input()

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
        print(f"Mic error: {e}. Falling back to text input.")
        return _text_input()

    try:
        query = r.recognize_google(audio)
        print(f"You: {query}")
        return query
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Speech service unavailable. Falling back to text input.")
        return _text_input()


# ===== API CALLS =====
def send_to_jarvis(prompt: str) -> dict:
    try:
        res = requests.post(
            f"{BACKEND_URL}/chat",
            json={"prompt": prompt},
            timeout=30
        )
        res.raise_for_status()
        return res.json()
    except requests.exceptions.ConnectionError:
        return {"response": "Cannot connect to JARVIS backend. Is it running? Run run_backend.bat first.", "tool_used": None}
    except requests.exceptions.Timeout:
        return {"response": "Request timed out.", "tool_used": None}
    except Exception as e:
        return {"response": f"Error: {e}", "tool_used": None}


def show_history():
    try:
        res = requests.get(f"{BACKEND_URL}/history?limit=5", timeout=10)
        data = res.json()
        print("\n--- Last 5 interactions ---")
        for item in reversed(data["history"]):
            print(f"[{item['time']}] You: {item['input']}")
            print(f"           JARVIS: {item['response'][:80]}...")
            if item["tool"]:
                print(f"           Tool used: {item['tool']}")
        print("---------------------------\n")
    except Exception as e:
        print(f"Could not fetch history: {e}")


# ===== MAIN LOOP =====
def main():
    print("=" * 50)
    print("  JARVIS v6 — Production AI Client")
    print("  Backend: http://localhost:8000")
    print("=" * 50)
    print("Commands: 'history' = show past chats, 'exit' = quit\n")

    # Check backend health
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=5).json()
        speak(f"JARVIS v{health['version']} online. Ready.")
    except Exception:
        print("WARNING: Backend not reachable. Start run_backend.bat first.\n")

    while True:
        print("Waiting for wake word 'Hey Jarvis' or type your command...")
        query = listen()

        if not query:
            continue

        if query.lower() in ("exit", "quit", "stop", "shutdown"):
            speak("Shutting down. Goodbye.")
            break

        if query.lower() == "history":
            show_history()
            continue

        # Strip wake word if present
        query = query.lower().replace("hey jarvis", "").strip()
        if not query:
            speak("Yes? What can I do for you?")
            query = listen()
            if not query:
                continue

        speak("On it...")
        result = send_to_jarvis(query)

        response = result.get("response", "No response.")
        tool = result.get("tool_used")

        if tool:
            speak(f"Done. Used the {tool} tool.")
        else:
            speak(response)


if __name__ == "__main__":
    main()
