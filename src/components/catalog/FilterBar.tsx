import { useState, useEffect } from 'react';
import { useDebounce } from '../../hooks/useDebounce';

// Definimos la interfaz para las "Props" (lo que recibe el componente)
interface FilterBarProps {
  onFilterChange: (val: string) => void;
}

export const FilterBar = ({ onFilterChange }: FilterBarProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useDebounce(searchTerm, 300);

  useEffect(() => {
    onFilterChange(debouncedSearch);
  }, [debouncedSearch, onFilterChange]);

  return (
    <div className="flex gap-4 mb-8">
      <input
        type="text"
        placeholder="Buscar por título..."
        className="border p-2 rounded w-full text-black" // Agregué text-black por si el fondo es oscuro
        onChange={(e) => setSearchTerm(e.target.value)}
        value={searchTerm} // Es mejor que sea un input controlado
      />
      <select className="border p-2 rounded text-black">
        <option value="">Todas las categorías</option>
      </select>
    </div>
  );
};