import React, { useContext } from 'react'
import type { ReactElement } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import AdminBatches from './pages/admin/AdminBatches'
import BatchDetail from './pages/admin/BatchDetail'
import AdminConfig from './pages/admin/AdminConfig'
import AdminPricing from './pages/admin/pricing/AdminPricing'
import CatalogPage from './pages/catalog/CatalogPage'
import BookDetailPage from './pages/catalog/BookDetailPage'
import { AuthContext } from './context/AuthContext'

function PrivateRoute({ children }: { children: ReactElement }) {
  const { state } = useContext(AuthContext)
  return state.isAuthenticated ? children : <Navigate to="/login" replace />
}

export default function RoutesApp() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/catalog" element={<CatalogPage />} />
      <Route path="/catalog/:id" element={<BookDetailPage />} />
      <Route path="/admin/batches" element={<PrivateRoute><AdminBatches /></PrivateRoute>} />
      <Route path="/admin/batches/:id/errors" element={<PrivateRoute><BatchDetail /></PrivateRoute>} />
      <Route path="/admin/config" element={<PrivateRoute><AdminConfig /></PrivateRoute>} />
      <Route path="/admin/pricing" element={<PrivateRoute><AdminPricing /></PrivateRoute>} />
      <Route path="*" element={<Navigate to="/catalog" replace />} />
    </Routes>
  )
}