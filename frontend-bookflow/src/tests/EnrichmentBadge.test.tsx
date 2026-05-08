import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import EnrichmentBadge from '../components/catalog/EnrichmentBadge'

describe('EnrichmentBadge', () => {
  it('muestra badge Enriquecido cuando isEnriched es true', () => {
    render(<EnrichmentBadge isEnriched={true} />)
    expect(screen.getByText(/Enriquecido/i)).toBeDefined()
  })

  it('muestra badge Basico cuando isEnriched es false', () => {
    render(<EnrichmentBadge isEnriched={false} />)
    expect(screen.getByText(/Basico/i)).toBeDefined()
  })
})
