import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'

export type Recommendation = {
  id: string
  title: string
  author: string
  category: string
  price: number
  published_flag: boolean
  quantity_available: number
}

export function useRecommendations(bookId: string) {
  return useQuery<Recommendation[]>({
    queryKey: ['recommendations', bookId],
    queryFn: async () => {
      const { data } = await api.get(`/api/recommendations/${bookId}`)
      return Array.isArray(data) ? data : []
    },
    enabled: !!bookId,
    staleTime: 1000 * 60,
  })
}
