<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:16213e&height=200&section=header&text=JARVIS&fontSize=80&fontColor=00d4ff&fontAlignY=38&desc=Just%20A%20Rather%20Very%20Intelligent%20System&descAlignY=60&descColor=ffffff&animation=fadeIn" width="100%"/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Versions](https://img.shields.io/badge/Versions-6-blueviolet?style=for-the-badge)](#version-history)

> *A personal AI assistant built in Python — evolved through **6 major versions** from a basic voice assistant to a full production-grade multi-agent AI platform.*

</div>

---

## 🧠 What is JARVIS?

JARVIS (**J**ust **A** **R**ather **V**ery **I**ntelligent **S**ystem) is a personal AI assistant inspired by Tony Stark's iconic AI companion. Built entirely in Python, this project documents the complete evolution of an AI assistant — from its first "Hello, how can I help you?" to a production-ready multi-agent platform capable of autonomous task planning and execution.

Each version is a complete, standalone project that introduces new concepts, patterns, and capabilities.

---

## 🚀 Version History

| Version | Name | Key Capability |
|---------|------|---------------|
| [v1](#v1--basic-voice-assistant) | Basic Voice Assistant | Voice I/O, Wikipedia, browser control |
| [v2](#v2--smart-ai-assistant) | Smart AI Assistant | GPT-powered brain, wake word detection |
| [v3](#v3--real-jarvis--agent-architecture) | Real JARVIS — Agent Architecture | Modular tools, memory, AI-driven tool selection |
| [v4](#v4--autonomous-ai-agent) | Autonomous AI Agent | Multi-step task planning & execution |
| [v5](#v5--multi-agent-ai-system) | Multi-Agent AI System | Manager → Planner / Research / Executor / Critic |
| [v6](#v6--production-ai-platform) | Production AI Platform | FastAPI backend, SQLite memory, browser dashboard |
| [v7](#v7--intelligent-ai-platform) | Intelligent AI Platform | OpenAI function calling, streaming (SSE), web UI, persistent memory |

---

## 📦 Version Details

### v1 — Basic Voice Assistant

> **"The foundation"** — Voice in, voice out.

JARVIS begins as a simple voice assistant that listens to spoken commands and responds with text-to-speech output. No AI, no cloud — just Python doing what Python does best.

**Capabilities:**
- 🎙️ Voice input via microphone
- 🔊 Text-to-speech responses (pyttsx3)
- ⏰ Time & date queries
- 📖 Wikipedia lookups
- 🌐 Browser control (open websites)

```bash
cd "VERSION 1 BASIC VOICE ASSISTANT"
python jarvis_final.py
```

---

### v2 — Smart AI Assistant

> **"Give JARVIS a real brain"** — GPT enters the chat.

OpenAI's GPT is integrated as the fallback brain. Anything JARVIS doesn't know how to handle natively is sent to GPT for an intelligent response. Wake word detection means JARVIS is always listening.

**New in v2:**
- 🤖 OpenAI GPT-4o-mini integration
- 🗣️ Wake word activation
- ❓ Unknown commands answered by GPT
- 💬 Conversational context

```bash
cd "VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)"
python jarvis_v2.py
```

---

### v3 — Real JARVIS — Agent Architecture

> **"Stop hard-coding everything"** — Tools, engine, memory.

A complete architectural rewrite. JARVIS now has a modular tool system where each capability is a separate tool, an AI engine decides which tool to use, and a memory system remembers what was said.

**Architecture:**
```
jarvis_v3.py (main loop)
    ├── engine.py     ← AI decides which tool to call
    ├── tools.py      ← all capabilities registered as tools
    ├── memory.py     ← conversation history
    └── detection.py  ← wake word system
```

**New in v3:**
- 🔧 Modular tool registry
- 🧠 AI-driven tool selection engine
- 💾 Persistent memory system
- 🔍 Web research capability
- 🛡️ Wake word system (dedicated module)

```bash
cd "VERSION 3 REAL JARVIS SYSTEM"
python "MAIN JARVIS LOOP/jarvis_v3.py"
```

---

### v4 — Autonomous AI Agent

> **"Don't just answer — act."** — Multi-step task planning.

JARVIS can now plan and execute multi-step tasks autonomously. Given a complex goal, it breaks it down into steps, executes them in sequence, and reports results.

**New in v4:**
- 📋 Task planning (goal → steps)
- ⚡ Sequential step execution
- 🔄 Autonomous retry & error handling
- 📊 Execution logging

```bash
cd "VERSION 4  AUTONOMOUS AI AGENT SYSTEM"
python tools.py
```

---

### v5 — Multi-Agent AI System

> **"One agent isn't enough."** — JARVIS becomes an organization.

Inspired by real AI research teams, v5 introduces a full multi-agent pipeline. A Manager agent receives the user request and delegates to specialized sub-agents, all reviewed by a Critic agent before the final response is delivered.

**Agent Pipeline:**
```
User Request
    ↓
Manager Agent      ← decides which agents are needed
    ↓
┌──────────────────────────┐
│  Planner  │  Research  │  Executor  │
└──────────────────────────┘
    ↓
Critic Agent       ← reviews & improves output
    ↓
Memory Store       ← saves everything
    ↓
Final Response
```

**New in v5:**
- 🏢 Multi-agent orchestration
- 🔬 Dedicated Research agent
- 🎯 Dedicated Executor agent
- ✅ Critic agent for quality control
- 🗂️ Shared memory across agents

```bash
cd "VERSION 5 MULTI-AGENT AI SYSTEM (JARVIS ORGANIZATION)"
python orchestrator.py
```

---

### v6 — Production AI Platform

> **"Ship it."** — JARVIS goes to production.

The final form: a fully productionized AI platform with a REST API backend, SQLite-backed persistent memory, a browser-based dashboard, and a decoupled voice client. Everything runs as separate services.

**Architecture:**
```
Voice / Chat UI (browser dashboard)
        ↓
  FastAPI Gateway  (port 8000)
        ↓
  AI Brain (GPT-4o-mini)
        ↓
  ┌─────┼──────┐
Tools  DB    Web
```

**New in v6:**
- 🌐 FastAPI REST backend
- 📚 SQLite persistent memory
- 🖥️ Browser dashboard (HTML/JS frontend)
- 🔌 Decoupled voice client
- 📡 Full REST API with interactive docs
- 🛠️ Tool registry via API

```bash
# Terminal 1 — start the backend
run_backend.bat

# Terminal 2 — voice client
run_client.bat

# Or open the browser dashboard
run_frontend.bat
```

**API available at:** `http://localhost:8000`
**Interactive docs at:** `http://localhost:8000/docs`

---

### v7 — Intelligent AI Platform

> **"The brain rewires itself"** — the assistant decides when to use tools.

The next-generation platform. JARVIS now uses **OpenAI function calling** to choose tools on its own, streams responses token-by-token over **Server-Sent Events**, keeps a rolling conversation context in SQLite, and serves a built-in web UI. The full project ships as `VERSION 7  INTELLIGENT AI PLATFORM (JARVIS NEXT-GEN).zip`.

**New in v7:**
- 🧠 OpenAI function calling (model-driven tool selection)
- ⚡ Streaming responses via Server-Sent Events (SSE)
- 🗂️ Persistent memory with rolling conversation context
- 🖥️ Built-in web UI served at `/ui`
- 🛠️ Expanded tools: Google, Wikipedia, weather, reminders, screenshots, open files/apps, time
- 🔐 No bundled keys — bring your own in a local `.env`

```bash
# Unzip "VERSION 7  INTELLIGENT AI PLATFORM (JARVIS NEXT-GEN).zip", then:
install.bat                 # install dependencies
copy .env.example .env      # then add your own OPENAI key
run_backend.bat             # start the server
```

Web UI at: `http://localhost:8000/ui` — or run `run_client.bat` for the voice/text client.

---

## 🗂️ Project Structure

```
JARVIS/
├── VERSION 1  BASIC VOICE ASSISTANT/
│   ├── jarvis.py
│   ├── jarvis_final.py
│   └── run_jarvis.bat
├── VERSION 2 SMART AI ASSISTANT (JARVIS UPGRADE)/
│   ├── jarvis_v2.py
│   └── VERSION 3 REAL JARVIS SYSTEM (AI AGENT ARCHITECTURE)/   ← v3 lives inside v2
│       ├── AI BRAIN (TOOL DECISION ENGINE)/engine.py
│       ├── MAIN JARVIS LOOP (FULL SYSTEM)/jarvis_v3.py        ← v3 entry point
│       ├── MEMORY SYSTEM (NEW)/memory.py
│       ├── TOOL SYSTEM (REAL POWER CORE)/tools.py
│       └── WAKE WORD SYSTEM (IMPROVED VERSION)/detection.py
├── VERSION 4  AUTONOMOUS AI AGENT SYSTEM/
│   ├── tools.py            ← entry point (run this)
│   ├── planner.py
│   ├── memory.py
│   └── toolsystem.py
├── VERSION 5  MULTI-AGENT AI SYSTEM (JARVIS ORGANIZATION)/
│   ├── orchestrator.py     ← main entry point
│   ├── manager.py
│   ├── planner.py
│   ├── research.py
│   ├── executor.py
│   ├── critic.py
│   └── memory.py
├── VERSION 6  PRODUCTION AI SYSTEM (JARVIS PLATFORM)/
│   ├── backend/
│   │   ├── main.py         ← FastAPI server
│   │   ├── tools.py        ← tool registry
│   │   └── memory.py       ← SQLite database
│   ├── client/client.py    ← voice client
│   ├── frontend/index.html ← browser dashboard
│   ├── requirements.txt
│   ├── run_backend.bat
│   ├── run_client.bat
│   └── run_frontend.bat
├── VERSION 7  INTELLIGENT AI PLATFORM (JARVIS NEXT-GEN)/
│   ├── backend/
│   │   ├── main.py         ← FastAPI server (function calling, SSE)
│   │   ├── tools.py        ← tool registry + schemas
│   │   └── memory.py       ← SQLite memory + rolling context
│   ├── client/client.py    ← voice/text client
│   ├── frontend/index.html ← web UI (served at /ui)
│   ├── requirements.txt
│   ├── .env.example
│   ├── install.bat
│   ├── install_voice.bat
│   ├── run_backend.bat
│   └── run_client.bat
├── jarvis_showcase.html    ← visual showcase page
├── AGENTS.md
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- A microphone (for voice versions)
- An OpenAI API key (optional — all versions include local fallback)

### Install Dependencies

```bash
pip install openai fastapi uvicorn speechrecognition pyttsx3 wikipedia requests beautifulsoup4 pyautogui
```

### Set Your OpenAI API Key

```bash
# Windows (permanent)
setx OPENAI_API_KEY "sk-your-key-here"

# Linux / macOS
export OPENAI_API_KEY="sk-your-key-here"
```

> **Note:** All versions work without an API key using local fallback logic. You only need a key to unlock full AI responses.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core language |
| **OpenAI GPT-4o-mini** | AI brain & reasoning |
| **FastAPI + Uvicorn** | Production API server (v6) |
| **SQLite** | Persistent memory (v6) |
| **SpeechRecognition** | Voice input |
| **pyttsx3** | Text-to-speech output |
| **Wikipedia API** | Knowledge lookups |
| **BeautifulSoup4** | Web research & scraping |
| **PyAutoGUI** | Desktop automation |

---

## 🗺️ Evolution Roadmap

```
v1  ──►  Voice I/O + basic commands
v2  ──►  GPT brain + wake word
v3  ──►  Agent architecture + tool system
v4  ──►  Autonomous planning + execution
v5  ──►  Multi-agent organization
v6  ──►  Production platform + REST API
v7  ──►  Intelligent platform: function calling + streaming + web UI
```

---

## 👤 Author

**Avijit Saha Apu** — [@191Avi](https://github.com/191Avi)

*Building JARVIS, one version at a time.*

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:16213e,100:1a1a2e&height=120&section=footer" width="100%"/>
</div>
