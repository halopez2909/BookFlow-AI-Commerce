import axios from 'axios'
import type { AxiosInstance } from 'axios'
import { showError } from '../utils/toast'


const baseURL = (import.meta.env.VITE_BFF_URL as string) || 'http://localhost:8000'

let getToken: () => string | null = () => null
export function registerTokenGetter(fn: () => string | null) { getToken = fn }

const api: AxiosInstance = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})
console.log('API baseURL=', baseURL)

// request: attach token
api.interceptors.request.use((config) => {
  const token = getToken()
  if (token && config.headers) config.headers.Authorization = `Bearer ${token}`
  return config
})

// response: handle 401
api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

api.interceptors.response.use(
  (r) => r,
  (err) => {
    const status = err?.response?.status
    if (status === 401) {
      window.location.href = '/login'
      return Promise.reject(err)
    }
    // construir mensaje legible
    let message = 'Request failed'
    if (err?.response?.data?.message) message = err.response.data.message
    else if (err?.message) message = err.message
    showError(message)
    return Promise.reject(err)
  }
)

export default api
