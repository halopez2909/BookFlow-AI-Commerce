export interface Book {
  id: string;
  title: string;
  author: string;
  category: string;
  cover_url: string | null;
  description: string | null;
  suggested_price: number | null;
  price_explanation?: string;
  enriched_flag: boolean;
  condition: 'Nuevo' | 'Usado';
  available: boolean;
}