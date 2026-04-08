import axios from 'axios'
import type { AxiosInstance } from 'axios'

const baseURL = (import.meta.env.VITE_BFF_URL as string) || 'http://localhost:8000'

let getToken: () => string | null = () => null

export function registerTokenGetter(fn: () => string | null) {
  getToken = fn
}

const api: AxiosInstance = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token && config.headers) {
    config.headers.Authorization = 'Bearer ' + token
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (err) => {
    const status = err?.response?.status
    if (status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
