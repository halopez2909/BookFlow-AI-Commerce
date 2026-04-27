import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PriceOverrideForm from '../src/components/pricing/PriceOverrideForm'

describe('PriceOverrideForm', () => {
  it('muestra error cuando el input está vacío', async () => {
    const user = userEvent.setup()
    render(<PriceOverrideForm onSubmit={vi.fn()} isSaving={false} />)
    await user.click(screen.getByRole('button', { name: /guardar/i }))
    expect(screen.getByRole('alert')).toBeInTheDocument()
  })

  it('muestra error cuando el input no es un número', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()
    render(<PriceOverrideForm onSubmit={onSubmit} isSaving={false} />)
    const input = screen.getByLabelText(/precio manual/i)
    await user.type(input, 'abc')
    await user.click(screen.getByRole('button', { name: /guardar/i }))
    expect(screen.getByRole('alert')).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('muestra error cuando el precio es 0 o negativo', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()
    render(<PriceOverrideForm onSubmit={onSubmit} isSaving={false} />)
    const input = screen.getByLabelText(/precio manual/i)
    await user.type(input, '0')
    await user.click(screen.getByRole('button', { name: /guardar/i }))
    expect(screen.getByRole('alert')).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('llama a onSubmit con el número parseado cuando el input es válido', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()
    render(<PriceOverrideForm onSubmit={onSubmit} isSaving={false} />)
    const input = screen.getByLabelText(/precio manual/i)
    await user.type(input, '25000')
    await user.click(screen.getByRole('button', { name: /guardar/i }))
    expect(onSubmit).toHaveBeenCalledWith(25000)
  })

  it('deshabilita el botón de submit mientras se guarda', () => {
    render(<PriceOverrideForm onSubmit={vi.fn()} isSaving={true} />)
    expect(screen.getByRole('button', { name: /guardando|guardar/i })).toBeDisabled()
  })
})