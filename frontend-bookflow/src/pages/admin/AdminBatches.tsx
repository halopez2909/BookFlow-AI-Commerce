import React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useInventoryBatches } from '../../hooks/useInventoryBatches'
import BatchTable from '../../components/inventory/BatchTable'
import FileUploader from '../../components/inventory/FileUploader'

export default function AdminBatches() {
  const navigate = useNavigate()
  const { data: batches, isLoading, isError, error, refetch } = useInventoryBatches()

  return (
    <div style={{ padding: 16, maxWidth: 1000, margin: '0 auto' }}>
      <h1>Import Batches</h1>
      <div style={{ marginBottom: 12 }}>
        <Link to="/admin/pricing">→ Panel de Pricing</Link>
      </div>
      <section style={{ marginBottom: 16 }}>
        <FileUploader onResult={() => refetch()} />
      </section>
      <section>
        {isLoading && <div>Loading...</div>}
        {isError && <div style={{ color: 'crimson' }}>Error: {String(error)}</div>}
        {!isLoading && !isError && Array.isArray(batches) && (
          <BatchTable
            batches={batches}
            loading={isLoading}
            onRowClick={(id) => navigate(`/admin/batches/${id}/errors`)}
          />
        )}
        {!isLoading && !isError && (!batches || batches.length === 0) && (
          <div>No batches found. Upload a file to get started.</div>
        )}
      </section>
    </div>
  )
}