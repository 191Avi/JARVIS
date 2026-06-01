import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

# ===== AI CONFIG =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# ===== VOICE ENGINE =====
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ===== LISTEN =====
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=6, phrase_time_limit=10)
    except (sr.WaitTimeoutError, AttributeError, OSError):
        print("Microphone unavailable or PyAudio is missing. Falling back to text input.")
        return input("Type your command: ").strip().lower()
    except Exception as e:
        print(f"Microphone error: {e}. Falling back to text input.")
        return input("Type your command: ").strip().lower()

    try:
        query = r.recognize_google(audio)
        print("You:", query)
        return query.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

# ===== AI RESPONSE (BRAIN) =====
def ask_ai(prompt):
    if not OPENAI_AVAILABLE:
        return "OpenAI package is not installed. I can only run built-in commands."
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
        return "I don't have an AI key configured yet. Add your OpenAI key in jarvis_v2.py or set OPENAI_API_KEY in the environment to enable AI mode."

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI error: {e}"

# ===== MAIN ASSISTANT =====
def jarvis():
    speak("Jarvis is now online")

    while True:
        query = listen()

        if "hey jarvis" in query:
            speak("Yes sir, I am listening")

            command = listen()

            # ===== BASIC COMMANDS =====
            if "time" in command:
                time = datetime.datetime.now().strftime("%H:%M")
                speak(f"The time is {time}")

            elif "open youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")

            elif "open google" in command:
                speak("Opening Google")
                webbrowser.open("https://google.com")

            elif "open notepad" in command:
                speak("Opening Notepad")
                os.system("notepad")

            elif "exit" in command or "stop" in command:
                speak("Shutting down")
                break

            else:
                # ===== AI BRAIN MODE =====
                speak("Thinking...")
                answer = ask_ai(command)
                speak(answer)

# RUN
jarvis()