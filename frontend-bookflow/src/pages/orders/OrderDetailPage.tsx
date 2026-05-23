import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useOrder } from '../../hooks/useOrders'
import api from '../../services/apiClient'

const STATUS_COLORS: Record<string, string> = {
  pending: '#F59E0B', confirmed: '#3B82F6',
  shipped: '#8B5CF6', delivered: '#10B981', cancelled: '#EF4444',
}

const STATUS_LABELS: Record<string, string> = {
  pending: 'Pendiente', confirmed: 'Confirmado',
  shipped: 'Enviado', delivered: 'Entregado', cancelled: 'Cancelado',
}

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: order, isLoading } = useOrder(id || '')
  const [bookTitles, setBookTitles] = useState<Record<string, string>>({})

  useEffect(() => {
    if (!order) return
    const fetchTitles = async () => {
      const titles: Record<string, string> = {}
      for (const item of order.items) {
        if (item.title && item.title !== item.book_id) {
          titles[item.book_id] = item.title
          continue
        }
        try {
          const { data } = await api.get('/api/catalog/books/' + item.book_id)
          titles[item.book_id] = data.title || item.book_id
        } catch {
          titles[item.book_id] = item.book_id
        }
      }
      setBookTitles(titles)
    }
    fetchTitles()
  }, [order])

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 48, color: 'var(--text-3)' }}>Cargando pedido...</div>
  if (!order) return <div className="page"><p>Pedido no encontrado</p></div>

  return (
    <div className="page">
      <button className="btn btn-ghost btn-sm" onClick={() => navigate('/orders')} style={{ marginBottom: 24 }}>← Mis Pedidos</button>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
        <h1>Pedido #{order.id.slice(0, 8)}</h1>
        <span style={{ background: STATUS_COLORS[order.status] + '20', color: STATUS_COLORS[order.status], padding: '6px 16px', borderRadius: 20, fontWeight: 600 }}>
          {STATUS_LABELS[order.status] || order.status}
        </span>
      </div>
      <div className="table-wrap" style={{ marginBottom: 24 }}>
        <table>
          <thead><tr><th>Libro</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr></thead>
          <tbody>
            {order.items.map(item => (
              <tr key={item.id}>
                <td style={{ cursor: 'pointer', color: 'var(--accent)' }}
                  onClick={() => navigate('/catalog/' + item.book_id)}>
                  {bookTitles[item.book_id] || item.title || item.book_id}
                </td>
                <td>{item.quantity}</td>
                <td>${item.unit_price.toLocaleString('es-CO')} COP</td>
                <td style={{ fontWeight: 600, color: 'var(--accent)' }}>${item.subtotal.toLocaleString('es-CO')} COP</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
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
