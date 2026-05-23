import React, { useContext } from 'react'
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

  function handleLogout() {
    dispatch({ type: 'LOGOUT' })
    navigate('/catalog')
  }

  const isActive = (path: string) => location.pathname.startsWith(path)

  return (
    <nav className="navbar">
      <span className="navbar-brand" onClick={() => navigate('/catalog')}>
        <span>Book</span>Flow
      </span>
      <div className="navbar-actions">
        <button className={`navbar-link ${isActive('/catalog') ? 'active' : ''}`} onClick={() => navigate('/catalog')}>
          Catálogo
        </button>
        <button className={`navbar-link ${isActive('/assistant') ? 'active' : ''}`} onClick={() => navigate('/assistant')}>
          Asistente
        </button>
        <button className={`navbar-link ${isActive('/cart') ? 'active' : ''}`} onClick={() => navigate('/cart')}>
          Carrito
          {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
        </button>
        {state.isAuthenticated && (
          <button className={`navbar-link ${isActive('/orders') ? 'active' : ''}`} onClick={() => navigate('/orders')}>
            Pedidos
          </button>
        )}
        {state.isAuthenticated ? (
          <button className="btn btn-ghost btn-sm" onClick={handleLogout} style={{ marginLeft: 8 }}>Salir</button>
        ) : (
          <button className="btn btn-ghost btn-sm" onClick={() => navigate('/login')} style={{ marginLeft: 8 }}>Admin</button>
        )}
      </div>
    </nav>
  )
}
