import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { Book } from '../utils/types'
type CatalogData = { items: Book[]; total: number; page: number; page_size: number }
type Filters = { title?: string; min_price?: number; max_price?: number; available?: boolean }
export function useCatalog() {
  const [filters, setFiltersState] = useState<Filters>({})
  const [page, setPage] = useState(1)
  const [extraItems, setExtraItems] = useState<Book[]>([])
  const { data, isLoading, isError, refetch } = useQuery<CatalogData>({
    queryKey: ['catalog', filters, page],
    queryFn: async () => {
      const params: Record<string, string> = { page: String(page), page_size: '20' }
      if (filters.title) params.title = filters.title
      if (filters.min_price !== undefined) params.min_price = String(filters.min_price)
      if (filters.max_price !== undefined) params.max_price = String(filters.max_price)
      if (filters.available) params.available = 'true'
      const { data } = await api.get<CatalogData>('/api/catalog/books', { params })
      return data
    },
    staleTime: 1000 * 30,
  })
  function fetchNextPage() {
    if (data && (data.items.length + extraItems.length) < data.total) {
      setExtraItems(prev => [...prev, ...(data.items ?? [])])
      setPage(p => p + 1)
    }
  }
  function setFilters(f: Filters) { setFiltersState(f); setPage(1); setExtraItems([]) }
  const items = page === 1 ? (data?.items ?? []) : extraItems
  return { data: data ? { ...data, items } : undefined, isLoading, isError, refetch, filters, setFilters, fetchNextPage }
}
