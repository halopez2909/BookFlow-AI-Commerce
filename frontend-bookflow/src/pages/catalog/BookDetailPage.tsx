import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { useBookDetail } from '../../hooks/useBookDetail'

export default function BookDetailPage() {
  const { id } = useParams()
  const { data: book, isLoading, isError } = useBookDetail(id)

  if (isLoading) return <div style={{ padding: 24 }}>Loading...</div>
  if (isError || !book) return (
    <div style={{ padding: 24 }}>
      <Link to="/catalog">Back to catalog</Link>
    </div>
  )

  return (
    <div style={{ padding: 24, maxWidth: 700, margin: '0 auto' }}>
      <Link to="/catalog" style={{ fontSize: 13, color: '#555', display: 'block', marginBottom: 16 }}>
        Back to catalog
      </Link>
      <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
        {book.cover_url && (
          <img src={book.cover_url} alt={book.title}
            style={{ width: 180, height: 240, objectFit: 'cover', borderRadius: 8 }} />
        )}
        <div style={{ flex: 1, minWidth: 220 }}>
          <h1 style={{ margin: '0 0 8px' }}>{book.title}</h1>
          <div><b>Author:</b> {book.author}</div>
          <div><b>Publisher:</b> {book.publisher}</div>
          {book.publication_year && <div><b>Year:</b> {book.publication_year}</div>}
          {book.isbn && <div><b>ISBN:</b> {book.isbn}</div>}
          {book.issn && <div><b>ISSN:</b> {book.issn}</div>}
          {book.description && <div style={{ marginTop: 16 }}>{book.description}</div>}
          <div style={{ marginTop: 16 }}>
            {book.published_flag
              ? <span style={{ background: '#e6f4ea', color: '#2d7a3a', padding: '4px 12px', borderRadius: 12 }}>Available</span>
              : <span style={{ background: '#fce8e8', color: '#c0392b', padding: '4px 12px', borderRadius: 12 }}>Not Available</span>
            }
          </div>
        </div>
      </div>
    </div>
  )
}
