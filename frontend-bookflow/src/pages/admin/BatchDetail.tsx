import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { useBatchErrors } from '../../hooks/useBatchErrors'
import ErrorsTable from '../../components/inventory/ErrorsTable'

export default function BatchDetail() {
  const { id } = useParams()
  const { data: errors, isLoading, isError, error } = useBatchErrors(id)

  return (
    <div style={{ padding: 16, maxWidth: 1000, margin: '0 auto' }}>
      <h1>Batch Errors</h1>
      <div style={{ marginBottom: 12 }}>
        <Link to="/admin/batches">Back to batches</Link>
      </div>
      {isLoading && <div>Loading...</div>}
      {isError && <div style={{ color: 'crimson' }}>Error: {String(error)}</div>}
      {!isLoading && !isError && Array.isArray(errors) && (
        <ErrorsTable errors={errors} />
      )}
      {!isLoading && !isError && (!errors || errors.length === 0) && (
        <div>No errors found for this batch.</div>
      )}
    </div>
  )
}
