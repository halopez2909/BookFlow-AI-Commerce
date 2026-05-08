import React from 'react'
type Props = {
  title: string; onTitleChange: (v:string)=>void
  minPrice?: number; maxPrice?: number
  onMinPriceChange?: (v:number|undefined)=>void
  onMaxPriceChange?: (v:number|undefined)=>void
  available?: boolean; onAvailableChange?: (v:boolean)=>void
}
export default function FilterBar({title,onTitleChange,minPrice,maxPrice,onMinPriceChange,onMaxPriceChange,available,onAvailableChange}:Props) {
  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label className="filter-label">Buscar</label>
        <div style={{position:'relative'}}>
          <span style={{position:'absolute',left:10,top:'50%',transform:'translateY(-50%)',color:'var(--text-3)',pointerEvents:'none'}}>🔍</span>
          <input type="text" placeholder="Titulo o autor..." value={title} onChange={e=>onTitleChange(e.target.value)} style={{paddingLeft:34,minWidth:240}} />
        </div>
      </div>
      <div className="filter-group">
        <label className="filter-label">Precio COP</label>
        <div className="range-row">
          <input type="number" placeholder="Min" value={minPrice??''} onChange={e=>onMinPriceChange?.(e.target.value?Number(e.target.value):undefined)} style={{width:90}} />
          <span style={{color:'var(--text-3)',fontSize:12}}>-</span>
          <input type="number" placeholder="Max" value={maxPrice??''} onChange={e=>onMaxPriceChange?.(e.target.value?Number(e.target.value):undefined)} style={{width:90}} />
        </div>
      </div>
      <div className="filter-group" style={{justifyContent:'flex-end'}}>
        <label className="filter-label">Disponibilidad</label>
        <label style={{display:'flex',alignItems:'center',gap:8,cursor:'pointer',fontSize:13,color:'var(--text-2)',height:38}}>
          <input type="checkbox" checked={available??false} onChange={e=>onAvailableChange?.(e.target.checked)} style={{width:'auto',accentColor:'var(--accent)'}} />
          Solo disponibles
        </label>
      </div>
    </div>
  )
}
