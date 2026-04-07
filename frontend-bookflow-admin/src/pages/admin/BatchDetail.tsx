import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { useBatchErrors } from '../../hooks/useBatchErrors'
import ErrorsTable from '../../components/inventory/ErrorsTable'

export default function BatchDetail() {
  const { id } = useParams()
  const { data: errors, isLoading, isError, error } = useBatchErrors(id)

  return (
    <div style={{ padding: 16, maxWidth: 1000, margin: '0 auto' }}>
      <h1>Errores del lote</h1>
      <div style={{ marginBottom: 12 }}>
        <Link to="/admin/batches">← Volver a lotes</Link>
      </div>

      <section>
        {isLoading && <div>Loading errors...</div>}
        {isError && <div style={{ color: 'crimson' }}>Error: {error?.message}</div>}
        {!isLoading && !isError && <ErrorsTable errors={errors} />}
      </section>
    </div>
  )
}
