interface EmptyStateProps {
  message: string;
}

export const EmptyState = ({ message }: EmptyStateProps) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center border-2 border-dashed border-gray-200 rounded-lg bg-gray-50">
      {/* Un icono grande de un libro o una lupa */}
      <div className="text-6xl mb-4">🔍</div>
      
      <h3 className="text-xl font-semibold text-gray-700">
        No se encontraron resultados
      </h3>
      
      <p className="text-gray-500 mt-2 max-w-xs">
        {message || "Prueba a buscar con otros términos o limpia los filtros."}
      </p>

      <button 
        onClick={() => window.location.reload()} 
        className="mt-6 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md font-medium transition-colors"
      >
        Limpiar búsqueda
      </button>
    </div>
  );
};