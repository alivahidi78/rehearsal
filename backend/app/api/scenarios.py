from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.scenario import Scenario, ScenarioCharacter, ScenarioRelationship
from app.schemas.scenario import ScenarioRead, ScenarioCreate, ScenarioSummary, ScenarioUpdate

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

@router.get("/", response_model=list[ScenarioSummary])
def get_all_scenarios(db: Session = Depends(get_db)):
    return db.query(Scenario).all()

@router.get("/{scenario_id}", response_model=ScenarioRead)
def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(404, "Scenario not found")
    
    return scenario

@router.post("/", response_model=ScenarioRead)
def create_scenario(scenario: ScenarioCreate, db: Session = Depends(get_db)):
    db_scenario = Scenario(**scenario.model_dump(exclude={"scenario_characters", "scenario_relationships"}))
    
    db.add(db_scenario)
    db.flush()  # writes to db without committing, generates the id
    
    for char_input in scenario.scenario_characters:
        db_sc = ScenarioCharacter(**char_input.model_dump(), scenario_id= db_scenario.id)
        db.add(db_sc)
        
    for rel_input in scenario.scenario_relationships:
        db_rel = ScenarioRelationship(**rel_input.model_dump(), scenario_id=db_scenario.id)
        db.add(db_rel)
    
    db.commit()  
    db.refresh(db_scenario)
    return db_scenario

@router.delete("/{scenario_id}", status_code=204)
def delete_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(404, "Scenario not found")    
    
    db.delete(scenario)
    db.commit()
    
@router.patch("/{scenario_id}", response_model=ScenarioRead)
def update_scenario(scenario_id: int, updates: ScenarioUpdate, db: Session = Depends(get_db)):
    # TODO be able to update characters and relationships in the scenario as well
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(404, "Scenario not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(scenario, field, value)
    db.commit()
    db.refresh(scenario)
    return scenario