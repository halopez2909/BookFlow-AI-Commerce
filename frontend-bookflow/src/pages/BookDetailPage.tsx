import { useParams, Link } from 'react-router-dom';
import { EnrichmentBadge } from '../components/catalog/EnrichmentBadge';
import { PriceSummary } from '../components/catalog/PriceSummary';
import { type Book } from '../types/catalog';
// 1. IMPORTANTE: Importa la lista MOCK_BOOKS desde donde la tengas centralizada
import { MOCK_BOOKS } from '../data/books'; 

export const BookDetailPage = () => {
  // 2. Extraemos el ID de la URL
  const { id } = useParams();

  // 3. Buscamos el libro real comparando el ID de la URL con el ID de la lista
  const book = MOCK_BOOKS.find((b) => b.id === id);

  // 4. Manejo de error si el ID no existe
  if (!book) {
    return (
      <div className="max-w-4xl mx-auto p-6 text-center mt-10">
        <h1 className="text-2xl font-bold mb-4">Libro no encontrado</h1>
        <Link to="/" className="text-blue-500 hover:underline">Volver al catálogo</Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md mt-6">
      <Link to="/" className="text-blue-500 hover:underline mb-6 inline-block">&larr; Volver al catálogo</Link>
      
      <div className="flex flex-col md:flex-row gap-8">
        <div className="md:w-1/3">
          <img 
            src={book.cover_url || 'https://via.placeholder.com/400x600?text=Sin+Portada'} 
            alt={book.title} 
            className="w-full rounded-lg shadow-lg"
          />
        </div>
        
        <div className="md:w-2/3 flex flex-col gap-4">
          <div className="flex items-center gap-3">
            <EnrichmentBadge isEnriched={book.enriched_flag} />
            <span className={`px-2 py-1 text-xs font-bold rounded-full ${book.available ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-700'}`}>
              {book.available ? 'Con Stock' : 'Sin Stock'}
            </span>
            <span className="px-2 py-1 text-xs font-bold rounded-full bg-purple-100 text-purple-700">
              {book.condition}
            </span>
          </div>
          
          <h1 className="text-3xl font-bold">{book.title}</h1>
          <p className="text-xl text-gray-600">{book.author}</p>
          <span className="text-sm font-semibold text-blue-500 uppercase tracking-wider">{book.category}</span>
          
          <div className="my-4 p-4 bg-gray-50 rounded border">
             <PriceSummary price={book.suggested_price} explanation={book.price_explanation} />
          </div>

          <div>
            <h3 className="font-bold text-lg border-b pb-2 mb-2">Descripción</h3>
            <p className="text-gray-700 leading-relaxed">
              {book.description || 'Sin descripción disponible.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};