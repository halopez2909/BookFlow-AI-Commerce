import React from 'react'
import type { Book } from '../../utils/types'

type Props = {
  book: Book
  onClick?: () => void
}

export default function BookCard({ book, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      style={{
        border: '1px solid #eee',
        borderRadius: 8,
        padding: 16,
        cursor: onClick ? 'pointer' : 'default',
        display: 'flex',
        flexDirection: 'column',
        gap: 8,
        background: '#fff',
        boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
        transition: 'box-shadow 0.2s',
      }}
    >
      {book.cover_url && (
        <img
          src={book.cover_url}
          alt={book.title}
          style={{ width: '100%', height: 180, objectFit: 'cover', borderRadius: 4 }}
        />
      )}
      <div style={{ fontWeight: 600, fontSize: 15 }}>{book.title}</div>
      <div style={{ color: '#555', fontSize: 13 }}>{book.author}</div>
      <div style={{ color: '#888', fontSize: 12 }}>{book.publisher}</div>
      {book.published_flag && (
        <span style={{ background: '#e6f4ea', color: '#2d7a3a', padding: '2px 8px', borderRadius: 12, fontSize: 11, alignSelf: 'flex-start' }}>
          Available
        </span>
      )}
    </div>
  )
}
