import React from 'react'
type Props = { message: string; onRetry?: () => void }
export default function EmptyState({ message, onRetry }: Props) {
  return (
    <div className="empty-state">
      <div style={{fontSize:40,marginBottom:12,opacity:0.4}}>📚</div>
      <p>{message}</p>
      {onRetry && <button className="btn btn-ghost" onClick={onRetry} style={{marginTop:16}}>Reintentar</button>}
    </div>
  )
}
