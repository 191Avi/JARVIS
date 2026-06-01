# AGENTS

## Purpose
This repository contains multiple versions of a Python-based voice assistant named JARVIS. The main workspace is a simple speech-enabled assistant with optional OpenAI integration, and it also includes an upgraded architecture under `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)`.

## Agent guidance
- Prefer the latest architecture in `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)` when making enhancements.
- Treat `jarvis_final.py` and `jarvis_v2.py` as earlier, standalone voice assistant versions.
- The `VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)` folder is the most modular design and should guide structural changes.

## Key files and components
- `jarvis_final.py` — voice assistant with wake-word listening, memory persistence, built-in commands, and optional OpenAI fallback.
- `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)\jarvis_v2.py` — upgraded voice assistant with direct OpenAI chat completion support.
- `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)\VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)\MAIN JARVIS LOOP (FULL SYSTEM)\jarvis_v3.py` — main control loop for the modular system.
- `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)\VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)\AI BRAIN (TOOL DECISION ENGINE)\engine.py` — action decision engine that maps user input to tool names.
- `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)\VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)\MEMORY SYSTEM (NEW)\memory.py` — memory load/save helper.
- `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)\VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)\TOOL SYSTEM (REAL POWER CORE)\tools.py` — tool implementations for opening services and interacting with OS resources.
- `VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)\VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)\WAKE WORD SYSTEM (IMPROVED VERSION)\detection.py` — wake word detection and action decision integration.

## Conventions
- Python scripts are executed directly. There is no build system or tests directory in this workspace.
- OpenAI integration is optional and uses placeholder API key strings.
- Speech recognition uses `speech_recognition`; voice output uses `pyttsx3`.
- The project keeps memory in JSON files like `memory.json`.

## What an AI agent should do first
1. Identify the target version before editing: `jarvis_final.py` for version 1, `jarvis_v2.py` for version 2, or the Version 3 subfolders for the modular system.
2. Preserve `OPENAI_API_KEY` placeholders and make API integration configurable, not hard-coded.
3. Keep voice assistant behavior simple and explicit: available commands, wake-word flow, and fallback AI chat.
4. Validate that any new module imports are available in the workspace and documented.

## Suggested next customization
- Add a `skills/` or `prompts/` customization file for `jarvis_v2.py` and `VERSION 3 REAL JARVIS SYSTEM` improvements, focusing on voice assistant command expansion, OpenAI prompt design, and modular tool actions.
