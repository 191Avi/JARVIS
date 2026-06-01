import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
    except sr.WaitTimeoutError:
        return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

def run_jarvis():
    speak("Hello, I am your assistant")

    while True:
        query = take_command()

        if "time" in query:
            time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {time}")

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "search wikipedia" in query:
            speak("Searching Wikipedia")
            search_term = query.replace("search wikipedia", "").strip()
            try:
                result = wikipedia.summary(search_term, sentences=2)
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("That topic is ambiguous. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("No Wikipedia page found for that topic.")

        elif "stop" in query or "exit" in query:
            speak("Goodbye")
            break

        elif query != "":
            speak("I am not trained for that yet")

if __name__ == "__main__":
    run_jarvis()