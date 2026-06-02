from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.character import NoteCategory

class ScenarioCharSummary(BaseModel):
    scenario_id: int
    is_player: bool
    scene_knowledge: Optional[str] = None
    
    class Config: from_attributes = True

class BehavioralNoteRead(BaseModel):
    id: int
    created_at: datetime
    character_id: int
    category: NoteCategory
    content: str
    
    class Config:
        from_attributes = True
    
class CharacterBase(BaseModel):
    name: str
    age: Optional[int] = None
    appearance: Optional[str] = None
    personality: Optional[str] = None
    backstory: Optional[str] = None
    speech_patterns: Optional[str] = None
    motivations: Optional[str] = None
    fears: Optional[str] = None
    
class CharacterCreate(CharacterBase):
    pass

class CharacterSummary(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    
    class Config:
        from_attributes = True
        
class CharacterRead(CharacterBase, CharacterSummary):
    behavioral_notes: list[BehavioralNoteRead] = []
    scenario_characters: list[ScenarioCharSummary] = []
    
class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    appearance: Optional[str] = None
    personality: Optional[str] = None
    backstory: Optional[str] = None
    speech_patterns: Optional[str] = None
    motivations: Optional[str] = None
    fears: Optional[str] = None