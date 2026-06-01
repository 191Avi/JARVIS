import speech_recognition as sr


def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
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
        print("Speech recognition service is unavailable.")
        return ""


def listen_for_wake():
    query = listen()
    return "hey jarvis" in query
