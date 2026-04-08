import React from 'react'

type Props = {
  title: string
  onTitleChange: (v: string) => void
}

export default function FilterBar({ title, onTitleChange }: Props) {
  return (
    <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap' }}>
      <input
        type="text"
        placeholder="Search by title..."
        value={title}
        onChange={(e) => onTitleChange(e.target.value)}
        style={{ padding: '8px 12px', borderRadius: 6, border: '1px solid #ddd', minWidth: 220, fontSize: 14 }}
      />
    </div>
  )
}
