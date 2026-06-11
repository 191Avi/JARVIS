import requests
import json
import sys
import io

try:
    import pyttsx3
    _tts = pyttsx3.init()
    _tts.setProperty("rate", 175)
    TTS_AVAILABLE = True
except Exception:
    _tts = None
    TTS_AVAILABLE = False

try:
    import sounddevice as sd
    import scipy.io.wavfile as wavfile
    import numpy as np
    SD_AVAILABLE = True
except ImportError:
    sd = None
    SD_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False

VOICE_AVAILABLE = SD_AVAILABLE and SR_AVAILABLE

BACKEND_URL = "http://localhost:8000"
WAKE_WORDS   = ["hey jarvis", "jarvis", "ok jarvis"]
SAMPLE_RATE  = 16000
RECORD_SECS  = 6   # max seconds to listen


# ===== SPEAK =====
def speak(text: str):
    print(f"\nJARVIS: {text}")
    if TTS_AVAILABLE and _tts:
        try:
            _tts.say(text)
            _tts.runAndWait()
        except Exception:
            pass


# ===== LISTEN =====
def _text_input(prompt: str = "You: ") -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        return "exit"


def listen() -> str:
    if not VOICE_AVAILABLE:
        return _text_input()

    try:
        print("Listening...", end=" ", flush=True)
        audio_data = sd.rec(
            int(RECORD_SECS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )
        sd.wait()  # wait until recording is done

        # Convert numpy array to WAV bytes
        buf = io.BytesIO()
        wavfile.write(buf, SAMPLE_RATE, audio_data)
        buf.seek(0)

        # Feed into SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(buf) as source:
            audio = recognizer.record(source)

        query = recognizer.recognize_google(audio)
        print(f"You: {query}")
        return query

    except sr.UnknownValueError:
        print("(couldn't understand)")
        return ""
    except sr.RequestError:
        print("Speech service unavailable — switching to text input.")
        return _text_input()
    except Exception as e:
        print(f"Mic error: {e} — switching to text input.")
        return _text_input()


def strip_wake_word(text: str) -> str:
    lower = text.lower().strip()
    for ww in WAKE_WORDS:
        if lower.startswith(ww):
            return text[len(ww):].strip(" ,.")
    return text


# ===== STREAMING CHAT =====
def send_streaming(prompt: str) -> tuple[str, str | None]:
    full_reply = ""
    tool_used  = None

    try:
        with requests.post(
            f"{BACKEND_URL}/chat/stream",
            json={"prompt": prompt},
            stream=True,
            timeout=60
        ) as res:
            res.raise_for_status()
            print("\nJARVIS: ", end="", flush=True)

            for line in res.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if not line.startswith("data: "):
                    continue
                data = json.loads(line[6:])

                if data["type"] == "tool":
                    tool_used = data["tool"]
                    args_str  = ", ".join(f"{k}={v}" for k, v in data.get("args", {}).items())
                    print(f"[Tool: {tool_used}({args_str})] ", end="", flush=True)

                elif data["type"] == "token":
                    tok = data["content"]
                    print(tok, end="", flush=True)
                    full_reply += tok

                elif data["type"] == "done":
                    print()
                    break

                elif data["type"] == "error":
                    print(f"\n[Error: {data['message']}]")
                    break

    except requests.exceptions.ConnectionError:
        msg = "Cannot connect to JARVIS backend. Start run_backend.bat first."
        print(f"\nJARVIS: {msg}")
        return msg, None
    except requests.exceptions.Timeout:
        msg = "Request timed out."
        print(f"\nJARVIS: {msg}")
        return msg, None
    except Exception as e:
        msg = f"Error: {e}"
        print(f"\nJARVIS: {msg}")
        return msg, None

    return full_reply, tool_used


# ===== HISTORY / STATS =====
def show_history():
    try:
        res = requests.get(f"{BACKEND_URL}/history?limit=5", timeout=10)
        data = res.json()
        print("\n─── Last 5 interactions ───────────────────")
        for item in reversed(data["history"]):
            print(f"[{item['time']}]")
            print(f"  You:    {item['input']}")
            snippet = (item['response'] or '')[:100]
            print(f"  JARVIS: {snippet}{'...' if len(item['response'] or '') > 100 else ''}")
            if item["tool"]:
                print(f"  Tool:   {item['tool']}")
        print("────────────────────────────────────────────\n")
    except Exception as e:
        print(f"Could not fetch history: {e}")


def show_stats():
    try:
        res = requests.get(f"{BACKEND_URL}/stats", timeout=10)
        data = res.json()
        print(f"\n  Total interactions: {data['total_interactions']}")
        if data["tool_usage"]:
            print("  Tool usage:", ", ".join(f"{k}×{v}" for k, v in data["tool_usage"].items()))
        print()
    except Exception as e:
        print(f"Could not fetch stats: {e}")


# ===== MAIN LOOP =====
def main():
    print("=" * 52)
    print("  JARVIS v7 — Intelligent AI Platform")
    print("  Backend: http://localhost:8000")
    print("  Web UI:  http://localhost:8000/ui")
    print("=" * 52)

    if VOICE_AVAILABLE:
        print(f"  Voice mode: ON  (mic ready, {RECORD_SECS}s per command)")
    else:
        print("  Voice mode: OFF (text input fallback)")

    print("Commands: history | stats | exit\n")

    # Health check
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=5).json()
        speak(f"JARVIS version {health['version']} online. How can I help?")
    except Exception:
        print("WARNING: Backend not reachable. Start run_backend.bat first.\n")

    while True:
        query = listen()

        if not query:
            continue

        cmd = query.lower().strip()

        if cmd in ("exit", "quit", "stop", "shutdown"):
            speak("Shutting down. Goodbye.")
            sys.exit(0)

        if cmd == "history":
            show_history()
            continue

        if cmd == "stats":
            show_stats()
            continue

        query = strip_wake_word(query)
        if not query:
            speak("Yes? What can I do for you?")
            continue

        response, tool = send_streaming(query)

        if TTS_AVAILABLE and response and len(response) < 300:
            speak(response)


if __name__ == "__main__":
    main()
