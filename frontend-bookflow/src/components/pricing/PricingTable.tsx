import React from 'react'
import type { PricingDecision } from '../../utils/types'
import PricingStatusBadge from './PricingStatusBadge'

type Props = {
  prices: PricingDecision[] | undefined
  loading?: boolean
  onRowClick?: (decision: PricingDecision) => void
  onRecalculate?: (decision: PricingDecision) => void
  recalculatingId?: string | null
}

function formatMoney(value: number | undefined, currency = 'ARS') {
  if (value === undefined || value === null || Number.isNaN(value)) return '-'
  return `${currency} ${value.toLocaleString('es-AR')}`
}

function SkeletonRow() {
  return (
    <tr>
      {Array.from({ length: 7 }).map((_, i) => (
        <td key={i} style={{ padding: 8 }}>
          <div
            data-testid="pricing-skeleton"
            style={{
              height: 14,
              background: '#eee',
              borderRadius: 4,
              animation: 'pulse 1.2s ease-in-out infinite',
            }}
          />
        </td>
      ))}
    </tr>
  )
}

export default function PricingTable({
  prices,
  loading,
  onRowClick,
  onRecalculate,
  recalculatingId,
}: Props) {
  return (
    <table
      data-testid="pricing-table"
      style={{ width: '100%', borderCollapse: 'collapse' }}
    >
      <thead>
        <tr style={{ background: '#f5f5f5' }}>
          <th style={{ textAlign: 'left', padding: 8 }}>Título</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Autor</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Condición</th>
          <th style={{ textAlign: 'right', padding: 8 }}>Precio sugerido IA</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Fuentes</th>
          <th style={{ textAlign: 'left', padding: 8 }}>Estado</th>
          <th style={{ textAlign: 'center', padding: 8 }}>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {loading && (
          <>
            <SkeletonRow />
            <SkeletonRow />
            <SkeletonRow />
          </>
        )}

        {!loading &&
          (prices ?? []).map((p) => {
            const shownPrice = p.manual_price ?? p.suggested_price
            const isAdjusted =
              p.manual_price !== undefined && p.manual_price !== null
            return (
              <tr
                key={p.id}
                style={{
                  cursor: onRowClick ? 'pointer' : 'default',
                  borderTop: '1px solid #eee',
                }}
                onClick={() => onRowClick && onRowClick(p)}
              >
                <td style={{ padding: 8 }}>{p.title}</td>
                <td style={{ padding: 8 }}>{p.author}</td>
                <td style={{ padding: 8 }}>{p.condition}</td>
                <td style={{ padding: 8, textAlign: 'right' }}>
                  <strong>{formatMoney(shownPrice, p.currency)}</strong>
                  {isAdjusted && (
                    <span
                      data-testid="adjusted-badge"
                      style={{
                        marginLeft: 8,
                        padding: '2px 6px',
                        borderRadius: 8,
                        background: '#fee2e2',
                        color: '#991b1b',
                        fontSize: 11,
                        fontWeight: 600,
                      }}
                    >
                      Ajustado
                    </span>
                  )}
                </td>
                <td style={{ padding: 8 }}>
                  {p.sources.length > 0
                    ? p.sources.map((s) => s.name).join(', ')
                    : '-'}
                </td>
                <td style={{ padding: 8 }}>
                  <PricingStatusBadge status={p.status} />
                </td>
                <td style={{ padding: 8, textAlign: 'center' }}>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation()
                      onRecalculate && onRecalculate(p)
                    }}
                    disabled={recalculatingId === p.id}
                    style={{
                      padding: '4px 10px',
                      background: '#0369a1',
                      color: 'white',
                      border: 'none',
                      borderRadius: 6,
                      cursor:
                        recalculatingId === p.id ? 'not-allowed' : 'pointer',
                    }}
                  >
                    {recalculatingId === p.id
                      ? 'Recalculando...'
                      : 'Recalcular'}
                  </button>
                </td>
              </tr>
            )
          })}

        {!loading && (!prices || prices.length === 0) && (
          <tr>
            <td colSpan={7} style={{ padding: 16, textAlign: 'center' }}>
              No hay decisiones de pricing.
            </td>
          </tr>
        )}
      </tbody>
    </table>
  )
}