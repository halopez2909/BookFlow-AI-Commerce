import os

BASE = "frontend-bookflow/src"

files = {}

# ── useCart hook ──────────────────────────────────────────────────────
files["hooks/useCart.ts"] = """import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/apiClient'

export type CartItem = {
  id: number
  book_id: string
  quantity: number
  unit_price: number
  subtotal: number
}

export type Cart = {
  id: number
  customer_id: string
  status: string
  items: CartItem[]
  total: number
}

export function useCart(customerId: string) {
  return useQuery<Cart>({
    queryKey: ['cart', customerId],
    queryFn: async () => {
      const { data } = await api.get(`/api/cart/${customerId}`)
      return data
    },
    enabled: !!customerId,
    retry: 1,
    staleTime: 1000 * 30,
  })
}

export function useAddToCart() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (payload: { customer_id: string; book_id: string; quantity: number }) => {
      const { data } = await api.post('/api/cart/items', payload)
      return data
    },
    onSuccess: (_, variables) => {
      qc.invalidateQueries({ queryKey: ['cart', variables.customer_id] })
    },
  })
}

export function useUpdateCartItem() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ itemId, quantity, customerId }: { itemId: number; quantity: number; customerId: string }) => {
      const { data } = await api.put(`/api/cart/items/${itemId}`, { quantity })
      return { data, customerId }
    },
    onSuccess: (result) => {
      qc.invalidateQueries({ queryKey: ['cart', result.customerId] })
    },
  })
}

export function useRemoveCartItem() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ itemId, customerId }: { itemId: number; customerId: string }) => {
      const { data } = await api.delete(`/api/cart/items/${itemId}`)
      return { data, customerId }
    },
    onSuccess: (result) => {
      qc.invalidateQueries({ queryKey: ['cart', result.customerId] })
    },
  })
}

export function useClearCart() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (customerId: string) => {
      const { data } = await api.delete(`/api/cart/${customerId}`)
      return { data, customerId }
    },
    onSuccess: (result) => {
      qc.invalidateQueries({ queryKey: ['cart', result.customerId] })
    },
  })
}
"""

# ── useOrders hook ────────────────────────────────────────────────────
files["hooks/useOrders.ts"] = """import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/apiClient'

export type OrderItem = {
  id: string
  book_id: string
  quantity: number
  unit_price: number
  subtotal: number
  title?: string
}

export type Order = {
  id: string
  customer_id: string
  status: string
  total_amount: number
  items: OrderItem[]
  created_at: string
  updated_at: string
  notes?: string
}

export function useOrders(customerId: string) {
  return useQuery<Order[]>({
    queryKey: ['orders', customerId],
    queryFn: async () => {
      const { data } = await api.get('/api/orders', { params: { customer_id: customerId } })
      return Array.isArray(data) ? data : []
    },
    enabled: !!customerId,
    staleTime: 1000 * 30,
  })
}

export function useOrder(orderId: string) {
  return useQuery<Order>({
    queryKey: ['order', orderId],
    queryFn: async () => {
      const { data } = await api.get(`/api/orders/${orderId}`)
      return data
    },
    enabled: !!orderId,
    staleTime: 1000 * 30,
  })
}

export function useCreateOrder() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (payload: { customer_id: string; items: any[]; notes?: string }) => {
      const { data } = await api.post('/api/orders', payload)
      return data
    },
    onSuccess: (_, variables) => {
      qc.invalidateQueries({ queryKey: ['orders', variables.customer_id] })
    },
  })
}
"""

# ── useAssistant hook ─────────────────────────────────────────────────
files["hooks/useAssistant.ts"] = """import { useState } from 'react'
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
"""

# ── useRecommendations hook ───────────────────────────────────────────
files["hooks/useRecommendations.ts"] = """import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'

export type Recommendation = {
  id: string
  title: string
  author: string
  category: string
  price: number
  published_flag: boolean
  quantity_available: number
}

export function useRecommendations(bookId: string) {
  return useQuery<Recommendation[]>({
    queryKey: ['recommendations', bookId],
    queryFn: async () => {
      const { data } = await api.get(`/api/recommendations/${bookId}`)
      return Array.isArray(data) ? data : []
    },
    enabled: !!bookId,
    staleTime: 1000 * 60,
  })
}
"""

