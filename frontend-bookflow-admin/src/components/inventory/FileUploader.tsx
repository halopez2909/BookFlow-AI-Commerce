import React, { useState } from 'react'
import api from '../../services/apiClient'
import { showSuccess, showError } from '../../utils/toast'

type UploadResult = {
  status: 'success' | 'partial' | 'error'
  importBatch?: any
  message?: string
}

export default function FileUploader({ onResult }: { onResult?: (r: UploadResult) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const maxSize = 5 * 1024 * 1024 // 5MB
  const allowedExt = ['.csv', '.xls', '.xlsx']

  function validate(f: File) {
    const name = f.name.toLowerCase()
    const okExt = allowedExt.some((ext) => name.endsWith(ext))
    const okSize = f.size <= maxSize
    return okExt && okSize
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!file) {
      showError('Selecciona un archivo')
      return
    }
    if (!validate(file)) {
      showError('Archivo inválido (tipo o tamaño)')
      return
    }
    setLoading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const { data } = await api.post('/api/inventory/upload', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      const result: UploadResult = { status: 'success', importBatch: data }
      onResult?.(result)
      showSuccess('Archivo subido con éxito')
    } catch (err: any) {
      console.error(err)
      const message = err?.response?.data?.message || err?.message || 'Error al subir archivo'
      const result: UploadResult = { status: 'error', message }
      onResult?.(result)
      showError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <input
        type="file"
        accept=".csv,.xls,.xlsx"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        disabled={loading}
      />
      <button type="submit" disabled={loading}>{loading ? 'Subiendo...' : 'Subir archivo'}</button>
    </form>
  )
}
