import React, { useState, useEffect } from 'react'
import { usePricingList } from '../../../hooks/usePricingList'
import { usePricingDetail } from '../../../hooks/usePricingDetail'
import { usePricingOverride } from '../../../hooks/usePricingOverride'
import { usePricingRecalculate } from '../../../hooks/usePricingRecalculate'
import PricingTable from '../../../components/pricing/PricingTable'
import ExplanationPanel from '../../../components/pricing/ExplanationPanel'
import PriceOverrideForm from '../../../components/pricing/PriceOverrideForm'
import { showError } from '../../../utils/toast'
import type { PricingDecision } from '../../../utils/types'

/**
 * Container de la pantalla /admin/pricing.
 * Responsabilidad: integrar hooks y componentes presentacionales.
 * No conoce Axios ni la URL del BFF (Dependency Inversion).
 */
export default function AdminPricing() {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [recalculatingId, setRecalculatingId] = useState<string | null>(null)

  const { prices, isLoading, error } = usePricingList()
  const { detail, isLoading: detailLoading } = usePricingDetail(selectedId)
  const { override, isSaving } = usePricingOverride()
  const { recalculateAsync } = usePricingRecalculate()

  useEffect(() => {
    if (error) showError(`Error cargando pricing: ${error.message}`)
  }, [error])

  function handleRowClick(decision: PricingDecision) {
    setSelectedId(decision.id)
  }

  async function handleRecalculate(decision: PricingDecision) {
    setRecalculatingId(decision.id)
    try {
      await recalculateAsync({
        book_id: decision.book_id,
        decision_id: decision.id,
      })
    } catch {
      /* el hook ya muestra el toast */
    } finally {
      setRecalculatingId(null)
    }
  }

  function handleOverride(manualPrice: number) {
    if (!detail) return
    override({ id: detail.id, manual_price: manualPrice })
  }

  return (
    <div style={{ padding: 16, maxWidth: 1200, margin: '0 auto' }}>
      <h1>Panel de Pricing</h1>
      <p style={{ color: '#475569' }}>
        Revisá los precios sugeridos por la IA, su explicación y ajustalos si es
        necesario antes de publicarlos.
      </p>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: selectedId ? '1.4fr 1fr' : '1fr',
          gap: 16,
          alignItems: 'flex-start',
        }}
      >
        <section>
          <PricingTable
            prices={prices}
            loading={isLoading}
            onRowClick={handleRowClick}
            onRecalculate={handleRecalculate}
            recalculatingId={recalculatingId}
          />
        </section>

        {selectedId && (
          <aside
            data-testid="pricing-side-panel"
            style={{
              border: '1px solid #e2e8f0',
              borderRadius: 8,
              padding: 16,
              background: 'white',
              position: 'sticky',
              top: 16,
            }}
          >
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 12,
              }}
            >
              <h2 style={{ margin: 0, fontSize: 18 }}>Detalle</h2>
              <button
                type="button"
                onClick={() => setSelectedId(null)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: 18,
                }}
                aria-label="Cerrar panel"
              >
                ×
              </button>
            </div>

            {detailLoading && (
              <div
                data-testid="detail-skeleton"
                style={{
                  height: 160,
                  background: '#eee',
                  borderRadius: 6,
                  animation: 'pulse 1.2s ease-in-out infinite',
                }}
              />
            )}

            {!detailLoading && detail && (
              <>
                <h3 style={{ margin: '4px 0 0' }}>{detail.title}</h3>
                <div style={{ color: '#64748b', fontSize: 13 }}>
                  {detail.author} · {detail.condition}
                </div>

                <div style={{ marginTop: 16 }}>
                  <ExplanationPanel decision={detail} />
                </div>

                <div style={{ marginTop: 16 }}>
                  <h4 style={{ margin: '4px 0 8px' }}>Ajuste manual</h4>
                  <PriceOverrideForm
                    initialValue={detail.manual_price ?? detail.suggested_price}
                    currency={detail.currency || 'ARS'}
                    isSaving={isSaving}
                    onSubmit={handleOverride}
                  />
                </div>
              </>
            )}
          </aside>
        )}
      </div>
    </div>
  )
}