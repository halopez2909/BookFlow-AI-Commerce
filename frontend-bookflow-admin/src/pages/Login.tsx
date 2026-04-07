import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/apiClient'
import { AuthContext } from '../context/AuthContext'

export default function Login() {
  const { dispatch } = useContext(AuthContext)
  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
    const bff = (import.meta.env.VITE_BFF_URL as string) || 'http://localhost:8000'
    const { data } = await api.post(`${bff}/api/auth/login`, { username, password })
    dispatch({ type: 'LOGIN', payload: { token: data.token, user: data.user } })
    navigate('/admin/batches', { replace: true })
    } catch (err: any) {
    console.error(err)
    setError(err?.response?.data?.message || err?.message || 'Login failed')
    } finally {
    setLoading(false)
    }

  }

  return (
    <div style={{ maxWidth: 420, margin: '48px auto', padding: 16 }}>
      <h2 style={{ marginBottom: 12 }}>Iniciar sesión</h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 8 }}>
          <label htmlFor="username">Usuario</label>
          <input
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ display: 'block', width: '100%', padding: 8, marginTop: 4 }}
            autoComplete="username"
          />
        </div>

        <div style={{ marginBottom: 12 }}>
          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ display: 'block', width: '100%', padding: 8, marginTop: 4 }}
            autoComplete="current-password"
          />
        </div>

        {error && <div style={{ color: 'crimson', marginBottom: 12 }}>{error}</div>}

        <button type="submit" disabled={loading} style={{ padding: '8px 16px' }}>
          {loading ? 'Ingresando...' : 'Ingresar'}
        </button>
      </form>
    </div>
  )
}

