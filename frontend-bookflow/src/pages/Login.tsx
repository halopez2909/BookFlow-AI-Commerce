import React, { useState, useContext } from 'react'
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
    setError(null); setSuccess(null); setLoading(true)
    try {
      if (mode === 'login') {
        const { data } = await api.post('/api/auth/login', { email, password })
        dispatch({ type: 'LOGIN', payload: { token: data.access_token, user: data } })
        navigate('/catalog', { replace: true })
      } else {
        await api.post('/api/auth/register', { email, password, role: 'user' })
        setSuccess('Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
        setMode('login')
      }
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : mode === 'login' ? 'Credenciales incorrectas' : 'Error al registrarse')
    } finally { setLoading(false) }
  }

  return (
    <div className="login-page">
      <div className="login-left">
        <div className="login-bg-lines" />
        <div className="login-left-content fade-up">
          <div className="login-logo">Book<span>Flow</span></div>
          <p className="login-tagline">Plataforma inteligente de comercio de libros con inteligencia artificial aplicada.</p>
          <div className="login-features">
            {['Catálogo enriquecido con IA', 'Precios sugeridos en tiempo real', 'Asistente conversacional', 'Recomendaciones personalizadas'].map(f => (
              <div key={f} className="login-feature">
                <span className="login-feature-dot" />
                {f}
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="login-right">
        <div className="login-form-container fade-up">
          <div className="login-tabs">
            <button className={`login-tab ${mode === 'login' ? 'active' : ''}`} onClick={() => { setMode('login'); setError(null); setSuccess(null); }}>
              Iniciar Sesión
            </button>
            <button className={`login-tab ${mode === 'register' ? 'active' : ''}`} onClick={() => { setMode('register'); setError(null); setSuccess(null); }}>
              Registrarse
            </button>
          </div>
          <h2 className="login-form-title">{mode === 'login' ? 'Bienvenido' : 'Nueva Cuenta'}</h2>
          <p className="login-form-subtitle">{mode === 'login' ? 'Accede para gestionar el sistema' : 'Crea tu cuenta para explorar'}</p>
          {success && <div className="login-success">{success}</div>}
          <form onSubmit={handleSubmit}>
            <div className="login-field">
              <label className="login-label">Correo electrónico</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} required placeholder="tu@email.com" />
            </div>
            <div className="login-field">
              <label className="login-label">Contraseña</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} required placeholder="••••••••" />
            </div>
            {error && <div className="login-error">{error}</div>}
            <button type="submit" disabled={loading} className="btn btn-primary login-submit">
              {loading ? '...' : mode === 'login' ? 'Iniciar Sesión' : 'Crear Cuenta'}
            </button>
          </form>
          <div className="login-back"><a href="/catalog">← Explorar catálogo público</a></div>
        </div>
      </div>
    </div>
  )
}
