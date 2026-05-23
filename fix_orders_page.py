with open("frontend-bookflow/src/pages/orders/OrdersPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add cancel button import
content = content.replace(
    "import { useOrders } from '../../hooks/useOrders'",
    "import { useOrders } from '../../hooks/useOrders'\nimport api from '../../services/apiClient'"
)

# Add cancel function before return
content = content.replace(
    "  if (!state.isAuthenticated)",
    """  async function handleCancel(orderId: string) {
    if (!confirm('¿Cancelar este pedido?')) return
    try {
      await api.put('/api/orders/' + orderId + '/status', { status: 'cancelled' })
      refetch()
    } catch (e: any) {
      alert(e?.response?.data?.detail || 'No se pudo cancelar')
    }
  }

  if (!state.isAuthenticated)"""
)

# Fix useOrders to get refetch
content = content.replace(
    "  const { data: orders, isLoading } = useOrders(customerId)",
    "  const { data: orders, isLoading, refetch } = useOrders(customerId)"
)

# Add cancel button in table
content = content.replace(
    "                  <td><span style={{ color: 'var(--accent)', fontSize: 13 }}>Ver →</span></td>",
    """                  <td style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <span style={{ color: 'var(--accent)', fontSize: 13 }}>Ver →</span>
                    {order.status === 'pending' && (
                      <button className="btn btn-ghost btn-sm" style={{ color: '#EF4444', fontSize: 11 }}
                        onClick={e => { e.stopPropagation(); handleCancel(order.id) }}>
                        Cancelar
                      </button>
                    )}
                  </td>"""
)

with open("frontend-bookflow/src/pages/orders/OrdersPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
