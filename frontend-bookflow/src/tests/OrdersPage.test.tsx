import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'

vi.mock('react-router-dom', () => ({ useNavigate: () => vi.fn() }))
vi.mock('../context/AuthContext', () => ({
  AuthContext: React.createContext({
    state: { isAuthenticated: false, user: null },
    dispatch: vi.fn()
  }),
}))
vi.mock('../hooks/useOrders', () => ({
  useOrders: () => ({ data: [], isLoading: false, refetch: vi.fn() }),
}))
vi.mock('../services/apiClient', () => ({ default: { put: vi.fn() } }))

import OrdersPage from '../pages/orders/OrdersPage'

describe('OrdersPage', () => {
  it('renderiza la pagina de pedidos', () => {
    render(<OrdersPage />)
    expect(document.body).toBeDefined()
  })

  it('muestra mensaje cuando no esta autenticado', () => {
    render(<OrdersPage />)
    expect(screen.getAllByText(/Iniciar sesi/i).length).toBeGreaterThan(0)
  })
})
