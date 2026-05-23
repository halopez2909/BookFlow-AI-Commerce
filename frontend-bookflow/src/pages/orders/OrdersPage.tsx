import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useOrders } from '../../hooks/useOrders'
import api from '../../services/apiClient'

const STATUS: Record<string, string> = {
  pending: 'status-pending', confirmed: 'status-confirmed',
  shipped: 'status-shipped', delivered: 'status-delivered', cancelled: 'status-cancelled',
}
const STATUS_LABELS: Record<string, string> = {
  pending: 'Pendiente', confirmed: 'Confirmado',
  shipped: 'Enviado', delivered: 'Entregado', cancelled: 'Cancelado',
}

export default function OrdersPage() {
  const { state } = useContext(AuthContext)
  const navigate = useNavigate()
  const customerId = state.user?.email || 'guest-001'
  const { data: orders, isLoading, refetch } = useOrders(customerId)

  if (!state.isAuthenticated) {
    return (
      <div className="page" style={{ textAlign: 'center', padding: '80px 24px' }}>
        <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 300 }}>Inicia sesión para ver tus pedidos</h2>
        <button className="btn btn-primary" onClick={() => navigate('/login')} style={{ marginTop: 24 }}>Iniciar sesión</button>
      </div>
    )
  }

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 80, color: 'var(--text-3)' }}>Cargando pedidos...</div>

  async function handleCancel(orderId: string) {
    if (!confirm('¿Cancelar este pedido?')) return
    try { await api.put('/api/orders/' + orderId + '/status', { status: 'cancelled' }); refetch() }
    catch (e: any) { alert(e?.response?.data?.detail || 'No se pudo cancelar') }
  }

  return (
    <div className="page fade-up">
      <div className="page-header">
        <h1>Mis Pedidos</h1>
        <p>Historial completo de tus compras</p>
      </div>
      {!orders || orders.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 64 }}>
          <p style={{ color: 'var(--text-3)', fontFamily: 'var(--font-display)', fontSize: 20 }}>No tienes pedidos aún</p>
          <button className="btn btn-primary" onClick={() => navigate('/catalog')} style={{ marginTop: 20 }}>Ir al catálogo</button>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>ID</th><th>Estado</th><th>Total</th><th>Fecha</th><th>Acciones</th></tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id} style={{ cursor: 'pointer' }} onClick={() => navigate('/orders/' + order.id)}>
                  <td style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--text-3)' }}>{order.id.slice(0, 8)}...</td>
                  <td><span className={`status-badge ${STATUS[order.status] || ''}`}>{STATUS_LABELS[order.status] || order.status}</span></td>
                  <td style={{ fontFamily: 'var(--font-display)', fontSize: 16, color: 'var(--accent)', fontWeight: 400 }}>
                    ${order.total_amount.toLocaleString('es-CO')} COP
                  </td>
                  <td style={{ color: 'var(--text-3)', fontSize: 12 }}>{new Date(order.created_at).toLocaleDateString('es-CO')}</td>
                  <td style={{ display: 'flex', gap: 8 }} onClick={e => e.stopPropagation()}>
                    <span style={{ color: 'var(--accent)', fontSize: 13 }}>Ver →</span>
                    {order.status === 'pending' && (
                      <button className="btn btn-ghost btn-sm" style={{ color: '#E8A0A0', borderColor: 'var(--red-light)', fontSize: 11 }}
                        onClick={() => handleCancel(order.id)}>Cancelar</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
