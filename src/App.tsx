import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { CatalogPage } from './pages/CatalogPage';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-100">
        <CatalogPage />
      </div>
    </QueryClientProvider>
  );
}

export default App;