# ── CartPage ──────────────────────────────────────────────────────────
files["pages/cart/CartPage.tsx"] = """import React, { useContext, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useCart, useUpdateCartItem, useRemoveCartItem, useClearCart } from '../../hooks/useCart'
import { useCreateOrder } from '../../hooks/useOrders'

export default function CartPage() {
  const { state } = useContext(AuthContext)
  const navigate = useNavigate()
  const customerId = state.user?.email || 'guest-001'
  const { data: cart, isLoading } = useCart(customerId)
  const updateItem = useUpdateCartItem()
  const removeItem = useRemoveCartItem()
  const clearCart = useClearCart()
  const createOrder = useCreateOrder()
  const [confirming, setConfirming] = useState(false)

  async function handleConfirmOrder() {
    if (!cart || cart.items.length === 0) return
    setConfirming(true)
    try {
      const orderItems = cart.items.map(item => ({
        book_id: item.book_id,
        quantity: item.quantity,
        unit_price: item.unit_price,
        title: item.book_id,
      }))
      const order = await createOrder.mutateAsync({
        customer_id: customerId,
        items: orderItems,
        notes: 'Pedido desde el carrito',
      })
      await clearCart.mutateAsync(customerId)
      navigate('/orders/' + order.id)
    } catch (e: any) {
      alert(e?.response?.data?.detail?.message || 'Error al crear el pedido')
    } finally {
      setConfirming(false)
    }
  }

  if (!state.isAuthenticated) {
    return (
      <div style={{ padding: 48, textAlign: 'center' }}>
        <p style={{ color: 'var(--text-2)', marginBottom: 16 }}>Debes iniciar sesión para ver tu carrito</p>
        <button className="btn btn-primary" onClick={() => navigate('/login')}>Iniciar sesión</button>
      </div>
    )
  }

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 48, color: 'var(--text-3)' }}>Cargando carrito...</div>

  const items = cart?.items || []
  const total = cart?.total || 0

  return (
    <div className="page">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 28 }}>
        <h1>Mi Carrito</h1>
        {items.length > 0 && (
          <button className="btn btn-ghost btn-sm" onClick={() => clearCart.mutate(customerId)}>
            Vaciar carrito
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 64, color: 'var(--text-3)' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>🛒</div>
          <p>Tu carrito está vacío</p>
          <button className="btn btn-primary" onClick={() => navigate('/catalog')} style={{ marginTop: 16 }}>
            Ver catálogo
          </button>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 24, alignItems: 'flex-start' }}>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Libro</th>
                  <th>Precio</th>
                  <th>Cantidad</th>
                  <th>Subtotal</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {items.map(item => (
                  <tr key={item.id}>
                    <td style={{ fontWeight: 500 }}>{item.book_id}</td>
                    <td>${Number(item.unit_price).toLocaleString('es-CO')} COP</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <button className="btn btn-ghost btn-sm" onClick={() => {
                          if (item.quantity > 1) updateItem.mutate({ itemId: item.id, quantity: item.quantity - 1, customerId })
                        }}>-</button>
                        <span style={{ minWidth: 24, textAlign: 'center' }}>{item.quantity}</span>
                        <button className="btn btn-ghost btn-sm" onClick={() =>
                          updateItem.mutate({ itemId: item.id, quantity: item.quantity + 1, customerId })
                        }>+</button>
                      </div>
                    </td>
                    <td style={{ fontWeight: 600, color: 'var(--accent)' }}>${Number(item.subtotal).toLocaleString('es-CO')} COP</td>
                    <td>
                      <button className="btn btn-ghost btn-sm" onClick={() => removeItem.mutate({ itemId: item.id, customerId })}
                        style={{ color: 'var(--accent)' }}>✕</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 'var(--r-lg)', padding: 24, position: 'sticky', top: 80 }}>
            <h3 style={{ marginBottom: 16, fontFamily: 'var(--font-display)' }}>Resumen</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, color: 'var(--text-2)' }}>
              <span>{items.length} {items.length === 1 ? 'item' : 'items'}</span>
            </div>
            <div style={{ borderTop: '1px solid var(--border)', paddingTop: 12, marginTop: 12, display: 'flex', justifyContent: 'space-between', fontWeight: 700, fontSize: 18 }}>
              <span>Total</span>
              <span style={{ color: 'var(--accent)' }}>${Number(total).toLocaleString('es-CO')} COP</span>
            </div>
            <button className="btn btn-primary" style={{ width: '100%', marginTop: 16, justifyContent: 'center' }}
              onClick={handleConfirmOrder} disabled={confirming}>
              {confirming ? 'Procesando...' : 'Confirmar Pedido'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
"""

