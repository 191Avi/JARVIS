import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

# Set your real OpenAI key here or via environment variable:
# Windows: set OPENAI_API_KEY=sk-...
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")


def _local_decide(task):
    task_lower = task.lower()
    agents = []
    if any(w in task_lower for w in ["plan", "how", "steps", "create", "build", "make", "write"]):
        agents.append("planner")
    if any(w in task_lower for w in ["research", "find", "search", "what is", "info", "look up", "about"]):
        agents.append("research")
    if any(w in task_lower for w in ["open", "type", "launch", "run", "go to", "visit"]):
        agents.append("executor")
    if any(w in task_lower for w in ["check", "review", "improve", "fix", "validate", "critique"]):
        agents.append("critic")
    if not agents:
        agents = ["planner", "executor"]
    return ", ".join(agents)


def manager_agent(task):
    if not OPENAI_AVAILABLE or not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        print("Manager: no API key — using local decision logic.")
        return _local_decide(task)

    prompt = f"""
You are a Manager AI.

Your job is to decide how to handle this task:

Task: {task}

Choose which agents are needed from this list only:
- planner
- research
- executor
- critic

Return ONLY a comma-separated list like:
planner, research
"""

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"Manager AI error: {e}. Using local decision.")
        return _local_decide(task)
