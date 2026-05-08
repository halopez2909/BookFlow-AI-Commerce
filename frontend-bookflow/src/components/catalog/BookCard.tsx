import React from 'react'
import type { Book } from '../../utils/types'
import EnrichmentBadge from './EnrichmentBadge'
import PriceSummary from './PriceSummary'
type Props = { book: Book; onClick?: () => void }
export default function BookCard({ book, onClick }: Props) {
  const initials = book.title.split(' ').slice(0,2).map((w:string)=>w[0]).join('').toUpperCase()
  return (
    <div className="book-card fade-in" onClick={onClick}>
      {book.cover_url
        ? <img className="book-card-img" src={book.cover_url} alt={book.title} loading="lazy"
            onError={(e)=>{const t=e.currentTarget as HTMLImageElement;t.style.display='none';const p=t.nextElementSibling as HTMLElement;if(p)p.style.display='flex';}} />
        : null}
      <div className="book-card-placeholder" style={{display:book.cover_url?'none':'flex'}}>{initials}</div>
      <div className="book-card-body">
        <EnrichmentBadge isEnriched={book.enriched_flag} />
        <div className="book-card-title">{book.title}</div>
        <div className="book-card-author">{book.author}</div>
        <div className="book-card-footer">
          <PriceSummary suggestedPrice={book.suggested_price} />
          {book.published_flag && <span className="badge badge-available">Disponible</span>}
        </div>
      </div>
    </div>
  )
}
