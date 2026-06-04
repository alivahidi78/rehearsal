import { useParams } from 'react-router-dom'
import { useState, useEffect, useRef } from 'react'
import { getSession, sendMessage, sendFeedback } from '../../api/sessions'
import type { MessageRead, SessionResponse } from '../../api/sessions'

import styles from './Session.module.css'

type InputMode = 'chat' | 'feedback'

function Session() {
    const { sessionId } = useParams<{ sessionId: string }>()
    const [messages, setMessages] = useState<MessageRead[]>([])
    const [lastResponse, setLastResponse] = useState<SessionResponse | null>(null)
    const [input, setInput] = useState('')
    const [mode, setMode] = useState<InputMode>('chat')
    const [loading, setLoading] = useState(true)
    const [sending, setSending] = useState(false)
    const narrativeEndRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (!sessionId) return
        getSession(sessionId)
            .then(state => {
                setMessages(state.messages)
                setLastResponse(state.last_response)
            })
            .finally(() => setLoading(false))
    }, [sessionId])

    useEffect(() => {
        narrativeEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    const handleSend = async () => {
        if (!input.trim() || !sessionId || sending) return
        setSending(true)

        if (mode === 'chat') {
            const response = await sendMessage(sessionId, input)
            setMessages(prev => [
                ...prev,
                { role: 'user', content: input },
                { role: 'assistant', content: response.narrative }
            ])
            setLastResponse(response)
        } else {
            await sendFeedback(sessionId, input)
        }

        setInput('')
        setSending(false)
    }

    if (loading) return <div>Loading...</div>

    return (
        <div className={styles.container}>
            
            {/* top panes */}
            <div className={styles.panes}>
                
                {/* narrative */}
                <div className={styles.narrative}>
                    {messages.map((msg, i) => (
                        <div key={i} style={{ marginBottom: '1rem' }}>
                            <strong>{msg.role === 'user' ? 'You' : 'Assistant'}</strong>
                            <p>{msg.content}</p>
                        </div>
                    ))}
                    <div ref={narrativeEndRef} />
                </div>

                {/* uncertainty */}
                <div className={styles.uncertainty}>
                    {lastResponse?.uncertainty && (
                        <div className={styles.uncertaintyBox}>
                            <strong>Uncertainty</strong>
                            <p>{lastResponse.uncertainty}</p>
                        </div>
                    )}
                </div>
            </div>

            {/* input area */}
            <div className={styles.inputArea}>
                <div className={styles.modeSelector}>
                    <label className={styles.radioLabel}>
                        <input
                            type="radio"
                            value="chat"
                            checked={mode === 'chat'}
                            onChange={() => setMode('chat')}
                        /> Chat
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="feedback"
                            checked={mode === 'feedback'}
                            onChange={() => setMode('feedback')}
                        /> Feedback
                    </label>
                </div>
                <div className={styles.inputRow}>
                    <textarea 
                        className={styles.textarea}
                        rows={3}
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        placeholder={mode === 'chat' ? 'What do you do?' : 'Give feedback...'}
                        onKeyDown={e => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault()
                                handleSend()
                            }
                        }}
                    />
                    <button
                        className={styles.sendButton}
                        onClick={handleSend}
                        disabled={sending || !input.trim()}
                    >
                        {sending ? '...' : 'Send'}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Session