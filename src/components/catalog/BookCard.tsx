import { type Book } from '../../types/catalog';
import { EnrichmentBadge } from './EnrichmentBadge';
import { Link } from 'react-router-dom';

export const BookCard = ({ book }: { book: Book }) => {
  return (
    <div className="border rounded-lg shadow-sm hover:shadow-md transition-shadow bg-white flex flex-col overflow-hidden">
      <img 
        src={book.cover_url || 'https://via.placeholder.com/400x600?text=Sin+Portada'} 
        alt={book.title} 
        className="w-full h-48 object-cover"
      />
      <div className="p-4 flex flex-col flex-grow gap-2">
        <EnrichmentBadge isEnriched={book.enriched_flag} />
        <h3 className="font-bold text-lg leading-tight mt-1">{book.title}</h3>
        <p className="text-sm text-gray-600">{book.author}</p>
        <span className="text-xs font-semibold text-blue-500 uppercase tracking-wider">{book.category}</span>
        
        <div className="mt-auto pt-4 flex justify-between items-end">
          <span className="font-bold text-gray-800">
            {book.suggested_price ? `$${book.suggested_price}` : 'Precio no disponible'}
          </span>
          <Link 
            to={`/catalog/${book.id}`} 
            className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700 transition-colors"
          >
            Ver detalles
          </Link>
        </div>
      </div>
    </div>
  );
};