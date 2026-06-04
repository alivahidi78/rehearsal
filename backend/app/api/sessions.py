import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.schemas.session_api import StartSessionRequest, MessageRequest, FeedbackRequest, SessionResponse, FeedbackSessionResponse, SessionStateResponse

from app.graph.graph import rehearsal_graph
from app.graph.state import RehearsalState
from app.schemas.session_internal import SessionScenario, SessionCharacter
from app.models.scenario import Scenario
from app.models.character import Character, BehavioralNote
from app.config import settings

# TODO get all sessions/ get all session messages/ delete session/ etc.

# TODO add streaming LLM responses instead of waiting for the full response
router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/{session_id}", response_model=SessionStateResponse)
def get_session(session_id: str):
    config = {"configurable": {"thread_id": session_id}}
    state = rehearsal_graph.get_state(config) # type: ignore
    if not state.values:
        raise HTTPException(status_code=404, detail="Session not found")
    return state.values

@router.post("/start", response_model=SessionResponse)
def start_session(request: StartSessionRequest,  db: Session = Depends(get_db)):
    # TODO check if player character exists in the scenario
    scenario = db.query(Scenario).options(
        joinedload(Scenario.scenario_characters),
        joinedload(Scenario.scenario_relationships)
    ).filter(Scenario.id == request.scenario_id).first()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    player_sc = next((sc for sc in scenario.scenario_characters if sc.is_player), None)
    if not player_sc:
        raise HTTPException(status_code=400, detail="No player character set for this scenario")
    
    # load and assemble session characters
    session_characters = []
    for sc in scenario.scenario_characters:
        character = db.query(Character).options(
            joinedload(Character.behavioral_notes)
        ).filter(Character.id == sc.character_id).first()
        
        if not character:
            raise HTTPException(status_code=404, detail=f"Character id={sc.character_id} not found")
        
        session_characters.append(SessionCharacter(
            id = character.id,
            name=character.name,
            appearance=character.appearance,
            backstory=character.backstory,
            personality=character.personality,
            speech_patterns=character.speech_patterns,
            motivations=character.motivations,
            fears=character.fears,
            behavioral_notes=character.behavioral_notes,
            is_player=sc.is_player,
            scene_knowledge=sc.scene_knowledge
        ))
    
    # build session scenario
    session_scenario = SessionScenario(
        situation=scenario.situation,
        characters=session_characters,
        relationships=scenario.scenario_relationships
    )
    
    # generate session id
    session_id = str(uuid.uuid4())
    
    # build initial state
    initial_state = RehearsalState(
        messages=[],
        scenario=session_scenario,
        player_character_id=player_sc.character_id,
        last_response=None,
        pending_feedback=None,
        last_feedback_response=None,
        feedback_error=None,
        next_node="generate_response"
    )
    
    # invoke graph
    config = {"configurable": {"thread_id": session_id}}
    result = rehearsal_graph.invoke(initial_state, config=config) # type: ignore
    
    return SessionResponse(
        session_id=session_id,
        narrative=result["last_response"].narrative,
        uncertainty=result["last_response"].uncertainty,
        await_input=result["last_response"].await_input
    )

@router.post("/message", response_model=SessionResponse)
def send_message(request: MessageRequest, db: Session = Depends(get_db)):
    config = {"configurable": {"thread_id": request.session_id}}
    
    result = rehearsal_graph.invoke(
        {
            "messages": [{"role": "user", "content": request.content}],
            "next_node": "generate_response"
        }, # type: ignore
        config=config # type: ignore
    ) 
    
    return SessionResponse(
        session_id=request.session_id,
        narrative=result["last_response"].narrative,
        uncertainty=result["last_response"].uncertainty,
        await_input=result["last_response"].await_input
    )

@router.post("/feedback", response_model=FeedbackSessionResponse)
def send_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    # TODO return refined feedback for the user to verify
    config = {"configurable": {"thread_id": feedback.session_id}}
    
    result = rehearsal_graph.invoke(
        {
            "pending_feedback": feedback.content,
            "next_node": "process_feedback"
        }, # type: ignore
        config=config # type: ignore
    )
    
    feedback_response = result.get("last_feedback_response")
    
    ############################################################################
    # This doesn't belong here. TODO clean it up
    if feedback_response and not result.get("feedback_error"):
        note = BehavioralNote(
            character_id=feedback_response.character_id,
            category=feedback_response.category,
            content=feedback_response.content
        )
        db.add(note)
        db.commit()
    ############################################################################
    
    return FeedbackSessionResponse(
        session_id=feedback.session_id,
        success=feedback_response is not None,
        error=result.get("feedback_error")
    )
    
@router.get("/debug/{session_id}")
def get_session_state(session_id: str):
    config = {"configurable": {"thread_id": session_id}}
    state = rehearsal_graph.get_state(config) # type: ignore
    return state.values
    
    
