# Jarvis V3 Modular Assistant Skill Prompt

This prompt is for AI agents working on the Version 3 modular JARVIS architecture in:
`VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)/VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)`.

## Primary modules
- `MAIN JARVIS LOOP (FULL SYSTEM)/jarvis_v3.py`: orchestrates wake-word listening, captures voice input, decides the action, and executes tools.
- `AI BRAIN (TOOL DECISION ENGINE)/engine.py`: maps user input to exactly one action string.
- `MEMORY SYSTEM (NEW)/memory.py`: loads and saves assistant memory in `memory.json`.
- `TOOL SYSTEM (REAL POWER CORE)/tools.py`: implements actual command helpers such as opening YouTube, Google, Notepad, screenshots, and Wikipedia search.
- `WAKE WORD SYSTEM (IMPROVED VERSION)/detection.py`: detects the wake phrase and returns whether the assistant should respond.

## Key guidance
- Focus changes on the Version 3 modular path; do not modify `jarvis_final.py` or `jarvis_v2.py` unless specifically requested.
- Keep the architecture modular: new capabilities should follow the pattern of adding an action string to `engine.py`, handling it in `jarvis_v3.py`, and implementing the tool in `tools.py`.
- Preserve placeholder API key strings and avoid hard-coded secrets. Make OpenAI integration configurable and optional.
- Use `speak()` for any spoken output and `listen()` for voice input.
- Guard optional dependencies (`openai`, `pyautogui`, etc.) with imports inside try/except blocks.
- Prefer explicit tool execution over broad free-form command parsing.
- Use the fallback AI chat only when the action is `general_answer` or no built-in tool action matches.

## Best practices
- Keep file-level responsibilities clear: `engine.py` decides actions, `jarvis_v3.py` executes them, `tools.py` performs them.
- Keep user-facing behaviors simple and predictable.
- Validate that any new imports are available in the workspace and documented.
- If adding memory features, update `memory.py` and use it from `jarvis_v3.py`.
- Keep the wake-word flow intact: detect `hey jarvis`, ask follow-up, then process the command.

## When adding or changing behavior
1. Add or update one action string in `AI BRAIN (TOOL DECISION ENGINE)/engine.py`.
2. Add the corresponding branch in `MAIN JARVIS LOOP (FULL SYSTEM)/jarvis_v3.py`.
3. Implement the actual functionality in `TOOL SYSTEM (REAL POWER CORE)/tools.py`.
4. Keep memory and wake-word logic separated in `MEMORY SYSTEM (NEW)/memory.py` and `WAKE WORD SYSTEM (IMPROVED VERSION)/detection.py`, respectively.
