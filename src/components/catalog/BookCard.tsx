
interface Book {
  id: string;
  title: string;
  author: string;
  imageUrl: string;
  category: string;
}

interface BookCardProps {
  book: Book;
}

export const BookCard = ({ book }: BookCardProps) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
      <img 
        src={book.imageUrl} 
        alt={book.title}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">
          {book.category}
        </span>
        <h3 className="mt-1 text-lg font-bold text-gray-900 leading-tight">
          {book.title}
        </h3>
        <p className="mt-1 text-gray-600 text-sm">
          {book.author}
        </p>
        <button className="mt-4 w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors">
          Ver detalles
        </button>
      </div>
    </div>
  );
};