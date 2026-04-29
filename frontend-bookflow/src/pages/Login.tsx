import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/apiClient'
import { AuthContext } from '../context/AuthContext'

export default function Login() {
  const { dispatch } = useContext(AuthContext)
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const { data } = await api.post('/api/auth/login', { email, password })
      dispatch({ type: 'LOGIN', payload: { token: data.access_token, user: data } })
      navigate('/admin/batches', { replace: true })
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-bg-orb login-bg-orb-1" />
      <div className="login-bg-orb login-bg-orb-2" />
      <div className="login-card animate-in">
        <div className="login-logo">Book<span>Flow</span></div>
        <p className="login-subtitle">Admin Portal — Sign in to continue</p>
        <form onSubmit={handleSubmit}>
          <div className="login-field">
            <label className="login-label" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="admin@bookflow.com"
              autoComplete="email"
            />
          </div>
          <div className="login-field">
            <label className="login-label" htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </div>
          {error && <div className="login-error">{error}</div>}
          <button type="submit" disabled={loading} className="btn btn-primary login-submit">
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <div className="login-back">
          <a href="/catalog">Back to catalog</a>
        </div>
      </div>
    </div>
  )
}
