import React from 'react'
import type { PricingDecision, PricingExplanation } from '../../utils/types'

type Props = {
  decision: PricingDecision
}

function isStructured(
  e: PricingExplanation | string | undefined
): e is PricingExplanation {
  return typeof e === 'object' && e !== null && 'summary' in e
}

function Section({
  title,
  children,
}: {
  title: string
  children: React.ReactNode
}) {
  return (
    <div style={{ marginBottom: 12 }}>
      <h4 style={{ margin: '4px 0', fontSize: 13, color: '#334155' }}>
        {title}
      </h4>
      <div style={{ fontSize: 14, color: '#0f172a' }}>{children}</div>
    </div>
  )
}

export default function ExplanationPanel({ decision }: Props) {
  const exp = decision.explanation

  return (
    <div
      data-testid="explanation-panel"
      style={{
        background: '#f8fafc',
        border: '1px solid #e2e8f0',
        borderRadius: 8,
        padding: 16,
      }}
    >
      <h3 style={{ marginTop: 0 }}>¿Por qué este precio?</h3>

      <Section title="Resumen">
        {isStructured(exp) ? exp.summary : String(exp || '—')}
      </Section>

      {isStructured(exp) && exp.method && (
        <Section title="Método">{exp.method}</Section>
      )}

      {isStructured(exp) && exp.factors && exp.factors.length > 0 && (
        <Section title="Factores considerados">
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {exp.factors.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </Section>
      )}

      <Section title="Parámetros de cálculo">
        <div>
          <strong>Factor de condición:</strong> {decision.condition_factor}
        </div>
        <div>
          <strong>Cantidad de referencias:</strong> {decision.reference_count}
        </div>
        <div>
          <strong>Precio sugerido:</strong>{' '}
          {(decision.currency || 'ARS') +
            ' ' +
            decision.suggested_price.toLocaleString('es-AR')}
        </div>
      </Section>

      {decision.sources?.length > 0 && (
        <Section title="Fuentes usadas">
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {decision.sources.map((s, i) => (
              <li key={i}>
                {s.name}
                {typeof s.price === 'number'
                  ? ` — ${decision.currency || 'ARS'} ${s.price.toLocaleString('es-AR')}`
                  : ''}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {isStructured(exp) && exp.notes && (
        <Section title="Notas">{exp.notes}</Section>
      )}
    </div>
  )
}