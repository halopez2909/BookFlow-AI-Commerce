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
  function handleTitleChange(v: string) { setTitleInput(v); setFilters({ ...filters, title: v }) }
  return (
    <div className="page">
      <div className="catalog-hero">
        <h1>Libreria BookFlow</h1>
        <p>{data?.total ? `${data.total} libros disponibles` : 'Explora nuestra coleccion'}</p>
      </div>
      <FilterBar
        title={titleInput} onTitleChange={handleTitleChange}
        minPrice={filters.min_price} maxPrice={filters.max_price}
        onMinPriceChange={v=>setFilters({...filters,min_price:v})}
        onMaxPriceChange={v=>setFilters({...filters,max_price:v})}
        available={filters.available} onAvailableChange={v=>setFilters({...filters,available:v})}
      />
      {isError && <EmptyState message="No se pudo cargar el catalogo." onRetry={()=>refetch()} />}
      {isLoading && (
        <div className="books-grid">{Array.from({length:12}).map((_,i)=><SkeletonCard key={i} />)}</div>
      )}
      {!isLoading && !isError && data?.items?.length === 0 && <EmptyState message="No se encontraron libros." />}
      {!isLoading && !isError && data?.items && data.items.length > 0 && (
        <>
          <div className="books-grid">
            {data.items.map(book=>(
              <BookCard key={book.id} book={book} onClick={()=>navigate('/catalog/'+book.id)} />
            ))}
          </div>
          {data.items.length < data.total && (
            <div className="load-more">
              <button className="btn btn-ghost" onClick={fetchNextPage}>Cargar mas libros</button>
            </div>
          )}
          <div className="books-count">Mostrando {data.items.length} de {data.total} libros</div>
        </>
      )}
    </div>
  )
}
