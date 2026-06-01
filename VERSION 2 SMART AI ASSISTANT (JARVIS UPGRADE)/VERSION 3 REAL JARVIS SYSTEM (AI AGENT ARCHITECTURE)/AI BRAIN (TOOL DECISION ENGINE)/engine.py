import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
if OPENAI_AVAILABLE:
    openai.api_key = OPENAI_API_KEY


def decide_action(user_input):
    if not OPENAI_AVAILABLE:
        print("OpenAI is not installed. Falling back to local decision mode.")
        return _local_decide_action(user_input)
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        print("OpenAI API key is not configured. Falling back to local decision mode.")
        return _local_decide_action(user_input)

    prompt = f"""
You are Jarvis AI.

User request: {user_input}

Decide the action:
Return only one of:
- open_youtube
- open_google
- open_notepad
- get_time
- wikipedia_search
- general_answer
"""

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Engine AI error: {e}")
        return _local_decide_action(user_input)


def _local_decide_action(user_input):
    text = user_input.lower()
    if "youtube" in text:
        return "open_youtube"
    if "google" in text:
        return "open_google"
    if "notepad" in text:
        return "open_notepad"
    if "time" in text or "what time" in text:
        return "get_time"
    if "wikipedia" in text or "search" in text:
        return "wikipedia_search"
    return "general_answer"