# ── OrdersPage ────────────────────────────────────────────────────────
files["pages/orders/OrdersPage.tsx"] = """import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useOrders } from '../../hooks/useOrders'

const STATUS_COLORS: Record<string, string> = {
  pending: '#F59E0B',
  confirmed: '#3B82F6',
  shipped: '#8B5CF6',
  delivered: '#10B981',
  cancelled: '#EF4444',
}

export default function OrdersPage() {
  const { state } = useContext(AuthContext)
  const navigate = useNavigate()
  const customerId = state.user?.email || 'guest-001'
  const { data: orders, isLoading } = useOrders(customerId)

  if (!state.isAuthenticated) {
    return (
      <div style={{ padding: 48, textAlign: 'center' }}>
        <p style={{ color: 'var(--text-2)', marginBottom: 16 }}>Debes iniciar sesión para ver tus pedidos</p>
        <button className="btn btn-primary" onClick={() => navigate('/login')}>Iniciar sesión</button>
      </div>
    )
  }

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 48, color: 'var(--text-3)' }}>Cargando pedidos...</div>

  return (
    <div className="page">
      <h1 style={{ marginBottom: 28 }}>Mis Pedidos</h1>
      {!orders || orders.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 64, color: 'var(--text-3)' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>📦</div>
          <p>No tienes pedidos aún</p>
          <button className="btn btn-primary" onClick={() => navigate('/catalog')} style={{ marginTop: 16 }}>
            Ir al catálogo
          </button>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Estado</th>
                <th>Total</th>
                <th>Fecha</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id} style={{ cursor: 'pointer' }} onClick={() => navigate('/orders/' + order.id)}>
                  <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{order.id.slice(0, 8)}...</td>
                  <td>
                    <span style={{
                      background: STATUS_COLORS[order.status] + '20',
                      color: STATUS_COLORS[order.status],
                      padding: '3px 10px', borderRadius: 20, fontSize: 12, fontWeight: 600
                    }}>{order.status}</span>
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--accent)' }}>${order.total_amount.toLocaleString('es-CO')} COP</td>
                  <td style={{ color: 'var(--text-3)', fontSize: 12 }}>{new Date(order.created_at).toLocaleDateString('es-CO')}</td>
                  <td><span style={{ color: 'var(--accent)', fontSize: 13 }}>Ver →</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
"""

# ── OrderDetailPage ───────────────────────────────────────────────────
files["pages/orders/OrderDetailPage.tsx"] = """import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useOrder } from '../../hooks/useOrders'

const STATUS_COLORS: Record<string, string> = {
  pending: '#F59E0B', confirmed: '#3B82F6',
  shipped: '#8B5CF6', delivered: '#10B981', cancelled: '#EF4444',
}

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: order, isLoading } = useOrder(id || '')

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 48, color: 'var(--text-3)' }}>Cargando pedido...</div>
  if (!order) return <div className="page"><p>Pedido no encontrado</p></div>

  return (
    <div className="page">
      <button className="btn btn-ghost btn-sm" onClick={() => navigate('/orders')} style={{ marginBottom: 24 }}>← Mis Pedidos</button>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
        <h1>Pedido #{order.id.slice(0, 8)}</h1>
        <span style={{ background: STATUS_COLORS[order.status] + '20', color: STATUS_COLORS[order.status], padding: '6px 16px', borderRadius: 20, fontWeight: 600 }}>
          {order.status}
        </span>
      </div>
      <div className="table-wrap" style={{ marginBottom: 24 }}>
        <table>
          <thead><tr><th>Libro</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr></thead>
          <tbody>
            {order.items.map(item => (
              <tr key={item.id}>
                <td>{item.title || item.book_id}</td>
                <td>{item.quantity}</td>
                <td>${item.unit_price.toLocaleString('es-CO')} COP</td>
                <td style={{ fontWeight: 600, color: 'var(--accent)' }}>${item.subtotal.toLocaleString('es-CO')} COP</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 16 }}>
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 'var(--r-lg)', padding: 20, minWidth: 240 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, color: 'var(--text-2)', fontSize: 13 }}>
            <span>Fecha</span><span>{new Date(order.created_at).toLocaleDateString('es-CO')}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 700, fontSize: 18, borderTop: '1px solid var(--border)', paddingTop: 12 }}>
            <span>Total</span>
            <span style={{ color: 'var(--accent)' }}>${order.total_amount.toLocaleString('es-CO')} COP</span>
          </div>
        </div>
      </div>
    </div>
  )
}
"""

