const BASE_URL = import.meta.env.VITE_API_URL

export interface SessionResponse {
    session_id: string
    narrative: string
    uncertainty: string | null
    await_input: boolean
}

export interface FeedbackResponse {
    session_id: string
    success: boolean
    error: string | null
}

export interface MessageRead {
    role: string
    content: string
}

export interface SessionStateResponse {
    messages: MessageRead[]
    last_response: SessionResponse | null
}

export async function getSession(session_id: string): Promise<SessionStateResponse> {
    const response = await fetch(`${BASE_URL}/sessions/${session_id}`)
    return response.json()
}

export async function startSession(scenario_id: number): Promise<SessionResponse> {
    const response = await fetch(`${BASE_URL}/sessions/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario_id })
    })
    return response.json()
}

export async function sendMessage(session_id: string, content: string): Promise<SessionResponse> {
    const response = await fetch(`${BASE_URL}/sessions/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id, content })
    })
    return response.json()
}

export async function sendFeedback(session_id: string, content: string): Promise<FeedbackResponse> {
    const response = await fetch(`${BASE_URL}/sessions/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id, content })
    })
    return response.json()
}