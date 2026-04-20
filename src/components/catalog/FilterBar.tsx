interface Props {
  searchTerm: string;
  setSearchTerm: (val: string) => void;
  category: string;
  setCategory: (val: string) => void;
  availableOnly: boolean;
  setAvailableOnly: (val: boolean) => void;
  minPrice: number;
  setMinPrice: (val: number) => void;
  maxPrice: number;
  setMaxPrice: (val: number) => void;
}

export const FilterBar = ({ 
  searchTerm, setSearchTerm, 
  category, setCategory, 
  availableOnly, setAvailableOnly,
  minPrice, setMinPrice,
  maxPrice, setMaxPrice
}: Props) => {
  return (
    <div className="flex flex-col md:flex-row gap-4 mb-6 bg-white p-4 rounded-lg shadow-sm border">
      <input 
        type="text" 
        placeholder="Buscar por título..." 
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="flex-grow border rounded px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
      />
      <select 
        value={category} 
        onChange={(e) => setCategory(e.target.value)}
        className="border rounded px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Todas las categorías</option>
        <option value="Novela">Novela</option>
        <option value="Tecnología">Tecnología</option>
        <option value="Infantil">Infantil</option>
        <option value="Académico">Académico</option>
      </select>
      <div className="flex items-center gap-2">
        <input 
          type="number" 
          placeholder="Min $" 
          value={minPrice || ''}
          onChange={(e) => setMinPrice(Number(e.target.value))}
          className="border rounded px-2 py-2 w-20"
        />
        <span>-</span>
        <input 
          type="number" 
          placeholder="Max $" 
          value={maxPrice || ''}
          onChange={(e) => setMaxPrice(Number(e.target.value))}
          className="border rounded px-2 py-2 w-20"
        />
      </div>
      <label className="flex items-center gap-2 cursor-pointer">
        <input 
          type="checkbox" 
          checked={availableOnly}
          onChange={(e) => setAvailableOnly(e.target.checked)}
          className="w-4 h-4"
        />
        <span className="text-sm font-medium">Solo disponibles</span>
      </label>
    </div>
  );
};