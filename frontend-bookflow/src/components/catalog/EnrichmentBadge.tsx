import React from 'react'
type Props = { isEnriched: boolean }
export default function EnrichmentBadge({ isEnriched }: Props) {
  return isEnriched
    ? <span className="badge badge-enriched">Enriquecido</span>
    : <span className="badge badge-basic">Basico</span>
}
