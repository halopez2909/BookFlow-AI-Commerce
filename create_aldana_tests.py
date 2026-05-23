import os

os.makedirs("frontend-bookflow/src/tests", exist_ok=True)

cart_test = """import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'

vi.mock('../../hooks/useCart', () => ({
  useCart: () => ({ data: {
    id: 1, customer_id: 'customer-001', status: 'active',
    items: [{ id: 1, book_id: 'REF-GATSBY', quantity: 2, unit_price: 18900, subtotal: 37800 }],
    total: 37800
  }, isLoading: false }),
  useUpdateCartItem: () => ({ mutate: vi.fn() }),
  useRemoveCartItem: () => ({ mutate: vi.fn() }),
  useClearCart: () => ({ mutate: vi.fn() }),
}))
vi.mock('../../hooks/useOrders', () => ({ useCreateOrder: () => ({ mutateAsync: vi.fn() }) }))
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
}))
vi.mock('../../context/AuthContext', () => ({
  AuthContext: React.createContext({ state: { isAuthenticated: true, user: { email: 'test@test.com' } }, dispatch: vi.fn() }),
}))

import CartPage from '../../pages/cart/CartPage'

describe('CartPage', () => {
  it('renderiza items del carrito', () => {
    render(<CartPage />)
    expect(screen.getByText('Mi Carrito')).toBeDefined()
    expect(screen.getByText('REF-GATSBY')).toBeDefined()
  })

  it('muestra el total del carrito', () => {
    render(<CartPage />)
    expect(screen.getByText(/85.500|37.800/)).toBeDefined()
  })

  it('muestra boton confirmar pedido', () => {
    render(<CartPage />)
    expect(screen.getByText(/Confirmar Pedido/i)).toBeDefined()
  })
})
"""

orders_test = """import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'

vi.mock('../../hooks/useOrders', () => ({
  useOrders: () => ({ data: [
    { id: 'order-001', status: 'pending', total_amount: 18900, created_at: '2026-05-19T00:00:00', items: [] },
    { id: 'order-002', status: 'delivered', total_amount: 45000, created_at: '2026-05-18T00:00:00', items: [] },
  ], isLoading: false, refetch: vi.fn() }),
}))
vi.mock('react-router-dom', () => ({ useNavigate: () => vi.fn() }))
vi.mock('../../context/AuthContext', () => ({
  AuthContext: React.createContext({ state: { isAuthenticated: true, user: { email: 'test@test.com' } }, dispatch: vi.fn() }),
}))
vi.mock('../../services/apiClient', () => ({ default: { put: vi.fn() } }))

import OrdersPage from '../../pages/orders/OrdersPage'

describe('OrdersPage', () => {
  it('renderiza historial de pedidos', () => {
    render(<OrdersPage />)
    expect(screen.getByText('Mis Pedidos')).toBeDefined()
  })

  it('muestra estado de cada pedido', () => {
    render(<OrdersPage />)
    expect(screen.getByText('pending')).toBeDefined()
    expect(screen.getByText('delivered')).toBeDefined()
  })

  it('muestra total de cada pedido', () => {
    render(<OrdersPage />)
    expect(screen.getByText(/18.900/)).toBeDefined()
    expect(screen.getByText(/45.000/)).toBeDefined()
  })
})
"""

assistant_test = """import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import React from 'react'

vi.mock('../../hooks/useAssistant', () => ({
  useAssistant: () => ({
    messages: [
      { role: 'user', content: 'Cuanto cuesta Don Quixote' },
      { role: 'assistant', content: 'El precio de Don Quixote es 25,200 COP', sources: ['catalog', 'pricing'] },
    ],
    isLoading: false,
    sendMessage: vi.fn(),
  }),
}))

import AssistantPage from '../../pages/assistant/AssistantPage'

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

  it('muestra fuentes del asistente', () => {
    render(<AssistantPage />)
    expect(screen.getByText(/catalog, pricing/i)).toBeDefined()
  })

  it('tiene input para escribir pregunta', () => {
    render(<AssistantPage />)
    expect(screen.getByPlaceholderText(/Cuánto cuesta Don Quixote/i)).toBeDefined()
  })

  it('tiene boton enviar', () => {
    render(<AssistantPage />)
    expect(screen.getByText('Enviar')).toBeDefined()
  })
})
"""

with open("frontend-bookflow/src/tests/CartPage.test.tsx", "w", encoding="utf-8") as f:
    f.write(cart_test)
with open("frontend-bookflow/src/tests/OrdersPage.test.tsx", "w", encoding="utf-8") as f:
    f.write(orders_test)
with open("frontend-bookflow/src/tests/AssistantPage.test.tsx", "w", encoding="utf-8") as f:
    f.write(assistant_test)
print("Tests creados!")
