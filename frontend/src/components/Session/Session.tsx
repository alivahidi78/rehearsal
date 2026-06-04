import { useParams } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { getSession, type MessageRead } from '../../api/sessions'

function Session() {
    const { sessionId } = useParams<{ sessionId: string }>()
    const [messages, setMessages] = useState<MessageRead[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (!sessionId) return
        getSession(sessionId)
            .then(state => {
                setMessages(state.messages)
            })
            .finally(() => setLoading(false))
    }, [sessionId])

    if (loading) return <div>Loading...</div>

    return (
        <div>
            {messages.map((msg, i) => (
                <div key={i}>
                    <strong>{msg.role}</strong>: {msg.content}
                </div>
            ))}
        </div>
    )
}

export default Session