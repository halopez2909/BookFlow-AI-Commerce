import { useInfiniteQuery } from '@tanstack/react-query';
import { type Book } from '../types/catalog';
// 1. IMPORTACIÓN CLAVE: Traemos los libros desde el archivo central
import { MOCK_BOOKS } from '../data/books'; 

export const useCatalog = (
  title: string, 
  categoryId: string, 
  availableOnly: boolean, 
  minPrice: number, 
  maxPrice: number
) => {
  return useInfiniteQuery({
    queryKey: ['catalog', title, categoryId, availableOnly, minPrice, maxPrice],
    queryFn: async ({ pageParam = 1 }) => {
      // Simulamos latencia de red
      await new Promise(resolve => setTimeout(resolve, 500));

      const filtered = MOCK_BOOKS.filter(book => {
        const searchTerm = title.toLowerCase();
        const matchesTitle = book.title.toLowerCase().includes(searchTerm);
        const matchesCategory = categoryId === '' || book.category === categoryId;
        const matchesAvailability = availableOnly ? book.available : true;
        
        const price = book.suggested_price ?? 0;
        const matchesMinPrice = minPrice > 0 ? price >= minPrice : true;
        const matchesMaxPrice = maxPrice > 0 ? price <= maxPrice : true;

        return matchesTitle && matchesCategory && matchesAvailability && matchesMinPrice && matchesMaxPrice;
      });

      return { books: filtered, nextPage: null };
    },
    getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    initialPageParam: 1,
  });
};