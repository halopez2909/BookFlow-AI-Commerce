import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import PriceSummary from '../components/catalog/PriceSummary'

describe('PriceSummary', () => {
  it('muestra el precio cuando existe', () => {
    render(<PriceSummary suggestedPrice={25200} />)
    expect(screen.getByText(/25.200/)).toBeDefined()
  })

  it('muestra Precio no disponible cuando es null', () => {
    render(<PriceSummary suggestedPrice={null} />)
    expect(screen.getByText(/Precio no disponible/i)).toBeDefined()
  })

  it('muestra Precio no disponible cuando es undefined', () => {
    render(<PriceSummary />)
    expect(screen.getByText(/Precio no disponible/i)).toBeDefined()
  })
})
