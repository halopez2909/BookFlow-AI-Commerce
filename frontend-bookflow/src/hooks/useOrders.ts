import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
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
    staleTime: 0,
    refetchOnWindowFocus: true,
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
