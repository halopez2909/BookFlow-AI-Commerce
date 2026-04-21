import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { PricingDecision } from '../utils/types'
import { showError, showSuccess } from '../utils/toast'

const useMocks =
  (import.meta.env.VITE_PRICING_USE_MOCKS as string | undefined) === 'true'

export type RecalculateInput = {
  book_id: string
  decision_id?: string
}

/**
 * Hook de escritura: recalcula el precio sugerido de un libro.
 * POST /api/pricing/calculate
 */
export function usePricingRecalculate() {
  const qc = useQueryClient()

  const mutation = useMutation<PricingDecision, Error, RecalculateInput>({
    mutationFn: async (payload) => {
      if (useMocks) {
        await new Promise((r) => setTimeout(r, 400))
        return {
          id: payload.decision_id || 'mock-new',
          book_id: payload.book_id,
          title: 'mock',
          author: 'mock',
          condition: 'mock',
          suggested_price: Math.floor(10000 + Math.random() * 20000),
          condition_factor: 0.9,
          reference_count: 4,
          sources: [],
          explanation: '',
          status: 'suggested',
        }
      }
      const { data } = await api.post<PricingDecision>(
        '/api/pricing/calculate',
        payload
      )
      return data
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['pricing', 'list'] })
      qc.invalidateQueries({ queryKey: ['pricing', 'detail'] })
      showSuccess('Precio recalculado')
    },
    onError: (err) => {
      showError(`Error al recalcular: ${err.message}`)
    },
  })

  return {
    recalculate: mutation.mutate,
    recalculateAsync: mutation.mutateAsync,
    isRecalculating: mutation.isPending,
    error: mutation.error,
  }
}