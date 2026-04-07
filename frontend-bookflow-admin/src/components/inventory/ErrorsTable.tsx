import React from 'react'
import type { BatchError } from '../../hooks/useBatchErrors'

export default function ErrorsTable({ errors }: { errors?: BatchError[] }) {
  if (!errors) return <div>No errors</div>
  if (!Array.isArray(errors)) return <div>Invalid errors data</div>
  if (errors.length === 0) return <div>No errors found</div>

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          <th style={{ textAlign: 'left', padding: 8 }}>Fila</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Tipo</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Mensaje</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Sugerencia</th>
        </tr>
      </thead>
      <tbody>
        {errors.map((e) => (
          <tr key={e.id} style={{ borderTop: '1px solid #eee' }}>
            <td style={{ padding: 8 }}>{e.row_number}</td>
            <td style={{ padding: 8 }}>{e.error_type}</td>
            <td style={{ padding: 8 }}>{e.message}</td>
            <td style={{ padding: 8 }}>{e.fix_hint ?? '-'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
