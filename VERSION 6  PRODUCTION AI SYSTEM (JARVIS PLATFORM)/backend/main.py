import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

from tools import execute_tool, list_tools
from memory import save_interaction, get_history, init_db

# ===== SETUP =====
app = FastAPI(title="JARVIS v6 API", version="6.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are Jarvis, a smart AI assistant with access to tools.

When the user wants to USE a tool, respond ONLY with the tool command — nothing else:
  TOOL:youtube               → opens YouTube
  TOOL:google:<query>        → searches Google for <query>
  TOOL:notepad               → opens Notepad
  TOOL:wikipedia:<query>     → searches Wikipedia for <query>
  TOOL:screenshot            → takes a screenshot

For everything else, answer normally and helpfully.
Be concise. Do not explain your tool choices.
"""

# ===== MODELS =====
class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    tool_used: str | None = None

# ===== STARTUP =====
@app.on_event("startup")
def startup():
    init_db()

# ===== ROUTES =====
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured.")

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": req.prompt}
            ]
        )
        ai_reply = res.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {e}")

    # Tool routing
    tool_used = None
    if ai_reply.startswith("TOOL:"):
        parts = ai_reply[5:].split(":", 1)
        tool_name = parts[0].strip()
        tool_arg  = parts[1].strip() if len(parts) > 1 else ""
        tool_result = execute_tool(tool_name, tool_arg)
        ai_reply = tool_result
        tool_used = tool_name

    save_interaction(req.prompt, ai_reply, tool_used)
    return ChatResponse(response=ai_reply, tool_used=tool_used)


@app.get("/history")
def history(limit: int = 20):
    return {"history": get_history(limit)}


@app.get("/tools")
def tools():
    return {"tools": list_tools()}


@app.get("/health")
def health():
    return {"status": "online", "version": "6.0"}
