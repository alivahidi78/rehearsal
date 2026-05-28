from app.models.base import Base, TimestampMixin
import enum
from sqlalchemy import Integer, String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import mapped_column, relationship

class NoteCategory(enum.Enum):
    personality = "personality"
    speech = "speech"
    behavior = "behavior"
    rule = "rule"

class Character(Base, TimestampMixin):
    __tablename__ = "characters"
    
    name = mapped_column(String(255), nullable=False)
    age = mapped_column(Integer, nullable=True)
    appearance = mapped_column(Text, nullable=True)
    personality = mapped_column(Text, nullable=True)
    backstory = mapped_column(Text, nullable=True)
    speech_patterns = mapped_column(Text, nullable=True)
    motivations = mapped_column(Text, nullable=True)
    fears = mapped_column(Text, nullable=True)

    behavioral_notes = relationship("BehavioralNote", back_populates="character")
    scenario_characters = relationship("ScenarioCharacter", back_populates="character")
    
class BehavioralNote(Base):
    __tablename__ = "behavioral_notes"
    created_at = mapped_column(DateTime, server_default=func.now())
    
    character_id = mapped_column(ForeignKey("characters.id"), nullable=False)
    category = mapped_column(SAEnum(NoteCategory), nullable=False)
    content = mapped_column(Text, nullable=False)
    
    character = relationship("Character", back_populates="behavioral_notes")
    
    