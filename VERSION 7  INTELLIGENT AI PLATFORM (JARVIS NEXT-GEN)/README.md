# JARVIS v7 — Intelligent AI Platform

A JARVIS-style AI assistant with tool use, persistent memory, streaming responses, and optional voice control.

## Features
- **OpenAI function calling** — the assistant decides when to use tools (Google search, Wikipedia, weather, reminders, screenshots, open files/apps, time).
- **Persistent memory** — SQLite-backed conversation history with rolling context.
- **Streaming** — token-by-token Server-Sent Events.
- **Voice or text** — voice client with automatic text fallback.
- **Web UI** — served at `/ui`.

## Tech stack
FastAPI · OpenAI · SQLite · Server-Sent Events · Vanilla JS frontend

## Setup
1. Install dependencies:
   ```
   install.bat
   ```
2. Copy `.env.example` to `.env` and add **your own** OpenAI key
   (get one at https://platform.openai.com/api-keys):
   ```
   OPENAI_API_KEY=sk-your-own-key-here
   ```
   > This repo does not include any API key. You must use your own.
3. Start the backend:
   ```
   run_backend.bat
   ```
4. Open the web UI at http://localhost:8000/ui, or run the voice/text client:
   ```
   run_client.bat
   ```

## Optional: voice support
```
install_voice.bat
```

## Security
This project ships **no API keys**. Each user supplies their own in a local `.env` file, which is gitignored and never committed.

---
Built by [@191Avi](https://github.com/191Avi)
