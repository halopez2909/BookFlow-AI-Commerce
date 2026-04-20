import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { CatalogPage } from './pages/CatalogPage';
import { BookDetailPage } from './pages/BookDetailPage'; // <-- Importa la página de detalle
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-100">
          <Routes>
            {/* Ruta principal: muestra el catálogo */}
            <Route path="/catalog" element={<CatalogPage />} />
            
            {/* Ruta de detalle: el :id es la parte dinámica */}
            <Route path="/catalog/:id" element={<BookDetailPage />} />
            
            {/* Redirigir la raíz al catálogo por defecto */}
            <Route path="/" element={<Navigate to="/catalog" />} />
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;