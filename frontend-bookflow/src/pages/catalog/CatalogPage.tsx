import React, { useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCatalog } from '../../hooks/useCatalog'
import BookCard from '../../components/catalog/BookCard'
import SkeletonCard from '../../components/catalog/SkeletonCard'
import FilterBar from '../../components/catalog/FilterBar'
import EmptyState from '../../components/shared/EmptyState'
import LibraryGate from '../../components/shared/LibraryGate'
import MetricsDashboard from '../../components/catalog/MetricsDashboard'

export default function CatalogPage() {
  const navigate = useNavigate()
  const [gateOpen, setGateOpen] = useState(false)
  const [titleInput, setTitleInput] = useState('')
  const { data, isLoading, isError, refetch, filters, setFilters, fetchNextPage } = useCatalog()

  function handleGateOpen() { setGateOpen(true) }

  function handleTitleChange(v: string) {
    setTitleInput(v)
    setFilters({ ...filters, title: v })
  }

  const metrics = useMemo(() => {
    if (!data?.items) return { enriched: 0, withPrice: 0, avgPrice: 0 }
    const items = data.items
    const enriched = items.filter(b => b.enriched_flag).length
    const priced = items.filter(b => b.suggested_price && b.suggested_price > 0)
    const avgPrice = priced.length > 0 ? priced.reduce((s, b) => s + (b.suggested_price || 0), 0) / priced.length : 0
    return { enriched, withPrice: priced.length, avgPrice }
  }, [data?.items])

  if (!gateOpen) return <LibraryGate onOpen={handleGateOpen} />

  return (
    <div className="page">
      <div className="catalog-hero fade-up">
        <div>
          <h1 className="catalog-hero-title">Nuestra <em>Colección</em></h1>
          <p className="catalog-hero-sub">
            {data?.total ? `${data.total} títulos · inteligencia artificial aplicada` : 'Catálogo enriquecido con IA'}
          </p>
        </div>
      </div>

      {!isLoading && data && (
        <MetricsDashboard
          total={data.total}
          enriched={metrics.enriched}
          withPrice={metrics.withPrice}
          avgPrice={metrics.avgPrice}
        />
      )}

      <FilterBar
        title={titleInput} onTitleChange={handleTitleChange}
        minPrice={filters.min_price} maxPrice={filters.max_price}
        onMinPriceChange={v => setFilters({ ...filters, min_price: v })}
        onMaxPriceChange={v => setFilters({ ...filters, max_price: v })}
        available={filters.available} onAvailableChange={v => setFilters({ ...filters, available: v })}
      />

      {isError && <EmptyState message="No se pudo cargar el catálogo." onRetry={() => refetch()} />}
      {isLoading && (
        <div className="books-grid">{Array.from({ length: 12 }).map((_, i) => <SkeletonCard key={i} />)}</div>
      )}
      {!isLoading && !isError && data?.items?.length === 0 && <EmptyState message="No se encontraron libros." />}
      {!isLoading && !isError && data?.items && data.items.length > 0 && (
        <>
          <div className="books-grid">
            {data.items.map((book, i) => (
              <div key={book.id} className="fade-up scale-in" style={{ animationDelay: `${Math.min(i * 0.04, 0.6)}s` }}>
                <BookCard book={book} onClick={() => navigate('/catalog/' + book.id)} />
              </div>
            ))}
          </div>
          {data.items.length < data.total && (
            <div className="load-more">
              <button className="btn btn-ghost" onClick={fetchNextPage}>Cargar más títulos</button>
            </div>
          )}
          <div className="books-count">{data.items.length} de {data.total} títulos</div>
        </>
      )}
    </div>
  )
}
