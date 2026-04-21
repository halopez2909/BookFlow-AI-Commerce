import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { BatchError } from '../utils/types'

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