import React, { useState, useEffect } from 'react'

interface Props { onOpen: () => void }

export default function LibraryGate({ onOpen }: Props) {
  const [opening, setOpening] = useState(false)

  function handleOpen() {
    setOpening(true)
    setTimeout(onOpen, 900)
  }

  return (
    <div className={`library-gate ${opening ? 'gate-open' : ''}`}>
      <div className="gate-left">
        <div className="login-bg-lines" />
        <div className="gate-text">Book</div>
      </div>
      <div className="gate-right">
        <div className="login-bg-lines" />
        <div className="gate-text">Flow</div>
      </div>
      <div className="gate-center">
        <div className="gate-logo">Book<span>Flow</span></div>
        <div className="gate-tagline">Librería de Comercio Inteligente</div>
        <button className="btn btn-primary gate-btn" onClick={handleOpen} style={{ fontSize: 13, letterSpacing: '0.12em', padding: '14px 32px' }}>
          Explorar Colección
        </button>
      </div>
    </div>
  )
}
