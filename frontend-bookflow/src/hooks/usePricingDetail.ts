import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { PricingDecision } from '../utils/types'
import { PRICING_MOCKS } from '../pages/admin/pricing/pricingMocks'

const useMocks =
  (import.meta.env.VITE_PRICING_USE_MOCKS as string | undefined) === 'true'

/**
 * Hook de lectura: obtiene el detalle de una decisión de pricing.
 * Se activa solo cuando hay un id seleccionado.
 */
export function usePricingDetail(id: string | null | undefined) {
  const query = useQuery<PricingDecision, Error>({
    queryKey: ['pricing', 'detail', id],
    enabled: !!id,
    queryFn: async () => {
      if (!id) throw new Error('Missing pricing id')
      if (useMocks) {
        await new Promise((r) => setTimeout(r, 150))
        const found = PRICING_MOCKS.find((p) => p.id === id)
        if (!found) throw new Error('Pricing decision no encontrada')
        return found
      }
      const { data } = await api.get<PricingDecision>(
        `/api/pricing/decisions/${id}`
      )
      return data
    },
    staleTime: 1000 * 30,
  })

  return {
    detail: query.data,
    isLoading: query.isLoading,
    error: query.error,
  }
}