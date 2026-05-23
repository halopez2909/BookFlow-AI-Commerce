import os

BASE = "frontend-bookflow/src"

# Fix LibraryGate - show every time visiting catalog
with open(f"{BASE}/pages/catalog/CatalogPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove sessionStorage logic - always show gate
content = content.replace(
    "const GATE_KEY = 'bookflow_gate_seen'\n\n",
    ""
).replace(
    "const [gateOpen, setGateOpen] = useState(() => sessionStorage.getItem(GATE_KEY) === '1')",
    "const [gateOpen, setGateOpen] = useState(false)"
).replace(
    "  function handleGateOpen() {\n    sessionStorage.setItem(GATE_KEY, '1')\n    setGateOpen(true)\n  }",
    "  function handleGateOpen() { setGateOpen(true) }"
)

with open(f"{BASE}/pages/catalog/CatalogPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Gate: siempre visible OK")

# ScrollToTop + ThemeToggle component
scroll_top = """import React, { useState, useEffect } from 'react'

export default function FloatingControls() {
  const [visible, setVisible] = useState(false)
  const [dark, setDark] = useState(() => localStorage.getItem('theme') !== 'light')

  useEffect(() => {
    const handler = () => setVisible(window.scrollY > 400)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  useEffect(() => {
    const root = document.documentElement
    if (dark) {
      root.style.setProperty('--bg', '#080706')
      root.style.setProperty('--bg-2', '#0E0C0A')
      root.style.setProperty('--bg-card', '#141210')
      root.style.setProperty('--bg-card-hover', '#1C1916')
      root.style.setProperty('--text', '#F0EAE0')
      root.style.setProperty('--text-2', '#9E8E7A')
      root.style.setProperty('--text-3', '#5C4E3E')
      root.style.setProperty('--border', 'rgba(200,164,90,0.1)')
      root.style.setProperty('--border-strong', 'rgba(200,164,90,0.22)')
      localStorage.setItem('theme', 'dark')
    } else {
      root.style.setProperty('--bg', '#F8F4EE')
      root.style.setProperty('--bg-2', '#EFEBE3')
      root.style.setProperty('--bg-card', '#FFFFFF')
      root.style.setProperty('--bg-card-hover', '#F5F0E8')
      root.style.setProperty('--text', '#1A1208')
      root.style.setProperty('--text-2', '#6B5A40')
      root.style.setProperty('--text-3', '#A8926E')
      root.style.setProperty('--border', 'rgba(139,100,30,0.15)')
      root.style.setProperty('--border-strong', 'rgba(139,100,30,0.28)')
      localStorage.setItem('theme', 'light')
    }
  }, [dark])

  const btnStyle: React.CSSProperties = {
    width: 44, height: 44, borderRadius: '50%',
    background: 'var(--bg-card)', border: '1px solid var(--border-strong)',
    color: 'var(--text-2)', cursor: 'pointer',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontSize: 18, transition: 'all 0.25s cubic-bezier(0.4,0,0.2,1)',
    boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
    backdropFilter: 'blur(12px)',
  }

  return (
    <div style={{
      position: 'fixed', bottom: 28, right: 28, z: 300,
      display: 'flex', flexDirection: 'column', gap: 10, zIndex: 300,
    }}>
      <button
        style={{ ...btnStyle, color: dark ? 'var(--accent)' : 'var(--accent)' }}
        onClick={() => setDark(d => !d)}
        title={dark ? 'Modo claro' : 'Modo oscuro'}
      >
        {dark ? '☀' : '☾'}
      </button>
      <button
        style={{
          ...btnStyle,
          opacity: visible ? 1 : 0,
          transform: visible ? 'translateY(0)' : 'translateY(16px)',
          pointerEvents: visible ? 'auto' : 'none',
        }}
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        title="Ir arriba"
      >
        ↑
      </button>
    </div>
  )
}
"""

os.makedirs(f"{BASE}/components/shared", exist_ok=True)
with open(f"{BASE}/components/shared/FloatingControls.tsx", "w", encoding="utf-8") as f:
    f.write(scroll_top)
print("FloatingControls OK")

# Add FloatingControls to App.tsx
app = """import React from 'react'
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
"""
with open(f"{BASE}/App.tsx", "w", encoding="utf-8") as f:
    f.write(app)
print("App.tsx OK")
print("\\nListo! Recarga el navegador.")
