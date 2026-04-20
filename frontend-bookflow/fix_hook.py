content = """import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { ImportBatch } from '../utils/types'

export function useInventoryBatches() {
  return useQuery<ImportBatch[], Error>({
    queryKey: ['inventory', 'batches'],
    queryFn: async () => {
      const { data } = await api.get('/api/inventory/batches')
      if (data && Array.isArray(data.items)) return data.items
      if (Array.isArray(data)) return data
      return []
    },
    staleTime: 1000 * 60,
    retry: 1,
  })
}
"""
with open('src/hooks/useInventoryBatches.ts', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
