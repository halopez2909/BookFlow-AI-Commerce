import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PricingTable from '../src/components/pricing/PricingTable'
import type { PricingDecision } from '../src/utils/types'

const mockPrices: PricingDecision[] = [
  {
    id: 'pd-001',
    book_id: 'b1',
    title: 'Cien años de soledad',
    author: 'Gabriel García Márquez',
    condition: 'Bueno',
    suggested_price: 18500,
    currency: 'ARS',
    condition_factor: 1,
    reference_count: 3,
    sources: [{ name: 'MercadoLibre' }],
    explanation: 'test',
    status: 'suggested',
    updated_at: '2026-01-01T00:00:00Z',
  },
  {
    id: 'pd-002',
    book_id: 'b2',
    title: 'Rayuela',
    author: 'Julio Cortázar',
    condition: 'Muy bueno',
    suggested_price: 20000,
    manual_price: 24500,
    currency: 'ARS',
    condition_factor: 1.1,
    reference_count: 3,
    sources: [{ name: 'MercadoLibre' }],
    explanation: 'test',
    status: 'overridden',
    updated_at: '2026-01-01T00:00:00Z',
  },
]

describe('PricingTable', () => {
  it('renderiza una fila por cada precio', () => {
    render(
      <PricingTable
        prices={mockPrices}
        onRowClick={() => {}}
        onRecalculate={() => {}}
      />
    )
    expect(screen.getByText('Cien años de soledad')).toBeInTheDocument()
    expect(screen.getByText('Rayuela')).toBeInTheDocument()
  })

  it('muestra manual_price cuando existe, si no suggested_price', () => {
    render(
      <PricingTable
        prices={mockPrices}
        onRowClick={() => {}}
        onRecalculate={() => {}}
      />
    )
    expect(screen.getByText(/18\.?500/)).toBeInTheDocument()
    expect(screen.getByText(/24\.?500/)).toBeInTheDocument()
  })

  it('llama a onRowClick al hacer click en una fila', async () => {
    const onRowClick = vi.fn()
    const user = userEvent.setup()
    render(
      <PricingTable
        prices={mockPrices}
        onRowClick={onRowClick}
        onRecalculate={() => {}}
      />
    )
    const row = screen.getByText('Cien años de soledad').closest('tr')!
    await user.click(row)
    expect(onRowClick).toHaveBeenCalledWith(
      expect.objectContaining({ id: 'pd-001' })
    )
  })

  it('llama a onRecalculate sin disparar onRowClick', async () => {
    const onRowClick = vi.fn()
    const onRecalculate = vi.fn()
    const user = userEvent.setup()
    render(
      <PricingTable
        prices={mockPrices}
        onRowClick={onRowClick}
        onRecalculate={onRecalculate}
      />
    )
    const buttons = screen.getAllByRole('button', { name: /recalcular/i })
    await user.click(buttons[0])
    expect(onRecalculate).toHaveBeenCalledWith(
      expect.objectContaining({ id: 'pd-001' })
    )
    expect(onRowClick).not.toHaveBeenCalled()
  })
})