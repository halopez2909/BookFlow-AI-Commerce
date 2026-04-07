import React, { useContext } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import AdminBatches from './pages/admin/AdminBatches'
import BatchDetail from './pages/admin/BatchDetail'
import AdminConfig from './pages/admin/AdminConfig'
import { AuthContext } from './context/AuthContext'

// Protected wrapper
function PrivateRoute({ children }: { children: JSX.Element }) {
  const { state } = useContext(AuthContext)
  return state.isAuthenticated ? children : <Navigate to="/login" replace />
}

export default function RoutesApp() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/admin/batches" element={<PrivateRoute><AdminBatches /></PrivateRoute>} />
      <Route path="/admin/batches/:id/errors" element={<PrivateRoute><BatchDetail /></PrivateRoute>} />
      <Route path="/admin/config" element={<PrivateRoute><AdminConfig /></PrivateRoute>} />
      <Route path="*" element={<Navigate to="/admin/batches" replace />} />
    </Routes>
  )
}
