from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from models import Interaction
from database import SessionLocal
import json

class LogInteractionInput(BaseModel):
    hcp_name: str = Field(description="Name of the Healthcare Professional")
    interaction_type: str = Field(description="Type of interaction (e.g., Meeting, Call, Email)")
    date: str = Field(description="Date of interaction in YYYY-MM-DD format")
    time: str = Field(description="Time of interaction in HH:MM format")
    attendees: Optional[str] = Field(default="", description="Comma separated list of attendees")
    topics: Optional[str] = Field(default="", description="Topics discussed")
    materials: Optional[str] = Field(default="", description="Materials shared")
    samples: Optional[str] = Field(default="", description="Samples distributed")
    sentiment: Optional[str] = Field(default="Neutral", description="Sentiment (Positive, Neutral, Negative)")
    outcomes: Optional[str] = Field(default="", description="Outcomes or agreements")
    follow_up: Optional[str] = Field(default="", description="Follow-up actions")

@tool("log_interaction", args_schema=LogInteractionInput, return_direct=False)
def log_interaction(
    hcp_name: str, 
    interaction_type: str, 
    date: str, 
    time: str, 
    attendees: str = "", 
    topics: str = "", 
    materials: str = "", 
    samples: str = "", 
    sentiment: str = "Neutral", 
    outcomes: str = "", 
    follow_up: str = ""
) -> str:
    """Logs a new interaction with a Healthcare Professional into the CRM system."""
    db = SessionLocal()
    try:
        new_interaction = Interaction(
            hcp_name=hcp_name,
            interaction_type=interaction_type,
            date=date,
            time=time,
            attendees=attendees,
            topics=topics,
            materials=materials,
            samples=samples,
            sentiment=sentiment,
            outcomes=outcomes,
            follow_up=follow_up
        )
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return f"Interaction with {hcp_name} logged successfully with ID {new_interaction.id}."
    except Exception as e:
        db.rollback()
        return f"Error logging interaction: {str(e)}"
    finally:
        db.close()

class EditInteractionInput(BaseModel):
    interaction_id: int = Field(description="The ID of the interaction to edit")
    hcp_name: Optional[str] = Field(default=None, description="Updated HCP Name")
    interaction_type: Optional[str] = Field(default=None, description="Updated interaction type")
    date: Optional[str] = Field(default=None, description="Updated date")
    time: Optional[str] = Field(default=None, description="Updated time")
    attendees: Optional[str] = Field(default=None, description="Updated attendees")
    topics: Optional[str] = Field(default=None, description="Updated topics")
    materials: Optional[str] = Field(default=None, description="Updated materials")
    samples: Optional[str] = Field(default=None, description="Updated samples")
    sentiment: Optional[str] = Field(default=None, description="Updated sentiment")
    outcomes: Optional[str] = Field(default=None, description="Updated outcomes")
    follow_up: Optional[str] = Field(default=None, description="Updated follow-up actions")

@tool("edit_interaction", args_schema=EditInteractionInput, return_direct=False)
def edit_interaction(
    interaction_id: int, 
    **kwargs
) -> str:
    """Edits an existing interaction in the CRM system. Only provide fields that need to be updated."""
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return f"Error: Interaction with ID {interaction_id} not found."
        
        for key, value in kwargs.items():
            if value is not None:
                setattr(interaction, key, value)
        
        db.commit()
        return f"Interaction ID {interaction_id} updated successfully."
    except Exception as e:
        db.rollback()
        return f"Error updating interaction: {str(e)}"
    finally:
        db.close()

class GetPastInteractionsInput(BaseModel):
    hcp_name: str = Field(description="Name of the Healthcare Professional to search history for")
    limit: Optional[int] = Field(default=5, description="Maximum number of interactions to retrieve")

@tool("get_past_interactions", args_schema=GetPastInteractionsInput, return_direct=False)
def get_past_interactions(hcp_name: str, limit: int = 5) -> str:
    """Retrieves the past interactions for a specific Healthcare Professional."""
    db = SessionLocal()
    try:
        interactions = db.query(Interaction).filter(Interaction.hcp_name.ilike(f"%{hcp_name}%")).order_by(Interaction.created_at.desc()).limit(limit).all()
        if not interactions:
            return f"No past interactions found for {hcp_name}."
        
        results = []
        for p in interactions:
            results.append({
                "id": p.id,
                "date": p.date,
                "type": p.interaction_type,
                "topics": p.topics
            })
        return json.dumps(results)
    finally:
        db.close()

class SearchMaterialsInput(BaseModel):
    topic: str = Field(description="The medical topic or product to search materials for")

@tool("search_materials", args_schema=SearchMaterialsInput, return_direct=False)
def search_materials(topic: str) -> str:
    """Searches the marketing materials repository for relevant brochures or PDFs based on a topic."""
    # Mock data
    materials = [
        {"id": 1, "name": "OncoBoost Phase III Trial Results.pdf", "topic": "Oncology"},
        {"id": 2, "name": "CardioPlus Efficacy Summary.pdf", "topic": "Cardiology"},
        {"id": 3, "name": "ImmunoShield Safety Guidelines.pdf", "topic": "Immunology"}
    ]
    results = [m["name"] for m in materials if topic.lower() in m["topic"].lower()]
    if results:
        return f"Found materials: {', '.join(results)}"
    return f"No specific materials found for topic: {topic}"

class ScheduleFollowUpInput(BaseModel):
    hcp_name: str = Field(description="Name of the HCP")
    reason: str = Field(description="Reason for follow up")
    timeframe: str = Field(description="When the follow up should happen (e.g., 'in 2 weeks')")

@tool("schedule_follow_up", args_schema=ScheduleFollowUpInput, return_direct=False)
def schedule_follow_up(hcp_name: str, reason: str, timeframe: str) -> str:
    """Schedules a follow-up action for a given HCP."""
    return f"Successfully scheduled a follow-up with {hcp_name} {timeframe} for: {reason}."

tools = [
    log_interaction,
    edit_interaction,
    get_past_interactions,
    search_materials,
    schedule_follow_up
]
