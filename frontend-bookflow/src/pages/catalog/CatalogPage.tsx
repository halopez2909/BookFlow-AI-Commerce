import React, { useState } from 'react'
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
