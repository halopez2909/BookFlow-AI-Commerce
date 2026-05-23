content = """import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/apiClient'
import { AuthContext } from '../context/AuthContext'

export default function Login() {
  const { dispatch } = useContext(AuthContext)
  const navigate = useNavigate()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setLoading(true)
    try {
      if (mode === 'login') {
        const { data } = await api.post('/api/auth/login', { email, password })
        dispatch({ type: 'LOGIN', payload: { token: data.access_token, user: data } })
        navigate('/catalog', { replace: true })
      } else {
        await api.post('/api/auth/register', { email, password, role: 'user' })
        setSuccess('Cuenta creada exitosamente. Ahora puedes iniciar sesion.')
        setMode('login')
      }
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      if (mode === 'login') {
        setError(typeof detail === 'string' ? detail : 'Credenciales incorrectas')
      } else {
        setError(typeof detail === 'string' ? detail : 'Error al registrarse')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-left">
        <div className="login-left-orb" style={{ width: 350, height: 350, background: 'rgba(251,146,60,0.1)', top: -80, right: -80 }} />
        <div className="login-left-orb" style={{ width: 200, height: 200, background: 'rgba(0,0,0,0.2)', bottom: -60, left: -40 }} />
        <div className="login-left-content">
          <div className="login-logo">Book<span>Flow</span></div>
          <p className="login-tagline">Plataforma inteligente de comercio de libros con IA para pricing y enriquecimiento.</p>
        </div>
      </div>

      <div className="login-right">
        <div className="login-form-container">
          <div style={{ display: 'flex', gap: 8, marginBottom: 24, background: 'var(--bg)', borderRadius: 'var(--r)', padding: 4 }}>
            <button
              onClick={() => { setMode('login'); setError(null); setSuccess(null) }}
              style={{ flex: 1, padding: '8px', borderRadius: 6, border: 'none', cursor: 'pointer', fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: 13,
                background: mode === 'login' ? 'var(--bg-card)' : 'transparent',
                color: mode === 'login' ? 'var(--text)' : 'var(--text-3)',
                boxShadow: mode === 'login' ? 'var(--shadow)' : 'none' }}>
              Iniciar Sesion
            </button>
            <button
              onClick={() => { setMode('register'); setError(null); setSuccess(null) }}
              style={{ flex: 1, padding: '8px', borderRadius: 6, border: 'none', cursor: 'pointer', fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: 13,
                background: mode === 'register' ? 'var(--bg-card)' : 'transparent',
                color: mode === 'register' ? 'var(--text)' : 'var(--text-3)',
                boxShadow: mode === 'register' ? 'var(--shadow)' : 'none' }}>
              Registrarse
            </button>
          </div>

          <h2 className="login-form-title">{mode === 'login' ? 'Bienvenido de vuelta' : 'Crear cuenta'}</h2>
          <p className="login-form-subtitle">{mode === 'login' ? 'Ingresa tus credenciales para continuar' : 'Crea tu cuenta para comprar libros'}</p>

          {success && <div style={{ background: '#F0FDF4', border: '1px solid #86EFAC', color: '#166534', padding: '10px 14px', borderRadius: 'var(--r)', fontSize: 13, marginBottom: 14 }}>{success}</div>}

          <form onSubmit={handleSubmit}>
            <div className="login-field">
              <label className="login-label">Correo</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} required placeholder="tu@email.com" autoComplete="email" />
            </div>
            <div className="login-field">
              <label className="login-label">Contrasena</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} required placeholder="..." autoComplete={mode === 'login' ? 'current-password' : 'new-password'} />
            </div>
            {error && <div className="login-error">{error}</div>}
            <button type="submit" disabled={loading} className="btn btn-primary login-submit">
              {loading ? (mode === 'login' ? 'Ingresando...' : 'Registrando...') : (mode === 'login' ? 'Iniciar Sesion' : 'Crear Cuenta')}
            </button>
          </form>

          <div className="login-back">
            <a href="/catalog">Ver catalogo publico</a>
          </div>
        </div>
      </div>
    </div>
  )
}
"""
with open("frontend-bookflow/src/pages/Login.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
