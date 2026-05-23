import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
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
