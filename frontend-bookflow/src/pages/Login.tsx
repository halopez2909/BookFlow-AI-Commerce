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
  const [error, setError] = useState<string|null>(null)
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault(); setError(null); setLoading(true)
    try {
      const { data } = await api.post('/api/auth/login', { email, password })
      dispatch({ type: 'LOGIN', payload: { token: data.access_token, user: data } })
      navigate('/admin/batches', { replace: true })
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Credenciales incorrectas')
    } finally { setLoading(false) }
  }
  return (
    <div className="login-page">
      <div className="login-left">
        <div className="login-left-orb" style={{width:350,height:350,background:'rgba(251,146,60,0.1)',top:-80,right:-80}} />
        <div className="login-left-orb" style={{width:200,height:200,background:'rgba(0,0,0,0.2)',bottom:-60,left:-40}} />
        <div className="login-left-content">
          <div className="login-logo">Book<span>Flow</span></div>
          <p className="login-tagline">Plataforma inteligente de comercio de libros con IA para pricing y enriquecimiento.</p>
        </div>
      </div>
      <div className="login-right">
        <div className="login-form-container">
          <h2 className="login-form-title">Portal Admin</h2>
          <p className="login-form-subtitle">Ingresa tus credenciales para continuar</p>
          <form onSubmit={handleSubmit}>
            <div className="login-field">
              <label className="login-label">Correo</label>
              <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required placeholder="admin@bookflow.com" autoComplete="email" />
            </div>
            <div className="login-field">
              <label className="login-label">Contrasena</label>
              <input type="password" value={password} onChange={e=>setPassword(e.target.value)} required placeholder="..." autoComplete="current-password" />
            </div>
            {error && <div className="login-error">{error}</div>}
            <button type="submit" disabled={loading} className="btn btn-primary login-submit">{loading?'Ingresando...':'Ingresar'}</button>
          </form>
          <div className="login-back"><a href="/catalog">Ver catalogo publico</a></div>
        </div>
      </div>
    </div>
  )
}
