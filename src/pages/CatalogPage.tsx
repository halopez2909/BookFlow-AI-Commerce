import { useState } from 'react';
import { useCatalog } from '../hooks/useCatalog';
import { BookCard } from '../components/catalog/BookCard';
import { FilterBar } from '../components/catalog/FilterBar';
import { SkeletonCard } from '../components/catalog/SkeletonCard';
import { EmptyState } from '../components/shared/EmptyState';

export const CatalogPage = () => {
  // Estados para los filtros
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryId, setCategoryId] = useState('');

  // Usamos nuestro hook inteligente
  const { 
    data, 
    isLoading, 
    isError, 
    fetchNextPage, 
    hasNextPage, 
    isFetchingNextPage 
  } = useCatalog(searchTerm, categoryId);

  // 1. Estado de Error
  if (isError) {
    return (
      <div className="text-center p-20">
        <h2 className="text-2xl font-bold text-red-600">¡Ups! Algo salió mal</h2>
        <p className="text-gray-600">No pudimos conectar con el servidor.</p>
        <button 
        onClick={() => window.location.reload()}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
        >
       Reintentar
       </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Catálogo de Libros</h1>
        <p className="text-gray-500">Explora nuestra colección disponible.</p>
      </header>

      {/* Barra de Filtros */}
      <FilterBar onFilterChange={setSearchTerm} />

      {/* Grid de Libros o Skeletons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {isLoading ? (
          // Mostramos 8 esqueletos mientras carga la primera vez
          Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)
        ) : data?.pages[0].books.length === 0 ? (
          // Si no hay resultados
          <div className="col-span-full">
            <EmptyState message={`No hay libros que coincidan con "${searchTerm}"`} />
          </div>
        ) : (
          // Mapeamos las páginas de libros (Infinite Query)
          data?.pages.map((page) =>
            page.books.map((book: any) => (
              <BookCard key={book.id} book={book} />
            ))
          )
        )}
      </div>

      {/* Botón Cargar Más */}
      {hasNextPage && (
        <div className="flex justify-center mt-12 mb-20">
          <button
            onClick={() => fetchNextPage()}
            disabled={isFetchingNextPage}
            className="bg-white border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-full font-bold hover:bg-blue-50 transition-colors disabled:opacity-50"
          >
            {isFetchingNextPage ? 'Cargando más...' : 'Cargar más libros'}
          </button>
        </div>
      )}
    </div>
  );
};