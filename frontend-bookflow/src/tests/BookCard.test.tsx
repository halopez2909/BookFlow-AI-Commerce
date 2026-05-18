import { describe, it, expect } from 'vitest'
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
