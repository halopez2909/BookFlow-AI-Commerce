import { useState } from 'react'
import api from '../services/apiClient'

export type Message = {
  role: 'user' | 'assistant'
  content: string
  intent?: string
  sources?: string[]
}

export function useAssistant(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  async function sendMessage(question: string) {
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setIsLoading(true)
    try {
      const { data } = await api.post('/api/assistant/query', {
        session_id: sessionId,
        question,
      })
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        intent: data.intent,
        sources: data.sources,
      }])
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Lo siento, no pude procesar tu pregunta. Intenta de nuevo.',
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return { messages, isLoading, sendMessage }
}
