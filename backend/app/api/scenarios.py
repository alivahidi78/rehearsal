from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.scenario import Scenario, ScenarioCharacter, ScenarioRelationship
from app.schemas.scenario import ScenarioRead, ScenarioCreate

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

@router.get("/", response_model=list[ScenarioRead])
def get_all_scenarios(db: Session = Depends(get_db)):
    return db.query(Scenario).all()

@router.get("/{scenario_id}", response_model=ScenarioRead)
def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    return db.query(Scenario).filter(Scenario.id == scenario_id).first()

@router.post("/", response_model=ScenarioRead)
def create_scenario(scenario: ScenarioCreate, db: Session = Depends(get_db)):
    db_scenario = Scenario(**scenario.model_dump(exclude={"characters", "relationships"}))
    
    db.add(db_scenario)
    db.flush()  # writes to db without committing, generates the id
    
    for char_input in scenario.characters:
        db_sc = ScenarioCharacter(**char_input.model_dump(), scenario_id= db_scenario.id)
        db.add(db_sc)
        
    for rel_input in scenario.relationships:
        db_rel = ScenarioRelationship(**rel_input.model_dump(), scenario_id=db_scenario.id)
        db.add(db_rel)
    
    db.commit()  
    db.refresh(db_scenario)
    return db_scenario