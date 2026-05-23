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
vi.mock('../hooks/useCart', () => ({
  useCart: () => ({ data: null, isLoading: false }),
  useUpdateCartItem: () => ({ mutate: vi.fn() }),
  useRemoveCartItem: () => ({ mutate: vi.fn() }),
  useClearCart: () => ({ mutate: vi.fn() }),
}))
vi.mock('../hooks/useOrders', () => ({
  useCreateOrder: () => ({ mutateAsync: vi.fn() }),
}))

import CartPage from '../pages/cart/CartPage'

describe('CartPage', () => {
  it('renderiza la pagina del carrito', () => {
    render(<CartPage />)
    expect(document.body).toBeDefined()
  })

  it('muestra mensaje cuando no esta autenticado', () => {
    render(<CartPage />)
    expect(screen.getAllByText(/Iniciar sesi/i).length).toBeGreaterThan(0)
  })
})
