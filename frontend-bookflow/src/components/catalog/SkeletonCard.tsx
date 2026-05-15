import React from 'react'
export default function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-img" />
      <div style={{padding:14}}>
        <div className="skeleton skeleton-line" style={{marginBottom:6}} />
        <div className="skeleton skeleton-line" />
        <div className="skeleton skeleton-line short" />
        <div className="skeleton skeleton-line xshort" />
      </div>
    </div>
  )
}
