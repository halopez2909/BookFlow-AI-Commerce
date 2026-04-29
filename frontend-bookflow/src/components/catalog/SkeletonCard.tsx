import React from 'react'

export default function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-cover" />
      <div style={{ padding: '14px' }}>
        <div className="skeleton skeleton-line" />
        <div className="skeleton skeleton-line short" />
      </div>
    </div>
  )
}
