from typing import Optional
from pydantic import BaseModel
from app.schemas.character import BehavioralNoteRead
from app.schemas.scenario import ScenarioRelationshipRead
from app.models.character import NoteCategory

#TODO delete sessions. Retrieve all sessions

class SessionCharacter(BaseModel):
    id: int
    name: str
    appearance: Optional[str] = None
    personality: Optional[str] = None
    backstory: Optional[str] = None
    speech_patterns: Optional[str] = None
    motivations: Optional[str] = None
    fears: Optional[str] = None
    behavioral_notes: list[BehavioralNoteRead] = []
    is_player: bool
    scene_knowledge: Optional[str] = None

class SessionScenario(BaseModel):
    situation: str
    characters: list[SessionCharacter]
    relationships: list[ScenarioRelationshipRead] = []
    
class LLMResponse(BaseModel):
    narrative: str
    uncertainty: Optional[str] = None
    await_input: bool

class FeedbackResponse(BaseModel):
    character_id: int
    category: NoteCategory
    content: str