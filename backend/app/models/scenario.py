from app.models.base import Base, TimestampMixin
import enum
from sqlalchemy import Integer, String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import mapped_column, relationship

class Scenario(Base, TimestampMixin):
    __tablename__ = "scenarios"

    title = mapped_column(String(255), nullable=False)
    situation = mapped_column(Text, nullable=False)
    
    scenario_characters = relationship("ScenarioCharacter", back_populates="scenario", cascade="all, delete-orphan")
    scenario_relationships = relationship("ScenarioRelationship", back_populates="scenario", cascade="all, delete-orphan")  

class ScenarioCharacter(Base):
    __tablename__ = "scenario_characters"
    
    # TODO only one character can be player in each scenario
    is_player = mapped_column(Boolean, nullable=False)
    scenario_id = mapped_column(ForeignKey("scenarios.id"), nullable=False)
    character_id = mapped_column(ForeignKey("characters.id"), nullable=False)
    scene_knowledge = mapped_column(Text, nullable=True)
    
    scenario = relationship("Scenario", back_populates="scenario_characters")
    character = relationship("Character", back_populates="scenario_characters")
    
class ScenarioRelationship(Base):
    __tablename__ = "scenario_relationships"
    
    scenario_id = mapped_column(ForeignKey("scenarios.id"), nullable=False)
    character_a_id = mapped_column(ForeignKey("characters.id"), nullable=False)
    character_b_id = mapped_column(ForeignKey("characters.id"), nullable=False)
    
    a_knows_b = mapped_column(Text, nullable=True)   
    b_knows_a = mapped_column(Text, nullable=True)   
    dynamic = mapped_column(Text, nullable=True)  
    
    scenario = relationship("Scenario", back_populates="scenario_relationships")
    character_a = relationship("Character", foreign_keys=[character_a_id])
    character_b = relationship("Character", foreign_keys=[character_b_id])
    
    
    