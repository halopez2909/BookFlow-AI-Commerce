import React, { useEffect, useState } from 'react'
import { useConfigParams } from '../../hooks/useConfigParams'
import { showSuccess, showError } from '../../utils/toast'

export default function AdminConfig() {
  const { data, isLoading, error, save } = useConfigParams()
  const [form, setForm] = useState<Record<string, any>>({})

  useEffect(() => {
    if (data) setForm(data)
  }, [data])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    try {
      await save(form)
      showSuccess('Parámetros guardados')
    } catch (err: any) {
      console.error(err)
      showError(err?.response?.data?.message || err?.message || 'Error al guardar parámetros')
    }
  }

  if (isLoading) return <div>Loading...</div>
  if (error) return <div style={{ color: 'crimson' }}>Error: {String(error)}</div>

  return (
    <form onSubmit={handleSubmit}>
      {Object.entries(form || {}).map(([k, v]) => (
        <div key={k}>
          <label>{k}</label>
          <input value={v as any} onChange={e => setForm({ ...form, [k]: e.target.value })} />
        </div>
      ))}
      <button type="submit">Guardar</button>
    </form>
  )
}
