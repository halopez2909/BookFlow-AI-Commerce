import React, { useState, useRef, useEffect } from 'react'
import { useAssistant } from '../../hooks/useAssistant'

const SESSION_ID = 'session-' + Math.random().toString(36).slice(2, 9)
const SUGGESTIONS = [
  '¿Cuánto cuesta Don Quixote?',
  '¿Está disponible 1984?',
  'Libros de George Orwell',
  'Cuéntame sobre The Great Gatsby',
]

export default function AssistantPage() {
  const { messages, isLoading, sendMessage } = useAssistant(SESSION_ID)
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  async function handleSend() {
    if (!input.trim() || isLoading) return
    const q = input.trim(); setInput('')
    await sendMessage(q)
    inputRef.current?.focus()
  }

  return (
    <div className="page fade-up" style={{ maxWidth: 860 }}>
      <div className="page-header">
        <h1>Asistente <em style={{ fontStyle: 'italic', color: 'var(--accent)' }}>BookFlow</em></h1>
        <p>Consulta precios, disponibilidad y descripción de cualquier título</p>
      </div>
      <div className="assistant-container" style={{ height: 'calc(100vh - 360px)', minHeight: 420 }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: 28, display: 'flex', flexDirection: 'column', gap: 16 }}>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', padding: '48px 24px', color: 'var(--text-3)' }}>
              <div style={{ fontSize: 40, marginBottom: 16, opacity: 0.2, fontFamily: 'var(--font-display)', fontStyle: 'italic' }}>◎</div>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: 22, color: 'var(--text-2)', fontWeight: 300, marginBottom: 8 }}>¿En qué puedo ayudarte?</p>
              <p style={{ fontSize: 13, marginBottom: 28, letterSpacing: '0.04em' }}>Pregunta sobre precios, disponibilidad o descripción</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' }}>
                {SUGGESTIONS.map(s => (
                  <button key={s} className="btn btn-ghost btn-sm" onClick={() => { setInput(s); inputRef.current?.focus(); }}
                    style={{ textTransform: 'none', letterSpacing: '0.02em', fontSize: 12 }}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
              <div className={`message-bubble ${msg.role === 'user' ? 'message-user' : 'message-assistant'}`}>
                {msg.content}
              </div>
              {msg.sources && msg.sources.length > 0 && (
                <div className="message-sources" style={{ marginLeft: msg.role === 'assistant' ? 4 : 0 }}>
                  Fuentes: {msg.sources.join(', ')}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div style={{ display: 'flex' }}>
              <div className="message-bubble message-assistant" style={{ padding: 0 }}>
                <div className="thinking-dots">
                  <div className="thinking-dot" /><div className="thinking-dot" /><div className="thinking-dot" />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
        <div style={{ padding: '16px 24px', borderTop: '1px solid var(--border)', display: 'flex', gap: 10, background: 'var(--bg-2)' }}>
          <input ref={inputRef} type="text" value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="¿Cuánto cuesta Don Quixote?" style={{ flex: 1 }} disabled={isLoading} />
          <button className="btn btn-primary" onClick={handleSend} disabled={isLoading || !input.trim()} style={{ flexShrink: 0 }}>
            Enviar
          </button>
        </div>
      </div>
    </div>
  )
}
