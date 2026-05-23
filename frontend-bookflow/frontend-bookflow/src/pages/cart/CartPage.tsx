import React, { useContext, useState } from 'react'
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
    if (!state.isAuthenticated) { navigate('/login'); return }
    setConfirming(true)
    try {
      const orderItems = cart.items.map(item => ({
        book_id: item.book_id, quantity: item.quantity,
        unit_price: item.unit_price, title: item.book_id,
      }))
      const order = await createOrder.mutateAsync({
        customer_id: customerId, items: orderItems, notes: 'Pedido desde carrito',
      })
      await clearCart.mutateAsync(customerId)
      navigate('/orders/' + order.id)
    } catch (e: any) {
      alert(e?.response?.data?.detail?.message || 'Error al crear el pedido')
    } finally { setConfirming(false) }
  }

  if (!state.isAuthenticated && (!cart || cart.items.length === 0)) {
    return (
      <div className="page" style={{ textAlign: 'center', padding: '80px 24px' }}>
        <div style={{ fontSize: 48, marginBottom: 16, opacity: 0.3, fontFamily: 'var(--font-display)' }}>◎</div>
        <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 300, marginBottom: 8 }}>Tu carrito está vacío</h2>
        <p style={{ color: 'var(--text-3)', marginBottom: 24 }}>Explora el catálogo y agrega libros a tu carrito</p>
        <button className="btn btn-primary" onClick={() => navigate('/catalog')}>Explorar catálogo</button>
      </div>
    )
  }

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 80, color: 'var(--text-3)' }}>Cargando carrito...</div>

  const items = cart?.items || []
  const total = cart?.total || 0

  return (
    <div className="page fade-up">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 32 }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontWeight: 300, fontSize: 'clamp(2rem,4vw,3rem)' }}>Mi Carrito</h1>
        {items.length > 0 && (
          <button className="btn btn-ghost btn-sm" onClick={() => clearCart.mutate(customerId)}>Vaciar</button>
        )}
      </div>

      {items.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 64 }}>
          <p style={{ color: 'var(--text-3)', fontFamily: 'var(--font-display)', fontSize: 20 }}>El carrito está vacío</p>
          <button className="btn btn-primary" onClick={() => navigate('/catalog')} style={{ marginTop: 20 }}>Ir al catálogo</button>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 24, alignItems: 'flex-start' }}>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Libro</th><th>Precio</th><th>Cantidad</th><th>Subtotal</th><th></th></tr>
              </thead>
              <tbody>
                {items.map(item => (
                  <tr key={item.id}>
                    <td style={{ fontWeight: 500, color: 'var(--text)', maxWidth: 200 }}>{item.book_id}</td>
                    <td style={{ color: 'var(--text-2)' }}>${Number(item.unit_price).toLocaleString('es-CO')}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <button className="btn btn-ghost btn-sm" style={{ width: 28, padding: '4px 8px' }}
                          onClick={() => { if (item.quantity > 1) updateItem.mutate({ itemId: item.id, quantity: item.quantity - 1, customerId }) }}>−</button>
                        <span style={{ minWidth: 24, textAlign: 'center', fontWeight: 600 }}>{item.quantity}</span>
                        <button className="btn btn-ghost btn-sm" style={{ width: 28, padding: '4px 8px' }}
                          onClick={() => updateItem.mutate({ itemId: item.id, quantity: item.quantity + 1, customerId })}>+</button>
                      </div>
                    </td>
                    <td style={{ fontWeight: 600, color: 'var(--accent)', fontFamily: 'var(--font-display)', fontSize: 16 }}>
                      ${Number(item.subtotal).toLocaleString('es-CO')}
                    </td>
                    <td>
                      <button className="btn btn-ghost btn-sm" style={{ color: 'var(--red)', borderColor: 'var(--red-light)' }}
                        onClick={() => removeItem.mutate({ itemId: item.id, customerId })}>✕</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="cart-summary">
            <h3 style={{ fontFamily: 'var(--font-display)', fontWeight: 400, fontSize: 22, marginBottom: 20 }}>Resumen</h3>
            <div style={{ color: 'var(--text-3)', fontSize: 13, marginBottom: 8 }}>
              {items.length} {items.length === 1 ? 'título' : 'títulos'}
            </div>
            <div className="cart-total-line">
              <span>Total</span>
              <span className="cart-total-amount">${Number(total).toLocaleString('es-CO')} COP</span>
            </div>
            <button className="btn btn-primary" style={{ width: '100%', marginTop: 20, justifyContent: 'center' }}
              onClick={handleConfirmOrder} disabled={confirming}>
              {confirming ? 'Procesando...' : 'Confirmar Pedido'}
            </button>
            {!state.isAuthenticated && (
              <p style={{ fontSize: 12, color: 'var(--text-3)', marginTop: 12, textAlign: 'center', fontStyle: 'italic' }}>
                Debes <a href="/login" style={{ color: 'var(--accent)' }}>iniciar sesión</a> para confirmar
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