# ── AssistantPage ─────────────────────────────────────────────────────
files["pages/assistant/AssistantPage.tsx"] = """import React, { useState, useRef, useEffect } from 'react'
import { useAssistant } from '../../hooks/useAssistant'

const SESSION_ID = 'session-' + Math.random().toString(36).slice(2, 9)

export default function AssistantPage() {
  const { messages, isLoading, sendMessage } = useAssistant(SESSION_ID)
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend() {
    if (!input.trim() || isLoading) return
    const q = input.trim()
    setInput('')
    await sendMessage(q)
  }

  return (
    <div className="page" style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 200px)' }}>
      <h1 style={{ marginBottom: 8 }}>Asistente BookFlow</h1>
      <p style={{ color: 'var(--text-2)', fontSize: 14, marginBottom: 24 }}>
        Pregunta sobre disponibilidad, precios y características de los libros
      </p>

      <div style={{ flex: 1, overflowY: 'auto', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 'var(--r-lg)', padding: 20, marginBottom: 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-3)', padding: 32 }}>
            <div style={{ fontSize: 40, marginBottom: 12 }}>🤖</div>
            <p>Hola! Soy el asistente de BookFlow.</p>
            <p style={{ fontSize: 13, marginTop: 8 }}>Puedes preguntarme sobre precios, disponibilidad y características de los libros.</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
            <div style={{
              maxWidth: '75%', padding: '10px 16px', borderRadius: 16,
              background: msg.role === 'user' ? 'var(--accent)' : 'var(--bg)',
              color: msg.role === 'user' ? 'white' : 'var(--text)',
              fontSize: 14, lineHeight: 1.5,
            }}>
              {msg.content}
            </div>
            {msg.sources && msg.sources.length > 0 && (
              <div style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 4 }}>
                Fuentes: {msg.sources.join(', ')}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div style={{ display: 'flex', alignItems: 'flex-start' }}>
            <div style={{ background: 'var(--bg)', padding: '10px 16px', borderRadius: 16, color: 'var(--text-3)', fontSize: 14 }}>
              Pensando...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <input
          type="text" value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder="¿Cuánto cuesta Don Quixote?"
          style={{ flex: 1 }}
          disabled={isLoading}
        />
        <button className="btn btn-primary" onClick={handleSend} disabled={isLoading || !input.trim()}>
          Enviar
        </button>
      </div>
    </div>
  )
}
"""

