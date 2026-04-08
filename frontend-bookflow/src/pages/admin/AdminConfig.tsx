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
      showSuccess('Parameters saved successfully')
    } catch (err: any) {
      showError(err?.response?.data?.detail || err?.message || 'Error saving parameters')
    }
  }

  if (isLoading) return <div>Loading...</div>
  if (error) return <div style={{ color: 'crimson' }}>Error: {String(error)}</div>

  return (
    <div style={{ padding: 16, maxWidth: 600, margin: '0 auto' }}>
      <h1>System Configuration</h1>
      <form onSubmit={handleSubmit}>
        {Object.entries(form || {}).map(([k, v]) => (
          <div key={k} style={{ marginBottom: 12 }}>
            <label style={{ display: 'block', fontWeight: 500 }}>{k}</label>
            <input
              value={v as string}
              onChange={(e) => setForm({ ...form, [k]: e.target.value })}
              style={{ display: 'block', width: '100%', padding: 8, marginTop: 4 }}
            />
          </div>
        ))}
        <button type="submit" style={{ padding: '8px 16px' }}>
          Save Parameters
        </button>
      </form>
    </div>
  )
}
