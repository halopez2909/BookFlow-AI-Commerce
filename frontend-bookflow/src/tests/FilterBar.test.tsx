import { describe, it, expect, vi } from 'vitest'
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