# ── NavBar updated ────────────────────────────────────────────────────
files["components/shared/NavBar.tsx"] = """import React, { useContext } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useCart } from '../../hooks/useCart'

export default function NavBar() {
  const { state, dispatch } = useContext(AuthContext)
  const navigate = useNavigate()
  const location = useLocation()
  const customerId = state.user?.email || 'guest-001'
  const { data: cart } = useCart(customerId)
  const cartCount = cart?.items?.length || 0

  function handleLogout() {
    dispatch({ type: 'LOGOUT' })
    navigate('/catalog')
  }

  const navLink = (path: string, label: string, extra?: React.ReactNode) => (
    <button
      className="navbar-link"
      style={{ color: location.pathname.startsWith(path) ? '#FB923C' : undefined }}
      onClick={() => navigate(path)}
    >
      {label}{extra}
    </button>
  )

  return (
    <nav className="navbar">
      <span className="navbar-brand" onClick={() => navigate('/catalog')} style={{ cursor: 'pointer' }}>
        Book<span>Flow</span>
      </span>
      <div className="navbar-actions">
        {navLink('/catalog', 'Catalogo')}
        {navLink('/assistant', 'Asistente')}
        {navLink('/cart', 'Carrito', cartCount > 0 ? (
          <span style={{ background: '#FB923C', color: 'white', borderRadius: '50%', width: 18, height: 18, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, marginLeft: 6, fontWeight: 700 }}>
            {cartCount}
          </span>
        ) : null)}
        {state.isAuthenticated && navLink('/orders', 'Mis Pedidos')}
        {state.isAuthenticated ? (
          <button className="navbar-link" onClick={handleLogout}>Salir</button>
        ) : (
          <button className="navbar-link" onClick={() => navigate('/login')}>Admin</button>
        )}
      </div>
    </nav>
  )
}
"""

# ── Updated BookDetailPage with recommendations and add to cart ───────
files["pages/catalog/BookDetailPage.tsx"] = """import React, { useContext, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useBookDetail } from '../../hooks/useBookDetail'
import { useRecommendations } from '../../hooks/useRecommendations'
import { useAddToCart } from '../../hooks/useCart'
import { AuthContext } from '../../context/AuthContext'

export default function BookDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { state } = useContext(AuthContext)
  const { book, isLoading, isError } = useBookDetail(id)
  const { data: recommendations } = useRecommendations(id || '')
  const addToCart = useAddToCart()
  const [added, setAdded] = useState(false)
  const [addError, setAddError] = useState('')
  const customerId = state.user?.email || 'guest-001'

  async function handleAddToCart() {
    if (!book) return
    setAddError('')
    try {
      await addToCart.mutateAsync({ customer_id: customerId, book_id: book.id, quantity: 1 })
      setAdded(true)
      setTimeout(() => setAdded(false), 3000)
    } catch (e: any) {
      setAddError(e?.response?.data?.detail || 'Error al agregar al carrito')
    }
  }

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 80, color: 'var(--text-3)' }}>Cargando...</div>
  if (isError || !book) return (
    <div className="page">
      <button className="btn btn-ghost btn-sm" onClick={() => navigate('/catalog')}>Volver</button>
      <p style={{ marginTop: 24, color: 'var(--text-2)' }}>No se encontro el libro.</p>
    </div>
  )

  const initials = book.title.split(' ').slice(0,2).map((w:string)=>w[0]).join('').toUpperCase()

  return (
    <div className="page">
      <button className="btn btn-ghost btn-sm" onClick={() => navigate('/catalog')} style={{ marginBottom: 28 }}>
        Volver al catalogo
      </button>

      <div className="detail-layout">
        <div>
          {book.cover_url
            ? <img className="detail-img" src={book.cover_url} alt={book.title} />
            : <div className="detail-img-placeholder">{initials}</div>}
        </div>

        <div className="detail-meta">
          <div>
            {book.enriched_flag
              ? <span className="badge badge-enriched" style={{ marginBottom: 10, display: 'inline-flex' }}>Enriquecido con IA</span>
              : <span className="badge badge-basic" style={{ marginBottom: 10, display: 'inline-flex' }}>Basico</span>}
            <h1 className="detail-title">{book.title}</h1>
            <p className="detail-author" style={{ marginTop: 6 }}>{book.author}</p>
          </div>

          {book.suggested_price ? (
            <div className="detail-price-box">
              <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 4 }}>Precio sugerido por IA</div>
              <div className="detail-price-value">${book.suggested_price.toLocaleString('es-CO')} COP</div>
              {book.price_explanation && <div className="detail-price-explanation">{book.price_explanation}</div>}
            </div>
          ) : <div style={{ color: 'var(--text-3)', fontSize: 14, fontStyle: 'italic' }}>Precio no disponible aun</div>}

          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <button className="btn btn-primary" onClick={handleAddToCart} disabled={addToCart.isPending}>
              {added ? '✓ Agregado!' : addToCart.isPending ? 'Agregando...' : '🛒 Agregar al carrito'}
            </button>
            <button className="btn btn-ghost" onClick={() => navigate('/cart')}>Ver carrito</button>
          </div>
          {addError && <p style={{ color: 'var(--accent)', fontSize: 13 }}>{addError}</p>}

          {book.description && (
            <div>
              <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-3)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 8 }}>Descripcion</div>
              <p className="detail-description">{book.description}</p>
            </div>
          )}

          <div className="detail-attrs">
            {book.publisher && <div className="detail-attr"><div className="detail-attr-label">Editorial</div><div className="detail-attr-value">{book.publisher}</div></div>}
            {book.publication_year && <div className="detail-attr"><div className="detail-attr-label">Anio</div><div className="detail-attr-value">{book.publication_year}</div></div>}
            {book.isbn && <div className="detail-attr"><div className="detail-attr-label">ISBN</div><div className="detail-attr-value" style={{ fontSize: 12 }}>{book.isbn}</div></div>}
          </div>

          <div>{book.published_flag
            ? <span className="badge badge-available">Disponible</span>
            : <span className="badge badge-basic">No disponible</span>}
          </div>
        </div>
      </div>

      {recommendations && recommendations.length > 0 && (
        <div style={{ marginTop: 48 }}>
          <h2 style={{ marginBottom: 20 }}>Tambien te puede interesar</h2>
          <div className="books-grid">
            {recommendations.map(rec => (
              <div key={rec.id} className="book-card fade-in" onClick={() => navigate('/catalog/' + rec.id)} style={{ cursor: 'pointer' }}>
                <div className="book-card-placeholder" style={{ height: 120, fontSize: 24 }}>
                  {rec.title.slice(0, 2).toUpperCase()}
                </div>
                <div className="book-card-body">
                  <div className="book-card-title">{rec.title}</div>
                  <div className="book-card-author">{rec.author}</div>
                  <div className="book-price">${rec.price.toLocaleString('es-CO')} COP</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
"""

