import React from 'react'

type Props = {
  message?: string
  onRetry?: () => void
}

export default function EmptyState({ message = 'No results found', onRetry }: Props) {
  return (
    <div style={{ textAlign: 'center', padding: 48, color: '#888' }}>
      <div style={{ fontSize: 48, marginBottom: 16 }}>??</div>
      <div style={{ fontSize: 16, marginBottom: 12 }}>{message}</div>
      {onRetry && (
        <button onClick={onRetry} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Retry
        </button>
      )}
    </div>
  )
}
