import { useState } from 'react';
import { useCatalog } from '../hooks/useCatalog';
import { BookCard } from '../components/catalog/BookCard';
import { FilterBar } from '../components/catalog/FilterBar';
import { SkeletonCard } from '../components/catalog/SkeletonCard';

export const CatalogPage = () => {
  // 1. Estados para los filtros (obligatorios para el Sprint 2)
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('');
  const [availableOnly, setAvailableOnly] = useState(false);
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(0);

  // 2. Llamada al hook con todos los parámetros
  const { 
    data, 
    fetchNextPage, 
    hasNextPage, 
    isLoading 
  } = useCatalog(
    searchTerm, 
    category, 
    availableOnly, 
    minPrice, 
    maxPrice
  );

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Catálogo de Libros</h1>

      {/* 3. FilterBar con todas las funciones de actualización de estado */}
      <FilterBar 
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        category={category}
        setCategory={setCategory}
        availableOnly={availableOnly}
        setAvailableOnly={setAvailableOnly}
        minPrice={minPrice}
        setMinPrice={setMinPrice}
        maxPrice={maxPrice}
        setMaxPrice={setMaxPrice}
      />

      {/* 4. Renderizado de la cuadrícula del catálogo */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {isLoading ? (
          // Muestra los esqueletos de carga con espacio para imagen
          Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)
        ) : (
          data?.pages.map((page) =>
            page.books.map((book) => (
              <BookCard key={book.id} book={book} />
            ))
          )
        )}
      </div>

      {/* 5. Control de paginación */}
      {hasNextPage && (
        <div className="flex justify-center mt-8">
          <button 
            onClick={() => fetchNextPage()}
            className="bg-gray-800 text-white px-6 py-2 rounded-lg hover:bg-gray-900 transition-colors"
          >
            Cargar más libros
          </button>
        </div>
      )}
    </div>
  );
};