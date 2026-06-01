import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")


def planner_agent(task):
    if not OPENAI_AVAILABLE or not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        print("Planner: no API key — using generic fallback plan.")
        return f"1. Search for information about {task}\n2. Complete the task"

    prompt = f"""
Break this task into clear, numbered steps:

Task: {task}

Return numbered steps only. No extra text.
"""

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Planner AI error: {e}. Using fallback plan.")
        return f"1. Search for information about {task}\n2. Complete the task"
