import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { PricingDecision } from '../utils/types'
import { showError, showSuccess } from '../utils/toast'

const useMocks =
  (import.meta.env.VITE_PRICING_USE_MOCKS as string | undefined) === 'true'

export type OverrideInput = {
  id: string
  manual_price: number
}

/**
 * Hook de escritura: ajusta manualmente el precio de un libro.
 * PUT /api/pricing/decisions/{id}/override
 */
export function usePricingOverride() {
  const qc = useQueryClient()

  const mutation = useMutation<PricingDecision, Error, OverrideInput>({
    mutationFn: async ({ id, manual_price }) => {
      if (useMocks) {
        await new Promise((r) => setTimeout(r, 200))
        // En modo mocks devolvemos una respuesta sintética.
        // El invalidate de abajo hará que la UI se refresque
        // pero contra los mocks originales (es un trade-off conocido de Semana 1).
        return {
          id,
          book_id: 'mock',
          title: 'mock',
          author: 'mock',
          condition: 'mock',
          suggested_price: 0,
          manual_price,
          final_price: manual_price,
          condition_factor: 1,
          reference_count: 0,
          sources: [],
          explanation: '',
          status: 'overridden',
        }
      }
      const { data } = await api.put<PricingDecision>(
        `/api/pricing/decisions/${id}/override`,
        { manual_price }
      )
      return data
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['pricing', 'list'] })
      qc.invalidateQueries({ queryKey: ['pricing', 'detail'] })
      showSuccess('Precio ajustado correctamente')
    },
    onError: (err) => {
      showError(`Error al ajustar precio: ${err.message}`)
    },
  })

  return {
    override: mutation.mutate,
    overrideAsync: mutation.mutateAsync,
    isSaving: mutation.isPending,
    error: mutation.error,
  }
}