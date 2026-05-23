window.HTMLElement.prototype.scrollIntoView = () => {}

import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'

vi.mock('../hooks/useAssistant', () => ({
  useAssistant: () => ({
    messages: [
      { role: 'user', content: 'Cuanto cuesta Don Quixote' },
      { role: 'assistant', content: 'El precio de Don Quixote es 25,200 COP', sources: ['catalog', 'pricing'] },
    ],
    isLoading: false,
    sendMessage: vi.fn(),
  }),
}))

import AssistantPage from '../pages/assistant/AssistantPage'

describe('AssistantPage', () => {
  it('renderiza el titulo del asistente', () => {
    render(<AssistantPage />)
    expect(screen.getByText(/Asistente BookFlow/i)).toBeDefined()
  })

  it('muestra mensajes del chat', () => {
    render(<AssistantPage />)
    expect(screen.getByText('Cuanto cuesta Don Quixote')).toBeDefined()
    expect(screen.getByText(/25,200 COP/)).toBeDefined()
  })

  it('tiene input para escribir pregunta', () => {
    render(<AssistantPage />)
    expect(screen.getByPlaceholderText(/Don Quixote/i)).toBeDefined()
  })

  it('tiene boton enviar', () => {
    render(<AssistantPage />)
    expect(screen.getByText('Enviar')).toBeDefined()
  })
})
