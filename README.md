# JARVIS — AI Assistant System

> Just A Rather Very Intelligent System

A personal AI assistant built in Python, evolved through 6 versions from a basic voice assistant to a full production-grade multi-agent AI platform.

---

## Version History

| Version | Name | What it does |
|---------|------|-------------|
| v1 | Basic Voice Assistant | Voice input, TTS output, time/Wikipedia/browser |
| v2 | Smart AI Assistant | OpenAI brain, wake word, unknown commands answered by GPT |
| v3 | Real JARVIS — Agent Architecture | Modular tools/engine/memory, AI picks the right tool |
| v4 | Autonomous AI Agent | Plans multi-step tasks, executes them in sequence |
| v5 | Multi-Agent AI System | Manager → Planner / Research / Executor / Critic agents |
| v6 | Production AI Platform | FastAPI backend, SQLite memory, browser dashboard, REST API |

---

## Project Structure

```
JARVIS/
├── VERSION 1  BASIC VOICE ASSISTANT/
│   ├── jarvis.py
│   └── jarvis_final.py
├── VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)/
│   ├── jarvis_v2.py
│   └── VERSION 3 REAL JARVIS SYSTEM/
│       ├── AI BRAIN (TOOL DECISION ENGINE)/engine.py
│       ├── MAIN JARVIS LOOP/jarvis_v3.py
│       ├── MEMORY SYSTEM/memory.py
│       ├── TOOL SYSTEM/tools.py
│       └── WAKE WORD SYSTEM/detection.py
├── VERSION 4  AUTONOMOUS AI AGENT SYSTEM/
│   ├── tools.py
│   ├── planner.py
│   ├── memory.py
│   └── toolsystem.py
├── VERSION 5  MULTI-AGENT AI SYSTEM (JARVIS ORGANIZATION)/
│   ├── orchestrator.py      ← main entry point
│   ├── manager.py
│   ├── planner.py
│   ├── research.py
│   ├── executor.py
│   ├── critic.py
│   └── memory.py
├── VERSION 6  PRODUCTION AI SYSTEM (JARVIS PLATFORM)/
│   ├── backend/
│   │   ├── main.py          ← FastAPI server
│   │   ├── tools.py         ← tool registry
│   │   └── memory.py        ← SQLite database
│   ├── client/
│   │   └── client.py        ← voice client
│   ├── frontend/
│   │   └── index.html       ← browser dashboard
│   ├── run_backend.bat
│   ├── run_client.bat
│   └── run_frontend.bat
├── jarvis_showcase.html     ← visual showcase page
└── README.md
```

---

## Quick Start

### Version 1 — Basic Voice Assistant
```bash
cd "VERSION 1  BASIC VOICE ASSISTANT"
python jarvis_final.py
```

### Version 5 — Multi-Agent System
```bash
cd "VERSION 5  MULTI-AGENT AI SYSTEM (JARVIS ORGANIZATION)"
python orchestrator.py
```

### Version 6 — Production Backend
```bash
# Terminal 1 — start the backend
run_backend.bat

# Terminal 2 — voice client
run_client.bat

# Or open the browser dashboard
run_frontend.bat
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## Setup

### Install dependencies
```bash
pip install openai fastapi uvicorn speechrecognition pyttsx3 wikipedia requests beautifulsoup4 pyautogui
```

### Set your OpenAI API key
```bash
# Windows (permanent)
setx OPENAI_API_KEY "sk-your-key-here"
```

All versions read the key from the environment automatically. No hardcoding needed.

> **Note:** All versions work without an API key using local fallback logic. You only need a key to unlock full AI responses.

---

## Tech Stack

- **Python 3.14**
- **OpenAI GPT-4o-mini** — AI brain
- **FastAPI + Uvicorn** — production API server
- **SQLite** — persistent memory
- **SpeechRecognition** — voice input
- **pyttsx3** — text-to-speech
- **Wikipedia API** — knowledge lookup
- **BeautifulSoup4** — web research

---

## Architecture (v6)

```
Voice / Chat UI
      ↓
 API Gateway (FastAPI)
      ↓
 AI Brain (GPT-4o-mini)
      ↓
 ┌────┼────┐
Tools  DB  Web
```

---

## Multi-Agent Flow (v5)

```
User Request
      ↓
 Manager Agent  →  decides which agents are needed
      ↓
 Planner    Research    Executor
      ↓
 Critic Agent  →  reviews and improves output
      ↓
 Memory Store  →  saves everything
```

---

*Built with Python and OpenAI*
