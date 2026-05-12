content = """import React, { useState } from 'react'
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
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <h1>Catalogo de Libros</h1>
      <FilterBar title={titleInput} onTitleChange={handleTitleChange} />
      {isError && <EmptyState message="Error cargando catalogo." onRetry={() => refetch()} />}
      {isLoading && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16 }}>
          {Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      )}
      {!isLoading && !isError && data?.items && data.items.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16 }}>
          {data.items.map((book) => (
            <BookCard key={book.id} book={book} onClick={() => navigate('/catalog/' + book.id)} />
          ))}
        </div>
      )}
    </div>
  )
}
"""
with open('frontend-bookflow/src/pages/catalog/CatalogPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
