export const SkeletonCard = () => {
  return (
    <div className="border rounded-lg shadow-sm bg-white flex flex-col animate-pulse h-full">
      <div className="w-full h-48 bg-gray-200 rounded-t-lg"></div>
      <div className="p-4 flex flex-col gap-3 flex-grow">
        <div className="h-4 bg-gray-200 rounded w-1/3"></div>
        <div className="h-6 bg-gray-200 rounded w-3/4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        <div className="h-10 bg-gray-200 rounded w-full mt-auto"></div>
      </div>
    </div>
  );
};