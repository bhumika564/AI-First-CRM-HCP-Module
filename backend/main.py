from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from database import init_db, get_db
from models import Interaction
from agent import agent_executor
from langchain_core.messages import HumanMessage

app = FastAPI(title="AI-First CRM HCP Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_thread"

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        messages = [HumanMessage(content=request.message)]
        response = agent_executor.invoke({"messages": messages}, config)
        
        # Extract the last AI message
        ai_message = response["messages"][-1].content
        return {"response": ai_message}
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/interactions")
def get_interactions(db: Session = Depends(get_db)):
    interactions = db.query(Interaction).order_by(Interaction.created_at.desc()).all()
    return interactions

@app.post("/api/interactions")
def create_interaction(data: dict, db: Session = Depends(get_db)):
    try:
        new_interaction = Interaction(**data)
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return new_interaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
