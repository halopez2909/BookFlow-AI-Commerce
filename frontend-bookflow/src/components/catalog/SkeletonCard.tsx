import React from 'react'

export default function SkeletonCard() {
  return (
    <div style={{
      border: '1px solid #eee',
      borderRadius: 8,
      padding: 16,
      background: '#fff',
      display: 'flex',
      flexDirection: 'column',
      gap: 8,
    }}>
      <div style={{ height: 180, background: '#f0f0f0', borderRadius: 4, animation: 'pulse 1.5s infinite' }} />
      <div style={{ height: 16, background: '#f0f0f0', borderRadius: 4, width: '80%' }} />
      <div style={{ height: 13, background: '#f0f0f0', borderRadius: 4, width: '60%' }} />
      <div style={{ height: 12, background: '#f0f0f0', borderRadius: 4, width: '40%' }} />
    </div>
  )
}
