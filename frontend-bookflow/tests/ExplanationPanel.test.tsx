import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ExplanationPanel from '../src/components/pricing/ExplanationPanel'
import type { PricingDecision, PricingExplanation } from '../src/utils/types'

const baseDecision: PricingDecision = {
  id: 'pd-001',
  book_id: 'b1',
  title: 'Libro de prueba',
  author: 'Autor',
  condition: 'Bueno',
  suggested_price: 10000,
  currency: 'ARS',
  condition_factor: 1,
  reference_count: 3,
  sources: [],
  explanation: '',
  status: 'suggested',
  updated_at: '2026-01-01T00:00:00Z',
}

describe('ExplanationPanel', () => {
  it('renderiza un explanation tipo string como texto plano', () => {
    const decision: PricingDecision = {
      ...baseDecision,
      explanation: 'Precio sugerido por mediana de 3 fuentes.',
    }

    render(<ExplanationPanel decision={decision} />)
    expect(screen.getByText(/mediana de 3 fuentes/i)).toBeInTheDocument()
  })

  it('renderiza las secciones cuando explanation es estructurado', () => {
    const explanation: PricingExplanation = {
      summary: 'Se aplicó una rebaja por condición Aceptable',
      method: 'median-adjusted',
      factors: ['Condición del libro', 'Fuentes externas'],
      notes: 'Ajuste conservador',
    }
    const decision: PricingDecision = {
      ...baseDecision,
      explanation,
      sources: [{ name: 'MercadoLibre' }, { name: 'Cuspide' }],
    }

    render(<ExplanationPanel decision={decision} />)
    expect(screen.getByText(/rebaja por condición/i)).toBeInTheDocument()
    expect(screen.getByText(/median-adjusted/i)).toBeInTheDocument()
    expect(screen.getByText(/Condición del libro/i)).toBeInTheDocument()
    expect(screen.getByText(/MercadoLibre/i)).toBeInTheDocument()
  })
})