import React from 'react'
import type { Book } from '../../utils/types'

type Props = {
  book: Book
  onClick?: () => void
}

export default function BookCard({ book, onClick }: Props) {
  const initials = book.title
    .split(' ')
    .slice(0, 2)
    .map((w: string) => w[0])
    .join('')
    .toUpperCase()

  return (
    <div className="book-card" onClick={onClick}>
      {book.cover_url ? (
        <img
          className="book-card-cover"
          src={book.cover_url}
          alt={book.title}
          loading="lazy"
          onError={(e) => {
            const target = e.currentTarget as HTMLImageElement
            target.style.display = 'none'
            const placeholder = target.nextElementSibling as HTMLElement
            if (placeholder) placeholder.style.display = 'flex'
          }}
        />
      ) : null}
      <div
        className="book-card-cover-placeholder"
        style={{ display: book.cover_url ? 'none' : 'flex' }}
      >
        {initials}
      </div>
      <div className="book-card-body">
        <div className="book-card-title">{book.title}</div>
        <div className="book-card-author">{book.author}</div>
        <div className="book-card-publisher">{book.publisher}</div>
        {book.published_flag && (
          <span className="badge badge-available">Available</span>
        )}
      </div>
    </div>
  )
}
