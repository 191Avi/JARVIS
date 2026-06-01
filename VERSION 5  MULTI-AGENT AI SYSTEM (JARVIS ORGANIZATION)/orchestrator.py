from memory import load_memory, save_memory
from manager import manager_agent
from planner import planner_agent
from research import research_agent
from executor import executor_agent
from critic import critic_agent

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False


# ===== VOICE WRAPPER (carried from Version 2) =====
def _text_input():
    try:
        return input("Type your task: ").strip().lstrip('﻿')
    except EOFError:
        return "exit"


def listen():
    if not SR_AVAILABLE:
        return input("Type your task: ").strip()

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
        print(f"Microphone error: {e}. Falling back to text input.")
        return _text_input()

    try:
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Speech recognition unavailable. Falling back to text input.")
        return _text_input()


def listen_task():
    task = listen()
    return task


# ===== MULTI-AGENT ORCHESTRATOR =====
def multi_agent_system(task):
    memory = load_memory()

    print("\n" + "=" * 50)
    print(f"  Task: {task}")
    print("=" * 50)

    print("\n[Manager Agent] Analyzing task...")
    agents = manager_agent(task)
    print(f"  Agents selected: {agents}")

    result = ""

    if "planner" in agents:
        print("\n[Planner Agent] Breaking down task...")
        plan = planner_agent(task)
        print(plan)
        result += "\nPLAN:\n" + plan

    if "research" in agents:
        print("\n[Research Agent] Gathering information...")
        research = research_agent(task)
        print(research)
        result += "\nRESEARCH:\n" + research

    if "executor" in agents:
        print("\n[Executor Agent] Performing actions...")
        exec_result = executor_agent(task)
        print(f"  {exec_result}")
        result += "\nEXECUTED: " + exec_result

    if "critic" in agents:
        print("\n[Critic Agent] Reviewing and improving output...")
        result = critic_agent(result)
        print(result)

    memory["tasks"].append(task)
    memory["agent_logs"].append({"task": task, "result": result, "agents": agents})
    save_memory(memory)

    print("\n" + "=" * 50)
    print("  Task completed.")
    print("=" * 50)
    return result


# ===== ENTRY POINT =====
if __name__ == "__main__":
    print("=" * 50)
    print("  JARVIS v5 - Multi-Agent AI System")
    print("  Agents: Manager | Planner | Research")
    print("          Executor | Critic | Memory")
    print("=" * 50)
    print("\nSpeak your task (or type if mic unavailable).")
    print("Type 'exit' to quit.\n")

    while True:
        task = listen_task()
        if not task:
            print("No task received. Try again.\n")
            continue
        if task.lower() in ("exit", "quit", "stop"):
            print("Shutting down JARVIS v5. Goodbye.")
            break
        multi_agent_system(task)
        print()
