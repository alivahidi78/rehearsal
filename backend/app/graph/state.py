from typing import TypedDict, Optional
from app.schemas.session import SessionScenario, LLMResponse

class RehearsalState(TypedDict):
    messages: list[dict]
    scenario: SessionScenario
    player_character_id: int
    last_response: LLMResponse
    pending_feedback: Optional[str]