import React, { useState } from 'react'

type Props = {
  initialValue?: number
  currency?: string
  isSaving?: boolean
  onSubmit: (manualPrice: number) => void
}

/**
 * Formulario para ajustar manualmente el precio. Única responsabilidad:
 * recibir un valor numérico, validarlo (> 0) y emitirlo al padre.
 */
export default function PriceOverrideForm({
  initialValue,
  currency = 'ARS',
  isSaving,
  onSubmit,
}: Props) {
  const [value, setValue] = useState<string>(
    initialValue !== undefined ? String(initialValue) : ''
  )
  const [error, setError] = useState<string | null>(null)

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const numeric = Number(value)
    if (!value.trim() || Number.isNaN(numeric)) {
      setError('El precio debe ser un número válido')
      return
    }
    if (numeric <= 0) {
      setError('El precio debe ser mayor a 0')
      return
    }
    setError(null)
    onSubmit(numeric)
  }

  return (
    <form
      data-testid="price-override-form"
      onSubmit={handleSubmit}
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: 8,
        padding: 12,
        border: '1px solid #e2e8f0',
        borderRadius: 8,
        background: 'white',
      }}
    >
      <label style={{ fontSize: 13, color: '#334155' }} htmlFor="manual-price">
        Precio manual ({currency})
      </label>
      <input
        id="manual-price"
        type="number"
        step="0.01"
        min="0"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        aria-label="Precio manual"
        aria-invalid={!!error}
        style={{
          padding: '6px 8px',
          border: `1px solid ${error ? '#dc2626' : '#cbd5e1'}`,
          borderRadius: 6,
          fontSize: 14,
        }}
      />
      {error && (
        <div role="alert" style={{ color: '#dc2626', fontSize: 12 }}>
          {error}
        </div>
      )}
      <button
        type="submit"
        disabled={isSaving}
        style={{
          alignSelf: 'flex-start',
          padding: '6px 14px',
          background: '#166534',
          color: 'white',
          border: 'none',
          borderRadius: 6,
          cursor: isSaving ? 'not-allowed' : 'pointer',
          fontWeight: 600,
        }}
      >
        {isSaving ? 'Guardando...' : 'Guardar precio'}
      </button>
    </form>
  )
}