# ── Updated routes ────────────────────────────────────────────────────
files["routes.tsx"] = """import React, { useContext } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import AdminBatches from './pages/admin/AdminBatches'
import BatchDetail from './pages/admin/BatchDetail'
import AdminConfig from './pages/admin/AdminConfig'
import AdminPricing from './pages/admin/pricing/AdminPricing'
import CatalogPage from './pages/catalog/CatalogPage'
import BookDetailPage from './pages/catalog/BookDetailPage'
import CartPage from './pages/cart/CartPage'
import OrdersPage from './pages/orders/OrdersPage'
import OrderDetailPage from './pages/orders/OrderDetailPage'
import AssistantPage from './pages/assistant/AssistantPage'
import { AuthContext } from './context/AuthContext'

function PrivateRoute({ children }: { children: JSX.Element }) {
  const { state } = useContext(AuthContext)
  return state.isAuthenticated ? children : <Navigate to="/login" replace />
}

export default function RoutesApp() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/catalog" element={<CatalogPage />} />
      <Route path="/catalog/:id" element={<BookDetailPage />} />
      <Route path="/cart" element={<CartPage />} />
      <Route path="/orders" element={<OrdersPage />} />
      <Route path="/orders/:id" element={<OrderDetailPage />} />
      <Route path="/assistant" element={<AssistantPage />} />
      <Route path="/admin/batches" element={<PrivateRoute><AdminBatches /></PrivateRoute>} />
      <Route path="/admin/batches/:id/errors" element={<PrivateRoute><BatchDetail /></PrivateRoute>} />
      <Route path="/admin/config" element={<PrivateRoute><AdminConfig /></PrivateRoute>} />
      <Route path="/admin/pricing" element={<PrivateRoute><AdminPricing /></PrivateRoute>} />
      <Route path="*" element={<Navigate to="/catalog" replace />} />
    </Routes>
  )
}
"""

# ── Updated App.tsx with NavBar ───────────────────────────────────────
files["App.tsx"] = """import React from 'react'
import NavBar from './components/shared/NavBar'
import RoutesApp from './routes'

export default function App() {
  return (
    <>
      <NavBar />
      <RoutesApp />
    </>
  )
}
"""

# Write all files
for path, content in files.items():
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: {path}")

print("\nAldana UI creada!")
