import os

# BookDetailPage.tsx
book_detail = """import React from 'react'
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
"""

# CatalogPage.tsx
catalog_page = """import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCatalog } from '../../hooks/useCatalog'
import BookCard from '../../components/catalog/BookCard'
import SkeletonCard from '../../components/catalog/SkeletonCard'
import FilterBar from '../../components/catalog/FilterBar'
import EmptyState from '../../components/shared/EmptyState'

export default function CatalogPage() {
  const navigate = useNavigate()
  const { data, isLoading, isError, refetch, filters, setFilters, fetchNextPage } = useCatalog()
  const [titleInput, setTitleInput] = useState('')

  function handleTitleChange(v: string) {
    setTitleInput(v)
    setFilters({ ...filters, title: v })
  }

  return (
    <div style={{ padding: 24, maxWidth: 1100, margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>BookFlow Catalog</h1>
        <a href="/login" style={{ fontSize: 13, color: '#555' }}>Admin Login</a>
      </div>
      <FilterBar title={titleInput} onTitleChange={handleTitleChange} />
      {isError && <EmptyState message="Could not load catalog." onRetry={() => refetch()} />}
      {isLoading && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16 }}>
          {Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      )}
      {!isLoading && !isError && data?.items?.length === 0 && (
        <EmptyState message="No books found. Try a different search." />
      )}
      {!isLoading && !isError && data?.items && data.items.length > 0 && (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16 }}>
            {data.items.map((book) => (
              <BookCard key={book.id} book={book} onClick={() => navigate('/catalog/' + book.id)} />
            ))}
          </div>
          {data.items.length < data.total && (
            <div style={{ textAlign: 'center', marginTop: 24 }}>
              <button onClick={fetchNextPage} style={{ padding: '10px 24px', cursor: 'pointer' }}>Load More</button>
            </div>
          )}
          <div style={{ marginTop: 12, color: '#888', fontSize: 13, textAlign: 'center' }}>
            Showing {data.items.length} of {data.total} books
          </div>
        </>
      )}
    </div>
  )
}
"""

# useBookDetail.ts
use_book_detail = """import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { Book } from '../utils/types'

export function useBookDetail(bookId?: string) {
  return useQuery<Book, Error>({
    queryKey: ['catalog', 'books', bookId],
    queryFn: async () => {
      const { data } = await api.get('/api/catalog/books/' + bookId)
      return data
    },
    enabled: !!bookId,
    staleTime: 1000 * 60,
    retry: 1,
  })
}
"""

# useCatalog.ts
use_catalog = """import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { Book } from '../utils/types'
import { useDebounce } from './useDebounce'

type Filters = { title?: string; category_id?: string }
type CatalogResponse = { items: Book[]; total: number; page: number; page_size: number }

export function useCatalog() {
  const [filters, setFilters] = useState<Filters>({})
  const [page, setPage] = useState(1)
  const PAGE_SIZE = 20
  const debouncedTitle = useDebounce(filters.title, 300)

  const query = useQuery<CatalogResponse, Error>({
    queryKey: ['catalog', 'books', debouncedTitle, filters.category_id, page],
    queryFn: async () => {
      const params: Record<string, any> = { page, page_size: PAGE_SIZE }
      if (debouncedTitle) params.title = debouncedTitle
      if (filters.category_id) params.category_id = filters.category_id
      const { data } = await api.get('/api/catalog/books', { params })
      return data
    },
    staleTime: 1000 * 60,
    retry: 1,
  })

  return {
    ...query,
    filters,
    setFilters,
    page,
    fetchNextPage: () => setPage(p => p + 1),
    PAGE_SIZE,
  }
}
"""

os.makedirs('src/pages/catalog', exist_ok=True)
os.makedirs('src/hooks', exist_ok=True)

with open('src/pages/catalog/BookDetailPage.tsx', 'w', encoding='utf-8') as f:
    f.write(book_detail)
print('BookDetailPage.tsx created')

with open('src/pages/catalog/CatalogPage.tsx', 'w', encoding='utf-8') as f:
    f.write(catalog_page)
print('CatalogPage.tsx created')

with open('src/hooks/useBookDetail.ts', 'w', encoding='utf-8') as f:
    f.write(use_book_detail)
print('useBookDetail.ts created')

with open('src/hooks/useCatalog.ts', 'w', encoding='utf-8') as f:
    f.write(use_catalog)
print('useCatalog.ts created')

print('All files created successfully!')
