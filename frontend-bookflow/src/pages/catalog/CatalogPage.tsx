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
    <>
      <nav className="navbar">
        <div className="navbar-brand">
          Book<span>Flow</span>
        </div>
        <div className="navbar-actions">
          <a href="/login" className="btn btn-ghost" style={{ fontSize: 13 }}>
            Admin
          </a>
        </div>
      </nav>

      <div className="page-container">
        <div className="catalog-hero animate-in">
          <h1>Discover Your Next Read</h1>
          <p>{data?.total ? `${data.total} books available` : 'Explore our curated collection'}</p>
        </div>

        <FilterBar title={titleInput} onTitleChange={handleTitleChange} />

        {isError && (
          <div className="empty-state">
            <div className="empty-state-icon">!</div>
            <h3>Could not load catalog</h3>
            <p>Something went wrong. Please try again.</p>
            <button className="btn btn-primary" onClick={() => refetch()}>Retry</button>
          </div>
        )}

        {isLoading && (
          <div className="books-grid">
            {Array.from({ length: 12 }).map((_, i) => <SkeletonCard key={i} />)}
          </div>
        )}

        {!isLoading && !isError && data?.items?.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">📚</div>
            <h3>No books found</h3>
            <p>Try a different search term.</p>
          </div>
        )}

        {!isLoading && !isError && data?.items && data.items.length > 0 && (
          <>
            <div className="books-grid">
              {data.items.map((book, i) => (
                <div key={book.id} style={{ animationDelay: `${i * 30}ms` }}>
                  <BookCard book={book} onClick={() => navigate('/catalog/' + book.id)} />
                </div>
              ))}
            </div>
            {data.items.length < data.total && (
              <div className="load-more-section">
                <button className="btn btn-ghost" onClick={fetchNextPage}>Load more books</button>
              </div>
            )}
            <div className="books-count">Showing {data.items.length} of {data.total} books</div>
          </>
        )}
      </div>
    </>
  )
}
