from typing import Optional
from pydantic import BaseModel

class StartSessionRequest(BaseModel):
    scenario_id: int
    player_character_id: int

class MessageRequest(BaseModel):
    session_id: str
    content: str

class FeedbackRequest(BaseModel):
    session_id: str
    content: str

class SessionResponse(BaseModel):
    session_id: str
    narrative: str
    uncertainty: Optional[str] = None
    await_input: bool
    
class FeedbackSessionResponse(BaseModel):
    session_id: str
    success: bool
    error: Optional[str] = None