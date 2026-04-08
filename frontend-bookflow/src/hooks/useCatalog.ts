import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { Book } from '../utils/types'
import { useDebounce } from './useDebounce'

type Filters = { title?: string; category_id?: string }
type CatalogResponse = { items: Book[]; total: number; page: number; page_size: number }

export function useCatalog() {
  const [filters, setFilters] = useState<Filters>({})
  const [page, setPage] = useState(1)
  const PAGE_SIZE = 20
  const debouncedTitle = useDebounce(filters.title, 300)

  const query = useQuery<CatalogResponse, Error>({
    queryKey: ['catalog', 'books', debouncedTitle, filters.category_id, page],
    queryFn: async () => {
      const params: Record<string, any> = { page, page_size: PAGE_SIZE }
      if (debouncedTitle) params.title = debouncedTitle
      if (filters.category_id) params.category_id = filters.category_id
      const { data } = await api.get('/api/catalog/books', { params })
      return data
    },
    staleTime: 1000 * 60,
    retry: 1,
  })

  return {
    ...query,
    filters,
    setFilters,
    page,
    fetchNextPage: () => setPage(p => p + 1),
    PAGE_SIZE,
  }
}
