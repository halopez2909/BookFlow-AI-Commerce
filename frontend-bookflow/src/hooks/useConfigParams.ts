import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/apiClient'

type ConfigParams = Record<string, any>

export function useConfigParams() {
  const qc = useQueryClient()

  const query = useQuery<ConfigParams, Error>(
    {
      queryKey: ['config', 'params'],
      queryFn: async () => {
        const { data } = await api.get('/api/config/params')
        return data
      },
      staleTime: 1000 * 60,
      retry: 1,
    }
  )

  const mutation = useMutation<any, Error, ConfigParams>(
    {
      mutationFn: async (payload: ConfigParams) => {
        const { data } = await api.put('/api/config/params', payload)
        return data
      },
      onSuccess: () => {
        // usar la forma objeto para evitar incompatibilidades de tipos
        qc.invalidateQueries({ queryKey: ['config', 'params'] })
      },
    }
  )

  return {
    ...query,
    save: mutation.mutateAsync,
  }
}
