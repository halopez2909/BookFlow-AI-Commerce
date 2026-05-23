import React, { useContext, useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useCart } from '../../hooks/useCart'

export default function NavBar() {
  const { state, dispatch } = useContext(AuthContext)
  const navigate = useNavigate()
  const location = useLocation()
  const customerId = state.user?.email || 'guest-001'
  const { data: cart } = useCart(customerId)
  const cartCount = cart?.items?.length || 0
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  const isActive = (path: string) => location.pathname.startsWith(path)

  return (
    <nav className="navbar" style={{ boxShadow: scrolled ? '0 4px 32px rgba(0,0,0,0.4)' : 'none' }}>
      <span className="navbar-brand" onClick={() => navigate('/catalog')}>
        <span className="navbar-brand-dot" />
        Book<span>Flow</span>
      </span>
      <div className="navbar-actions">
        {[
          { path: '/catalog', label: 'Catálogo' },
          { path: '/assistant', label: 'Asistente' },
        ].map(({ path, label }) => (
          <button key={path} className={`navbar-link ${isActive(path) ? 'active' : ''}`} onClick={() => navigate(path)}>
            {label}
          </button>
        ))}
        <button className={`navbar-link ${isActive('/cart') ? 'active' : ''}`} onClick={() => navigate('/cart')}>
          Carrito {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
        </button>
        {state.isAuthenticated && (
          <button className={`navbar-link ${isActive('/orders') ? 'active' : ''}`} onClick={() => navigate('/orders')}>
            Pedidos
          </button>
        )}
        {state.isAuthenticated ? (
          <button className="btn btn-ghost btn-sm" onClick={() => { dispatch({ type: 'LOGOUT' }); navigate('/catalog'); }} style={{ marginLeft: 8 }}>
            Salir
          </button>
        ) : (
          <button className="btn btn-ghost btn-sm" onClick={() => navigate('/login')} style={{ marginLeft: 8 }}>
            Admin
          </button>
        )}
      </div>
    </nav>
  )
}
