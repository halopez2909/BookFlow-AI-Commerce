import React from 'react'
import type { PricingStatus } from '../../utils/types'

type Props = {
  status: PricingStatus
}

type BadgeStyle = { label: string; bg: string; fg: string }

const styles: Record<PricingStatus, BadgeStyle> = {
  suggested: { label: 'IA sugerido', bg: '#e0f2fe', fg: '#0369a1' },
  applied: { label: 'Aplicado', bg: '#dcfce7', fg: '#166534' },
  pending: { label: 'Pendiente', bg: '#fef9c3', fg: '#854d0e' },
  overridden: { label: 'Ajustado', bg: '#fee2e2', fg: '#991b1b' },
}

export default function PricingStatusBadge({ status }: Props) {
  const s = styles[status] ?? styles.pending
  return (
    <span
      data-testid={`pricing-badge-${status}`}
      style={{
        display: 'inline-block',
        padding: '2px 8px',
        borderRadius: 12,
        background: s.bg,
        color: s.fg,
        fontSize: 12,
        fontWeight: 600,
        whiteSpace: 'nowrap',
      }}
    >
      {s.label}
    </span>
  )
}