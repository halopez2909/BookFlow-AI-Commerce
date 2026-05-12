content = """import React from 'react'

type Props = {
  message: string
  onRetry?: () => void
}

export default function EmptyState({ message, onRetry }: Props) {
  return (
    <div style={{ textAlign: 'center', padding: 48, color: '#888' }}>
      <p>{message}</p>
      {onRetry && (
        <button onClick={onRetry} style={{ marginTop: 12, padding: '8px 16px', cursor: 'pointer' }}>
          Reintentar
        </button>
      )}
    </div>
  )
}
"""
with open('frontend-bookflow/src/components/shared/EmptyState.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
