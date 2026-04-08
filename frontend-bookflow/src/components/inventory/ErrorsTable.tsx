import React from 'react'
import type { BatchError } from '../../utils/types'

export default function ErrorsTable({ errors }: { errors?: BatchError[] }) {
  if (!errors || errors.length === 0) return <div>No errors found</div>

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ background: '#f5f5f5' }}>
          <th style={{ textAlign: 'left', padding: 8 }}>Row</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Error Type</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Message</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Fix Hint</th>
        </tr>
      </thead>
      <tbody>
        {errors.map((e) => (
          <tr key={e.id} style={{ borderTop: '1px solid #eee' }}>
            <td style={{ padding: 8 }}>{e.row_number}</td>
            <td style={{ padding: 8 }}>{e.error_type}</td>
            <td style={{ padding: 8 }}>{e.message}</td>
            <td style={{ padding: 8, color: '#666' }}>{e.fix_hint ?? '-'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
