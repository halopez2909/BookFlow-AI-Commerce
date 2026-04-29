import React from 'react'

type Props = {
  title: string
  onTitleChange: (v: string) => void
}

export default function FilterBar({ title, onTitleChange }: Props) {
  return (
    <div className="filter-bar">
      <div className="filter-input-wrapper">
        <span className="filter-input-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
        </span>
        <input
          type="text"
          placeholder="Search by title or author..."
          value={title}
          onChange={(e) => onTitleChange(e.target.value)}
        />
      </div>
    </div>
  )
}
