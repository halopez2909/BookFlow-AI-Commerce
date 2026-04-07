import React from 'react'
import type { ImportBatch } from '../../utils/types'

type Props = {
  batches: ImportBatch[] | undefined
  loading?: boolean
  onRowClick?: (id: string) => void
  onDelete?: (id: string, fileName: string) => void
}

export default function BatchTable({ batches, loading, onRowClick, onDelete }: Props) {
  if (loading) return <div>Loading batches...</div>
  if (!batches || batches.length === 0) return <div>No batches found</div>

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          <th style={{ textAlign: 'left', padding: 8 }}>Archivo</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Fecha</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Filas</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Válidas</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Inválidas</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Estado</th>
          <th style={{ textAlign: 'center', padding: 8 }}>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {batches.map((b) => (
          <tr
            key={b.id}
            onClick={() => onRowClick && onRowClick(b.id)}
            style={{ cursor: onRowClick ? 'pointer' : 'default', borderTop: '1px solid #eee' }}
          >
            <td style={{ padding: 8 }}>{b.file_name}</td>
            <td style={{ padding: 8 }}>{new Date(b.upload_date).toLocaleString()}</td>
            <td style={{ padding: 8, textAlign: 'right' }}>{b.processed_rows}</td>
            <td style={{ padding: 8, textAlign: 'right' }}>{b.valid_rows}</td>
            <td style={{ padding: 8, textAlign: 'right' }}>{b.invalid_rows}</td>
            <td style={{ padding: 8 }}>{b.status}</td>
            <td style={{ padding: 8, textAlign: 'center' }}>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  onDelete && onDelete(b.id, b.file_name)
                }}
              >
                Eliminar
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
