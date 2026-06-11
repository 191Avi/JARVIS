import os
import json
try:
    from dotenv import load_dotenv
    # Load .env from the project root (one level up from backend/)
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))
except ImportError:
    pass
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

from tools import execute_tool, list_tools, TOOL_SCHEMAS
from memory import save_interaction, get_history, get_conversation_context, get_stats, clear_history, init_db

# ===== SETUP =====
app = FastAPI(title="JARVIS v7 API", version="7.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are JARVIS, an intelligent AI assistant with access to tools.
You remember previous conversations and can use tools to take real actions.

Personality: concise, helpful, confident — like the AI from Iron Man.
When using a tool, don't explain what you're about to do, just do it.
After a tool runs, give a short natural confirmation.
"""

CONTEXT_TURNS = 10  # how many previous exchanges to include


# ===== MODELS =====
class ChatRequest(BaseModel):
    prompt: str
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    tool_used: str | None = None
    tool_args: dict | None = None

class ClearRequest(BaseModel):
    confirm: bool = False


# ===== STARTUP =====
@app.on_event("startup")
def startup():
    init_db()

    # Mount frontend if it exists
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
    if os.path.isdir(frontend_path):
        app.mount("/ui", StaticFiles(directory=frontend_path, html=True), name="frontend")


# ===== CHAT (non-streaming) =====
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured.")

    # Build messages: system + conversation history + new user message
    context = get_conversation_context(turns=CONTEXT_TURNS)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + context + [
        {"role": "user", "content": req.prompt}
    ]

    tool_used = None
    tool_args = None
    ai_reply  = ""

    try:
        # First call — GPT decides whether to use a tool
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        if msg.tool_calls:
            # GPT wants to call a tool
            tc        = msg.tool_calls[0]
            tool_used = tc.function.name
            tool_args = json.loads(tc.function.arguments)
            tool_result = execute_tool(tool_used, tool_args)

            # Second call — let GPT form a natural response using the tool result
            messages.append(msg)  # assistant message with tool_calls
            messages.append({
                "role":         "tool",
                "tool_call_id": tc.id,
                "content":      tool_result
            })
            followup = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            ai_reply = followup.choices[0].message.content.strip()
        else:
            ai_reply = msg.content.strip()

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {e}")

    save_interaction(req.prompt, ai_reply, tool_used, tool_args)
    return ChatResponse(response=ai_reply, tool_used=tool_used, tool_args=tool_args)


# ===== CHAT (streaming) =====
@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_API_KEY":
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured.")

    context = get_conversation_context(turns=CONTEXT_TURNS)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + context + [
        {"role": "user", "content": req.prompt}
    ]

    def generate():
        tool_used   = None
        tool_args   = None
        full_reply  = ""

        try:
            # First: check if a tool call is needed (non-streaming so we can inspect)
            check = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
            )
            msg = check.choices[0].message

            if msg.tool_calls:
                tc          = msg.tool_calls[0]
                tool_used   = tc.function.name
                tool_args   = json.loads(tc.function.arguments)
                tool_result = execute_tool(tool_used, tool_args)

                # Signal tool use to client
                yield f"data: {json.dumps({'type': 'tool', 'tool': tool_used, 'args': tool_args, 'result': tool_result})}\n\n"

                # Stream the natural follow-up
                messages.append(msg)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": tool_result})
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_reply += delta
                        yield f"data: {json.dumps({'type': 'token', 'content': delta})}\n\n"
            else:
                # Stream the reply directly
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_reply += delta
                        yield f"data: {json.dumps({'type': 'token', 'content': delta})}\n\n"

            # Done signal
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            save_interaction(req.prompt, full_reply, tool_used, tool_args)

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# ===== OTHER ROUTES =====
@app.get("/history")
def history(limit: int = 20):
    return {"history": get_history(limit)}


@app.get("/stats")
def stats():
    return get_stats()


@app.get("/tools")
def tools():
    return {"tools": list_tools()}


@app.post("/clear")
def clear(req: ClearRequest):
    if not req.confirm:
        raise HTTPException(status_code=400, detail="Set confirm=true to clear history.")
    return {"message": clear_history()}


@app.get("/health")
def health():
    return {"status": "online", "version": "7.0"}
