import { useInfiniteQuery } from '@tanstack/react-query';

export interface Book {
  id: string;
  title: string;
  author: string;
  category: string;
  imageUrl: string;
  available: boolean;
}

const MOCK_BOOKS: Book[] = [
  { 
    id: '1', 
    title: 'Cien años de soledad', 
    author: 'Gabriel García Márquez', 
    category: 'Novela', 
    imageUrl: 'https://picsum.photos/id/101/400/600',
    available: true 
  },
  { 
    id: '2', 
    title: 'Clean Code', 
    author: 'Robert C. Martin', 
    category: 'Tecnología', 
    imageUrl: 'https://m.media-amazon.com/images/I/41xShlnTZTL._SX376_BO1,204,203,200_.jpg',
    available: true 
  },
  { 
    id: '3', 
    title: 'El Principito', 
    author: 'Antoine de Saint-Exupéry', 
    category: 'Infantil', 
    imageUrl: 'https://picsum.photos/id/201/400/600',
    available: true 
  },
  { 
    id: '4', 
    title: 'Calculo de una variable', 
    author: 'James Stewart', 
    category: 'Académico', 
    imageUrl: 'https://picsum.photos/id/301/400/600',
    available: false 
  },
];

export const useCatalog = (title: string, categoryId: string) => {
  return useInfiniteQuery({
    queryKey: ['catalog', title, categoryId],
    queryFn: async ({ pageParam = 1 }) => {
      await new Promise(resolve => setTimeout(resolve, 800));

      const filtered = MOCK_BOOKS.filter(book => {
        // .trim() elimina espacios accidentales al inicio o final
        const searchTerm = title.trim().toLowerCase();
        
        // CORRECCIÓN: Usamos .startsWith() para que sea exacto al inicio
        const matchesTitle = book.title.toLowerCase().startsWith(searchTerm);
        
        const matchesCategory = categoryId === '' || book.category === categoryId;
        
        return matchesTitle && matchesCategory;
      });

      return {
        books: filtered,
        nextPage: null
      };
    },
    getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    initialPageParam: 1,
  });
};