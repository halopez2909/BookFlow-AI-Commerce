import React from 'react'
import NavBar from './components/shared/NavBar'
import FloatingControls from './components/shared/FloatingControls'
import RoutesApp from './routes'

export default function App() {
  return (
    <>
      <NavBar />
      <RoutesApp />
      <FloatingControls />
    </>
  )
}
