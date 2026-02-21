from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.executors import SequentialToolExecutor
from tools.categorizer import categorizer
from tools.db import insert_income, insert_outcome, create_user
from db.db import DB
from db.queries.conversation_queries import ConversationQueries
from contextlib import asynccontextmanager
import time
import json
import asyncio

# ── Load prompt files ──────────────────────────────────────────
with open("AGENT.md", "r") as f:
  CONTEXT = f.read()
with open("instructions/instructions.input.md", "r") as f:
  INPUT_INSTRUCTIONS = f.read()
with open("instructions/instructions.output.md", "r") as f:
  OUTPUT_INSTRUCTIONS = f.read()

# ── Database ───────────────────────────────────────────────────
_db = DB()

# ── Session store ──────────────────────────────────────────────
# Maps conversation_id → { "agent": Agent, "last_active": timestamp }
_sessions: dict[int, dict] = {}
SESSION_TTL_SECONDS = 30 * 60  # 30 minutes


def _cleanup_stale_sessions():
  """Remove sessions inactive beyond TTL."""
  now = time.time()
  stale = [
    cid for cid, data in _sessions.items()
    if now - data["last_active"] > SESSION_TTL_SECONDS
  ]
  for cid in stale:
    del _sessions[cid]


def _create_agent(user_id: int) -> Agent:
  """Create a fresh agent with no conversation history."""
  model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1:latest",
    temperature=0.2,
    top_p=0.5,
  )
  return Agent(
    tool_executor=SequentialToolExecutor(),
    model=model,
    tools=[categorizer, insert_income, insert_outcome, create_user],
    system_prompt=f"{CONTEXT}\n\n{INPUT_INSTRUCTIONS}",
    structured_output_prompt=OUTPUT_INSTRUCTIONS,
    state={"user_id": user_id},
  )


def _rebuild_agent_from_db(conversation_id: int, user_id: int) -> Agent:
  """
  Rebuild an agent by replaying conversation history from the database.
  Only called ONCE when a session is not in memory (expired or server restarted).
  """
  agent = _create_agent(user_id)
  rows = _db.execute_query(
    ConversationQueries.get_conversation_messages(conversation_id)
  )
  if rows:
    for row in rows:
      agent.messages.append({
        "role": row[0],
        "content": [{"text": row[1]}],
      })
  return agent


def get_or_create_agent(conversation_id: int, user_id: int) -> Agent:
  """
  - Agent in memory → return it (0 DB reads)
  - Agent expired → rebuild from DB (1 DB read), then cache it
  - New conversation → create fresh agent, cache it
  """
  _cleanup_stale_sessions()

  if conversation_id in _sessions:
    _sessions[conversation_id]["last_active"] = time.time()
    return _sessions[conversation_id]["agent"]

  agent = _rebuild_agent_from_db(conversation_id, user_id)
  _sessions[conversation_id] = {
    "agent": agent,
    "last_active": time.time(),
  }
  return agent


# ── App lifecycle ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
  print("AccountantAgent API is starting...")
  yield
  _sessions.clear()
  print("AccountantAgent API shut down.")


# ── FastAPI app ────────────────────────────────────────────────
app = FastAPI(
  title="AccountantAgent API",
  description="Personal finance AI agent exposed as a REST API",
  version="0.1.0",
  lifespan=lifespan,
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# ── Models ─────────────────────────────────────────────────────

class Message(BaseModel):
  role: str
  content: str
  created_at: str

  @staticmethod
  def build(row) -> "Message":
    return Message(role=row[0], content=row[1], created_at=str(row[2]))

class CreateConversationRequest(BaseModel):
  user_id: int = 1
  title: str = "New Conversation"

class ConversationResponse(BaseModel):
  id: int
  title: str
  created_at: str

class ConversationListItem(BaseModel):
  id: int
  title: str
  created_at: str
  updated_at: str

  @staticmethod
  def build(row) -> "ConversationListItem":
    return ConversationListItem(
      id=row[0], title=row[1], created_at=str(row[2]), updated_at=str(row[3])
    )

class Conversations(BaseModel):
  conversations: list[ConversationListItem]
  
  @staticmethod
  def build(rows) -> "Conversations":
    return Conversations(
      conversations=[ConversationListItem.build(row) for row in rows]
    )

class ChatRequest(BaseModel):
  message: str

# CONVERSATION AND MESSAGE MANAGEMENT

@app.post("/conversations", response_model=ConversationResponse)
async def create_conversation(request: CreateConversationRequest):
  """Create a new conversation for a user."""
  result = _db.execute_query(
    ConversationQueries.create_conversation(request.user_id, request.title)
  )
  if not result:
    raise HTTPException(status_code=500, detail="Failed to create conversation")
  row = result[0]
  return ConversationResponse(id=row[0], title=row[1], created_at=str(row[2]))


@app.get("/conversations/{user_id}", response_model=list[ConversationListItem])
async def get_conversations(user_id: int):
  """List all conversations for a user."""
  rows = _db.execute_query(
    ConversationQueries.get_conversations_by_user(user_id)
  )
  if not rows:
    return []
  return Conversations.build(rows).conversations

@app.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: int) -> list[Message]:
  """Get all messages in a conversation (for loading chat history in UI)."""
  rows = _db.execute_query(
    ConversationQueries.get_conversation_messages(conversation_id)
  )
  if not rows:
    return []
  return [ Message.build(r) for r in rows ]


# CHAT

@app.websocket("/ws/chat/{conversation_id}")
async def websocket_chat(
  websocket: WebSocket,
  conversation_id: int,
  user_id: int = Query(default=1),
):
  """
  WebSocket for real-time chat.

  Connect:
    ws://localhost:8000/ws/chat/42?user_id=1

  Client sends:
    { "message": "gasté 500 en comida" }

  Server sends:
    { "type": "start" }
    { "type": "end", "content": "✅ Transacción guardada..." }
    { "type": "error", "content": "..." }
  """
  await websocket.accept()

  agent = get_or_create_agent(conversation_id, user_id)

  try:
    while True:
      data = await websocket.receive_text()
      payload = json.loads(data)
      user_message = payload["message"]

      await websocket.send_text(json.dumps({"type": "start"}))

      result = await asyncio.to_thread(agent, user_message)

      await websocket.send_text(json.dumps({
        "type": "end",
        "content": str(result),
      }))

      _db.execute_query(
        ConversationQueries.insert_message(conversation_id, "user", user_message)
      )
      _db.execute_query(
        ConversationQueries.insert_message(conversation_id, "assistant", str(result))
      )
      _db.execute_query(
        ConversationQueries.update_conversation_timestamp(conversation_id)
      )

  except WebSocketDisconnect:
    print(f"Client disconnected from conversation {conversation_id}")
  except Exception as e:
    try:
      await websocket.send_text(json.dumps({
        "type": "error",
        "content": str(e),
      }))
    except:
      pass

# Alternative to websockets
@app.post('/chat/{conversation_id}/{user_id}')
async def chat_endpoint(conversation_id: int, user_id: int, request: ChatRequest):
  """Handle chat messages."""
  agent = get_or_create_agent(conversation_id, user_id)
  try:

    _db.execute_query(
      ConversationQueries.insert_message(conversation_id, "user", request.message)
    )

    response = await asyncio.to_thread(agent, request.message)

    _db.execute_query(
      ConversationQueries.insert_message(conversation_id, "assistant", str(response))
    )
    _db.execute_query(
      ConversationQueries.update_conversation_timestamp(conversation_id)
    )

    return {"response": str(response)}
  except Exception as e:
    return {"error": str(e)}
