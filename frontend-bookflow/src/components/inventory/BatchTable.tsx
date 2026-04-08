import React from 'react'
import type { ImportBatch } from '../../utils/types'

type Props = {
  batches: ImportBatch[] | undefined
  loading?: boolean
  onRowClick?: (id: string) => void
}

export default function BatchTable({ batches, loading, onRowClick }: Props) {
  if (loading) return <div>Loading batches...</div>
  if (!batches || batches.length === 0) return <div>No batches found</div>

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ background: '#f5f5f5' }}>
          <th style={{ textAlign: 'left', padding: 8 }}>File</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Date</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Total Rows</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Valid</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Invalid</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Success %</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Status</th>
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
            <td style={{ padding: 8, textAlign: 'right' }}>{b.total_rows}</td>
            <td style={{ padding: 8, textAlign: 'right', color: 'green' }}>{b.valid_rows}</td>
            <td style={{ padding: 8, textAlign: 'right', color: 'crimson' }}>{b.invalid_rows}</td>
            <td style={{ padding: 8, textAlign: 'right' }}>{b.success_percentage ?? '-'}%</td>
            <td style={{ padding: 8 }}>{b.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
