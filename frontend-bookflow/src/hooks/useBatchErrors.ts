import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'

export type BatchError = {
  id: string
  row_number: number
  error_type: string
  message: string
  fix_hint?: string
}

export function useBatchErrors(batchId?: string) {
  return useQuery<BatchError[], Error>({
    queryKey: ['inventory', 'batches', batchId, 'errors'],
    queryFn: async () => {
      const { data } = await api.get(`/api/inventory/batches/${batchId}/errors`)
      return data
    },
    enabled: !!batchId,
    staleTime: 1000 * 60,
    retry: 1,
  })
}
