import React from 'react'
type Props = { suggestedPrice?: number | null; explanation?: string | null }
export default function PriceSummary({ suggestedPrice, explanation }: Props) {
  if (!suggestedPrice) return <span className="book-price-na">Precio no disponible</span>
  return (
    <div>
      <div className="book-price">${suggestedPrice.toLocaleString('es-CO')} COP</div>
      {explanation && <div style={{fontSize:11,color:'var(--text-3)',marginTop:3,lineHeight:1.4}}>{explanation.length>60?explanation.slice(0,60)+'...':explanation}</div>}
    </div>
  )
}
