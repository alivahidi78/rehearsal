from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScenarioCharacterBase(BaseModel):
    character_id: int
    is_player: bool
    scene_knowledge: Optional[str] = None
    
class ScenarioCharacterInput(ScenarioCharacterBase):
    pass
    
class ScenarioCharacterRead(ScenarioCharacterBase):
    class Config:
        from_attributes = True
        
class ScenarioRelationshipBase(BaseModel):
    character_a_id: int
    character_b_id: int
    dynamic: Optional[str] = None
    a_knows_b: Optional[str] = None
    b_knows_a: Optional[str] = None

class ScenarioRelationshipInput(ScenarioRelationshipBase):
    pass

class ScenarioRelationshipRead(ScenarioRelationshipBase):
    id: int

    class Config:
        from_attributes = True
        
class ScenarioBase(BaseModel):
    title: str
    situation: str
    
class ScenarioCreate(ScenarioBase):
    characters: list[ScenarioCharacterInput]
    relationships: list[ScenarioRelationshipInput] = []

class ScenarioRead(ScenarioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    characters: list[ScenarioCharacterRead]
    relationships: list[ScenarioRelationshipRead]
    
    class Config:
        from_attributes = True