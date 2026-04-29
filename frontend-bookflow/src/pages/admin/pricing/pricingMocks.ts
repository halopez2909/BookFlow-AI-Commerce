import type { PricingDecision } from '../../../utils/types'

// Mocks usados durante la Semana 1 mientras el BFF de pricing
// no está disponible. En Semana 2 se desactivan vía flag.
export const PRICING_MOCKS: PricingDecision[] = [
  {
    id: 'pd-001',
    book_id: 'book-001',
    title: 'Cien años de soledad',
    author: 'Gabriel García Márquez',
    condition: 'Bueno',
    suggested_price: 18500,
    currency: 'ARS',
    condition_factor: 0.9,
    reference_count: 7,
    sources: [
      { name: 'MercadoLibre', url: 'https://mercadolibre.com', price: 19000 },
      { name: 'Cuspide', url: 'https://cuspide.com', price: 18200 },
      { name: 'Google Books', price: 18400 },
    ],
    explanation: {
      summary:
        'El precio sugerido surge del promedio de referencias públicas ajustado por la condición del ejemplar.',
      factors: [
        'Promedio de 7 referencias recientes: 18.533',
        'Factor de condición "Bueno": 0.9',
        'Sin penalización por edición',
      ],
      method: 'Promedio ponderado por condición',
      notes: 'Precio redondeado a múltiplos de 100 ARS.',
    },
    status: 'suggested',
    updated_at: '2026-04-15T10:00:00Z',
  },
  {
    id: 'pd-002',
    book_id: 'book-002',
    title: 'Rayuela',
    author: 'Julio Cortázar',
    condition: 'Muy bueno',
    suggested_price: 22000,
    manual_price: 24500,
    final_price: 24500,
    currency: 'ARS',
    condition_factor: 0.95,
    reference_count: 5,
    sources: [
      { name: 'MercadoLibre', price: 23000 },
      { name: 'Cuspide', price: 21500 },
      { name: 'Prometeo', price: 22500 },
    ],
    explanation: {
      summary:
        'Se priorizó el estado "Muy bueno" y se usaron 5 referencias con baja dispersión.',
      factors: [
        'Promedio de 5 referencias: 22.333',
        'Factor de condición "Muy bueno": 0.95',
        'Dispersión baja entre referencias (stdev < 5%)',
      ],
      method: 'Promedio ajustado por condición',
    },
    status: 'overridden',
    updated_at: '2026-04-16T11:30:00Z',
  },
  {
    id: 'pd-003',
    book_id: 'book-003',
    title: 'El Aleph',
    author: 'Jorge Luis Borges',
    condition: 'Aceptable',
    suggested_price: 9800,
    currency: 'ARS',
    condition_factor: 0.7,
    reference_count: 3,
    sources: [
      { name: 'MercadoLibre', price: 10500 },
      { name: 'Librería de ocasión', price: 9000 },
      { name: 'Google Books', price: 9900 },
    ],
    explanation: {
      summary:
        'Pocos datos disponibles; precio estimado con factor de condición bajo por desgaste.',
      factors: [
        'Promedio de 3 referencias: 9.800',
        'Factor de condición "Aceptable": 0.7',
        'Solo 3 referencias: confianza media',
      ],
      method: 'Promedio ajustado por condición',
      notes: 'Se recomienda revisar manualmente antes de publicar.',
    },
    status: 'pending',
  },
]