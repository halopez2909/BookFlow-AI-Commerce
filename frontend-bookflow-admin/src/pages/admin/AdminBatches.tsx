import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useInventoryBatches } from '../../hooks/useInventoryBatches'
import BatchTable from '../../components/inventory/BatchTable'
import FileUploader from '../../components/inventory/FileUploader'
import api from '../../services/apiClient'
import { showSuccess, showError } from '../../utils/toast'



export default function AdminBatches() {
  const navigate = useNavigate()
  const { data: batches, isLoading, isError, error, refetch } = useInventoryBatches()

  // Debug: inspecciona en la consola del navegador
  console.log('DEBUG batches:', batches)

  if (!batches) return <div>No batches</div>
  if (!Array.isArray(batches)) {
    console.error('BatchTable: expected array, got:', batches)
    return <div>Invalid data</div>
  }

  async function deleteBatch(id: string, fileName: string) {
    // ejemplo: confirmar solo si no es .test; ajustar según necesidad
    const confirmMsg = fileName.toLowerCase().endsWith('.test')
      ? `¿Eliminar el lote de prueba ${fileName}?`
      : `¿Eliminar el lote ${fileName}?`
    if (!confirm(confirmMsg)) return

    try {
      await api.delete(`/api/inventory/batches/${id}`)
      showSuccess('Lote eliminado')
      await refetch()
    } catch (err: any) {
      console.error(err)
      showError(err?.response?.data?.message || err?.message || 'Error al eliminar lote')
    }
  }

  return (
    <div style={{ padding: 16, maxWidth: 1000, margin: '0 auto' }}>
      <h1>Import Batches</h1>

      <section style={{ marginBottom: 16 }}>
        <FileUploader
          onResult={(res) => {
            console.log('upload result', res)
            // refetch batches after upload
            refetch()
          }}
        />
      </section>

      <section>
        {isLoading && <div>Loading...</div>}
        {isError && <div style={{ color: 'crimson' }}>Error: {String(error)}</div>}
        {!isLoading && !isError && (
          <BatchTable
            batches={batches}
            loading={isLoading}
            onRowClick={(id) => navigate(`/admin/batches/${id}/errors`)}
            onDelete={deleteBatch}
          />
        )}
      </section>
    </div>
  )
}
