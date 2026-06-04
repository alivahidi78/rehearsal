from typing import Optional
from pydantic import BaseModel
from app.schemas.session_internal import LLMResponse

class StartSessionRequest(BaseModel):
    scenario_id: int

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
    
class MessageRead(BaseModel):
    role: str
    content: str

class SessionStateResponse(BaseModel):
    messages: list[MessageRead]
    last_response: Optional[LLMResponse] = None