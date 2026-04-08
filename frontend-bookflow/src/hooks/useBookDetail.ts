import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { Book } from '../utils/types'

export function useBookDetail(bookId?: string) {
  return useQuery<Book, Error>({
    queryKey: ['catalog', 'books', bookId],
    queryFn: async () => {
      const { data } = await api.get('/api/catalog/books/' + bookId)
      return data
    },
    enabled: !!bookId,
    staleTime: 1000 * 60,
    retry: 1,
  })
}
