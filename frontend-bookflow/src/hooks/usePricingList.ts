import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { PricingDecision } from '../utils/types'
import { PRICING_MOCKS } from '../pages/admin/pricing/pricingMocks'

// Flag para Semana 1 (mocks) vs Semana 2 (BFF real).
// Se activa poniendo VITE_PRICING_USE_MOCKS=true en el .env
const useMocks =
  (import.meta.env.VITE_PRICING_USE_MOCKS as string | undefined) === 'true'

type ListResponse = { items: PricingDecision[] } | PricingDecision[]

/**
 * Hook de lectura: obtiene el listado de decisiones de pricing.
 * Sólo expone prices, isLoading, error y refetch (Interface Segregation).
 */
export function usePricingList() {
  const query = useQuery<PricingDecision[], Error>({
    queryKey: ['pricing', 'list'],
    queryFn: async () => {
      if (useMocks) {
        // simulamos latencia para ver el skeleton
        await new Promise((r) => setTimeout(r, 250))
        return PRICING_MOCKS
      }
      const { data } = await api.get<ListResponse>('/api/pricing/decisions')
      if (Array.isArray(data)) return data
      if (data && Array.isArray((data as any).items)) {
        return (data as any).items as PricingDecision[]
      }
      return []
    },
    staleTime: 1000 * 30,
    retry: 1,
  })

  return {
    prices: query.data ?? [],
    isLoading: query.isLoading,
    error: query.error,
    refetch: query.refetch,
  }
}