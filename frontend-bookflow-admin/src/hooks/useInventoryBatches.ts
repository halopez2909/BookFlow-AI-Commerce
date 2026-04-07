import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { ImportBatch } from '../utils/types'

export function useInventoryBatches() {
  return useQuery<ImportBatch[], Error>({
    queryKey: ['inventory', 'batches'],
    queryFn: async () => {
      const { data } = await api.get('/api/inventory/batches')
      return data
    },
    staleTime: 1000 * 60,
    retry: 1,
  })
}
