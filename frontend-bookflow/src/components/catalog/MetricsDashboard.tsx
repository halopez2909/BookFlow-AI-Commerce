import React from 'react'

interface Props {
  total: number
  enriched: number
  withPrice: number
  avgPrice: number
}

export default function MetricsDashboard({ total, enriched, withPrice, avgPrice }: Props) {
  const enrichedPct = total > 0 ? Math.round((enriched / total) * 100) : 0
  const pricedPct = total > 0 ? Math.round((withPrice / total) * 100) : 0

  return (
    <div className="metrics-grid fade-up" style={{ animationDelay: '0.1s' }}>
      <div className="metric-card">
        <div className="metric-label">Total Títulos</div>
        <div className="metric-value metric-accent">{total.toLocaleString('es-CO')}</div>
        <div className="metric-sub">En el catálogo activo</div>
        <div className="metric-icon">◎</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Enriquecidos con IA</div>
        <div className="metric-value">{enrichedPct}<span style={{ fontSize: 18, color: 'var(--text-3)' }}>%</span></div>
        <div className="metric-sub">{enriched} de {total} títulos</div>
        <div className="metric-icon">✦</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Con Precio IA</div>
        <div className="metric-value">{pricedPct}<span style={{ fontSize: 18, color: 'var(--text-3)' }}>%</span></div>
        <div className="metric-sub">{withPrice} títulos valuados</div>
        <div className="metric-icon">◈</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Precio Promedio</div>
        <div className="metric-value" style={{ fontSize: 24 }}>${avgPrice > 0 ? Math.round(avgPrice / 1000) + 'K' : '—'}</div>
        <div className="metric-sub">COP · Sugerido por IA</div>
        <div className="metric-icon">❋</div>
      </div>
    </div>
  )
}
