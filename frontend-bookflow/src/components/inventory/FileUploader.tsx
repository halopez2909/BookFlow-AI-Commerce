import React, { useState } from 'react'
import api from '../../services/apiClient'
import { showSuccess, showError } from '../../utils/toast'

export default function FileUploader({ onResult }: { onResult?: () => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const maxSizeMB = 10
  const allowedExt = ['.csv', '.xls', '.xlsx']

  function validate(f: File): boolean {
    const name = f.name.toLowerCase()
    const validExt = allowedExt.some((ext) => name.endsWith(ext))
    const validSize = f.size <= maxSizeMB * 1024 * 1024
    if (!validExt) {
      showError('Invalid file type. Only .csv, .xls, .xlsx are allowed.')
      return false
    }
    if (!validSize) {
      showError("File size exceeds " + String(maxSizeMB) + "MB limit.")
      return false
    }
    return true
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!file) {
      showError('Please select a file')
      return
    }
    if (!validate(file)) return
    setLoading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      await api.post('/api/inventory/upload', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      showSuccess('File uploaded successfully')
      setFile(null)
      onResult?.()
    } catch (err: any) {
      showError(err?.response?.data?.detail || err?.message || 'Error uploading file')
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
      <button type="submit" disabled={loading || !file} style={{ padding: '6px 16px' }}>
        {loading ? 'Uploading...' : 'Upload File'}
      </button>
    </form>
  )
}
