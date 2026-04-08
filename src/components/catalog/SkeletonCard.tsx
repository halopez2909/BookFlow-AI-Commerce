export const SkeletonCard = () => {
  return (
    <div className="border rounded-lg p-4 shadow-sm bg-white animate-pulse">
      {/* Espacio para la imagen */}
      <div className="h-48 bg-gray-200 rounded-md mb-4"></div>
      
      {/* Línea para el título */}
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
      
      {/* Línea para el autor */}
      <div className="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
      
      {/* Botón/Tag inferior */}
      <div className="flex justify-between items-center">
        <div className="h-6 bg-gray-200 rounded w-20"></div>
        <div className="h-4 bg-gray-200 rounded w-16"></div>
      </div>
    </div>
  );
};