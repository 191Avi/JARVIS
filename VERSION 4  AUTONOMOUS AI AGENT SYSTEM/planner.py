import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")


def _fallback_plan(user_task):
    return f"1. Search for information about {user_task}\n2. Complete the task"


def planner(user_task):
    if not OPENAI_AVAILABLE:
        print("OpenAI not installed. Using fallback plan.")
        return _fallback_plan(user_task)
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        print("OpenAI API key not configured. Using fallback plan.")
        return _fallback_plan(user_task)

    prompt = f"""
You are an AI planner.

Break this task into simple steps:

Task: {user_task}

Return steps as a numbered list only.
"""

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Planner AI error: {e}. Using fallback plan.")
        return _fallback_plan(user_task)
