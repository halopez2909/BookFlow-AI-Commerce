import os

os.makedirs("frontend-bookflow/src/tests", exist_ok=True)

# Test EnrichmentBadge
badge_test = """import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import EnrichmentBadge from '../components/catalog/EnrichmentBadge'

describe('EnrichmentBadge', () => {
  it('muestra badge Enriquecido cuando isEnriched es true', () => {
    render(<EnrichmentBadge isEnriched={true} />)
    expect(screen.getByText(/Enriquecido/i)).toBeDefined()
  })

  it('muestra badge Basico cuando isEnriched es false', () => {
    render(<EnrichmentBadge isEnriched={false} />)
    expect(screen.getByText(/Basico/i)).toBeDefined()
  })
})
"""

# Test PriceSummary
price_test = """import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import PriceSummary from '../components/catalog/PriceSummary'

describe('PriceSummary', () => {
  it('muestra el precio cuando existe', () => {
    render(<PriceSummary suggestedPrice={25200} />)
    expect(screen.getByText(/25.200/)).toBeDefined()
  })

  it('muestra Precio no disponible cuando es null', () => {
    render(<PriceSummary suggestedPrice={null} />)
    expect(screen.getByText(/Precio no disponible/i)).toBeDefined()
  })

  it('muestra Precio no disponible cuando es undefined', () => {
    render(<PriceSummary />)
    expect(screen.getByText(/Precio no disponible/i)).toBeDefined()
  })
})
"""

# Test BookCard
bookcard_test = """import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import React from 'react'
import BookCard from '../components/catalog/BookCard'
import type { Book } from '../utils/types'

const mockBook: Book = {
  id: '1',
  title: 'The Great Gatsby',
  author: 'F. Scott Fitzgerald',
  publisher: 'Scribner',
  category_id: 'cat-1',
  isbn: '9780743273565',
  enriched_flag: true,
  published_flag: true,
  cover_url: 'https://covers.openlibrary.org/b/id/10590366-M.jpg',
  suggested_price: 18900,
  description: 'A novel about the American dream',
}

const mockBookBasic: Book = {
  id: '2',
  title: 'Unknown Book',
  author: 'Unknown Author',
  publisher: 'Publisher',
  category_id: 'cat-1',
  enriched_flag: false,
  published_flag: true,
  cover_url: null,
  suggested_price: null,
}

describe('BookCard', () => {
  it('renderiza titulo del libro', () => {
    render(<BookCard book={mockBook} />)
    expect(screen.getByText('The Great Gatsby')).toBeDefined()
  })

  it('renderiza portada real cuando cover_url existe', () => {
    render(<BookCard book={mockBook} />)
    const img = document.querySelector('img')
    expect(img).toBeDefined()
    expect(img?.src).toContain('openlibrary')
  })

  it('muestra placeholder cuando no hay cover_url', () => {
    render(<BookCard book={mockBookBasic} />)
    const img = document.querySelector('img')
    expect(img).toBeNull()
  })

  it('muestra badge Enriquecido para libros enriquecidos', () => {
    render(<BookCard book={mockBook} />)
    expect(screen.getByText(/Enriquecido/i)).toBeDefined()
  })

  it('muestra badge Basico para libros no enriquecidos', () => {
    render(<BookCard book={mockBookBasic} />)
    expect(screen.getByText(/Basico/i)).toBeDefined()
  })

  it('muestra precio cuando existe', () => {
    render(<BookCard book={mockBook} />)
    expect(screen.getByText(/18.900/)).toBeDefined()
  })

  it('muestra Precio no disponible cuando no hay precio', () => {
    render(<BookCard book={mockBookBasic} />)
    expect(screen.getByText(/Precio no disponible/i)).toBeDefined()
  })
})
"""

# Test FilterBar
filterbar_test = """import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import React from 'react'
import FilterBar from '../components/catalog/FilterBar'

describe('FilterBar', () => {
  it('renderiza input de busqueda', () => {
    render(<FilterBar title="" onTitleChange={() => {}} />)
    expect(screen.getByPlaceholderText(/Titulo o autor/i)).toBeDefined()
  })

  it('llama onTitleChange al escribir', () => {
    const onChange = vi.fn()
    render(<FilterBar title="" onTitleChange={onChange} />)
    fireEvent.change(screen.getByPlaceholderText(/Titulo o autor/i), { target: { value: 'Gatsby' } })
    expect(onChange).toHaveBeenCalledWith('Gatsby')
  })

  it('renderiza filtros de precio min y max', () => {
    render(<FilterBar title="" onTitleChange={() => {}} />)
    expect(screen.getByPlaceholderText('Min')).toBeDefined()
    expect(screen.getByPlaceholderText('Max')).toBeDefined()
  })

  it('renderiza checkbox de disponibilidad', () => {
    render(<FilterBar title="" onTitleChange={() => {}} />)
    expect(screen.getByText(/Solo disponibles/i)).toBeDefined()
  })

  it('llama onAvailableChange al marcar checkbox', () => {
    const onAvailable = vi.fn()
    render(<FilterBar title="" onTitleChange={() => {}} onAvailableChange={onAvailable} />)
    fireEvent.click(screen.getByRole('checkbox'))
    expect(onAvailable).toHaveBeenCalledWith(true)
  })
})
"""

with open("frontend-bookflow/src/tests/EnrichmentBadge.test.tsx", "w", encoding="utf-8") as f:
    f.write(badge_test)

with open("frontend-bookflow/src/tests/PriceSummary.test.tsx", "w", encoding="utf-8") as f:
    f.write(price_test)

with open("frontend-bookflow/src/tests/BookCard.test.tsx", "w", encoding="utf-8") as f:
    f.write(bookcard_test)

with open("frontend-bookflow/src/tests/FilterBar.test.tsx", "w", encoding="utf-8") as f:
    f.write(filterbar_test)

print("Tests created!")
