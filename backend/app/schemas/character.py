from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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


class CharacterRead(CharacterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True