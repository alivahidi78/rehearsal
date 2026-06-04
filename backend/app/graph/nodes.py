from app.schemas.session_internal import LLMResponse, FeedbackResponse
from app.models.character import NoteCategory
from app.graph.state import RehearsalState
from app.config import client, settings

# TODO add default user commands for the way story progresses

def mock_llm_response() -> LLMResponse:
    return LLMResponse(
        narrative="John looks up as Alice enter the room, his expression unreadable.",
        uncertainty="I am not sure who John is meant to be.",
        await_input=True
    )
    
def llm_call(system: str, messages: list) -> LLMResponse:
    response = client.messages.create(
        model= "claude-sonnet-4-6",
        max_tokens= 1024,
        system= system,
        messages= messages, # type: ignore
        tools= [{
            "name": "scene_response",
            "description": "Always use this to respond",
            "input_schema": LLMResponse.model_json_schema()
            }],
        tool_choice= {"type": "tool", "name": "scene_response"}
    )
    # filter so only the data inside the tool use block is displayed.
    tool_use = next(block for block in response.content if block.type == "tool_use")
    return LLMResponse(**tool_use.input) # type: ignore

def build_roleplay_prompt(state: RehearsalState) -> str:
    # TODO move the prompts to a json file
    # TODO consider relationships as well
    sc = state["scenario"]
    
    situation_desc = f"Scenario:\n {sc.situation}\n"
    
    characters_desc = "Characters:\n"
    for i, char in enumerate(sc.characters):
        characters_desc += "".join([
            f"{i + 1}.\nName: {char.name}",
            "(user's character)\n" if char.is_player else "\n",
            f"Appearance: {char.appearance}\n" if char.appearance else "",
            f"Backstory: {char.backstory}\n" if char.backstory else "",
            f"Personality: {char.personality}\n" if char.personality else "",
            f"Speech Patterns: {char.speech_patterns}\n" if char.speech_patterns else "",
            f"Motivations: {char.motivations}\n" if char.motivations else "",
            f"Fears: {char.fears}\n" if char.fears else "",
            f"Scene Knowledge: {char.scene_knowledge}\n" if char.scene_knowledge else "",
        ])
        if char.behavioral_notes:
            characters_desc += ("Additional Notes (These notes override whatever is "
                                "described beforehand whenever something is "
                                "contradictory): \n")
            for j, note in enumerate(char.behavioral_notes):
                characters_desc += f"Note {j + 1} (on {note.category}): {note.content}\n"         
        
    prompt = (
        "You are a story-telling assistant. You will consider a specific scenario "
        "involving a list of pre-defined characters. One of these characters will "
        "be role-played by the user. You are to first set the stage by describing "
        "the environment, the situation, and the people in a natural story-like "
        "fashion without being overly expository. Depending on the specific "
        "scenario and the specific characters, others may act or speak before the "
        "user's character, or they may wait for the user to act or speak first. "
        "Describe the situation and role-play as non-user characters up until the " 
        "point where the user is meant to act, then stop the story and wait for the " 
        "user to continue their turn. After receiving the reply, resume the scene "
        "continuing after the user's action.\n" 
        "NEVER use first person, or second person pronouns.\n"
        "You must ALWAYS respond with a JSON object in exactly this format:\n"
        "{\n"
        '    "narrative": "<the story text>",\n'
        '    "uncertainty": "<what you were unsure about, or null if none>",\n'
        '    "await_input": <true if waiting for user, false if scene is still unfolding>\n'
        "}\n"
        "Never include anything outside the JSON object.\n"
        "If you are uncertain how a character would behave in a situation because "
        "their profile does not cover it, still make a choice but explain your "
        "uncertainty in the right output section")
    
    prompt += situation_desc + characters_desc
    
    return prompt  

def generate_response(state: RehearsalState) -> dict:
    prompt = build_roleplay_prompt(state)
    
    try:
        if settings.use_mock_llm:
            llm_response = mock_llm_response()
        else:
            llm_response = llm_call(prompt, state["messages"])
    except Exception as e:
        return {
            "messages": [],
            "last_response": LLMResponse(
                narrative="Something went wrong, please try again.",
                uncertainty=str(e) if settings.debug else "An error occurred.",
                await_input=True)
            }
        
    
    return {
        "messages": [{"role": "assistant", "content": llm_response.narrative}],
        "last_response": llm_response
    }

def build_feedback_prompt(state: RehearsalState, feedback: str) -> str:
    sc = state["scenario"]
    
    characters_desc = "Characters in this scene:\n"
    for char in sc.characters:
        characters_desc += f"- {char.name} (id: {char.id})\n"
    
    conversation_history = ""
    if state["messages"]:
        for m in state["messages"]:
            role = "Writer" if m["role"] == "user" else "Scene"
            conversation_history += f"{role}: {m['content']}\n"
    
    prompt = (
        "You are helping a writer refine their characters. "
        "You will receive a correction about how a character behaved incorrectly in a scene. "
        "Extract the key insight and return it as a structured note about that character.\n\n"
        f"{characters_desc}\n"
        f"Conversation so far:\n{conversation_history}\n"
        f"Writer's feedback: {feedback}\n\n"
        "Return the character_id this feedback applies to, the category, and a clean "
        "concise note rewritten as a third-person observation about the character."
    )
    
    return prompt

def process_feedback(state: RehearsalState) -> dict:
    error = False
    error_description = None
    feedback = state["pending_feedback"]
    prompt = build_feedback_prompt(state, feedback) # type: ignore
    
    try:
        if settings.use_mock_llm:
            feedback_response = FeedbackResponse(
                character_id=1,
                category=NoteCategory.behavior,
                content="Mock note: character would not behave this way."
            )
        else:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=512,
                system=prompt,
                messages=[{"role": "user", "content": feedback}], # type: ignore
                tools=[{
                    "name": "feedback_response",
                    "description": "Always use this to respond",
                    "input_schema": FeedbackResponse.model_json_schema()
                }],
                tool_choice={"type": "tool", "name": "feedback_response"}
            )
            tool_use = next(block for block in response.content if block.type == "tool_use")
            feedback_response = FeedbackResponse(**tool_use.input)  # type: ignore
            
    except Exception as e:
        error = True
        error_description = str(e)
        feedback_response = None

    return {
        "pending_feedback": None,
        "last_feedback_response": feedback_response,
        "feedback_error": error_description if error and settings.debug else None
    }