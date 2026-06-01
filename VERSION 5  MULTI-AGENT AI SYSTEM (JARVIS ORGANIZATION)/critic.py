import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")


def critic_agent(result):
    if not result or not result.strip():
        return result

    if not OPENAI_AVAILABLE or not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        print("Critic: no API key — returning result as-is.")
        return result

    prompt = f"""
You are a quality-review AI.

Review this output and return an improved, cleaner version:

{result}

Return the improved version only. No meta-commentary.
"""

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Critic AI error: {e}. Returning original result.")
        return result
