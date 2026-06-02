from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.character import Character
from app.models.scenario import ScenarioCharacter
from app.schemas.character import CharacterCreate, CharacterRead, CharacterSummary, CharacterUpdate

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/", response_model=list[CharacterSummary])
def get_all_characters(db: Session = Depends(get_db)):
    return db.query(Character).all()

@router.get("/{character_id}", response_model=CharacterRead)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.post("/", response_model=CharacterRead)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    db_character = Character(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@router.delete("/{character_id}", status_code=204)
def delete_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    in_scenarios = db.query(ScenarioCharacter).filter(ScenarioCharacter.character_id == character_id).first()
    if in_scenarios:
        raise HTTPException(status_code=409, detail="Character is used in one or more scenarios. Remove them from those scenarios first.")
    
    db.delete(character)
    db.commit()
    
@router.patch("/{character_id}", response_model=CharacterRead)
def update_character(character_id: int, updates: CharacterUpdate, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(character, field, value)
    db.commit()
    db.refresh(character)
    return character