import operator
from typing import TypedDict, Optional, Annotated
from app.schemas.session_internal import SessionScenario, LLMResponse, FeedbackResponse

class RehearsalState(TypedDict):
    messages: Annotated[list, operator.add]
    scenario: SessionScenario
    player_character_id: int
    last_response: Optional[LLMResponse]
    pending_feedback: Optional[str]
    last_feedback_response: Optional[FeedbackResponse]
    feedback_error: Optional[str]
    next_node: str