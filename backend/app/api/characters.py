from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterRead

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/", response_model=list[CharacterRead])
def get_all_characters(db: Session = Depends(get_db)):
    return db.query(Character).all()

@router.get("/{character_id}", response_model=CharacterRead)
def get_character(character_id: int, db: Session = Depends(get_db)):
    return db.query(Character).filter(Character.id == character_id).first()

@router.post("/", response_model=CharacterRead)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    db_character = Character(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character