import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useBookDetail } from '../../hooks/useBookDetail'
export default function BookDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { book, isLoading, isError } = useBookDetail(id)
  if (isLoading) return <div className="page" style={{textAlign:'center',padding:80,color:'var(--text-3)'}}>Cargando...</div>
  if (isError || !book) return (
    <div className="page">
      <button className="btn btn-ghost btn-sm" onClick={()=>navigate('/catalog')}>Volver</button>
      <p style={{marginTop:24,color:'var(--text-2)'}}>No se encontro el libro.</p>
    </div>
  )
  const initials = book.title.split(' ').slice(0,2).map((w:string)=>w[0]).join('').toUpperCase()
  return (
    <div className="page">
      <button className="btn btn-ghost btn-sm" onClick={()=>navigate('/catalog')} style={{marginBottom:28}}>Volver al catalogo</button>
      <div className="detail-layout">
        <div>
          {book.cover_url
            ? <img className="detail-img" src={book.cover_url} alt={book.title} />
            : <div className="detail-img-placeholder">{initials}</div>}
        </div>
        <div className="detail-meta">
          <div>
            {book.enriched_flag
              ? <span className="badge badge-enriched" style={{marginBottom:10,display:'inline-flex'}}>Enriquecido con IA</span>
              : <span className="badge badge-basic" style={{marginBottom:10,display:'inline-flex'}}>Basico</span>}
            <h1 className="detail-title">{book.title}</h1>
            <p className="detail-author" style={{marginTop:6}}>{book.author}</p>
          </div>
          {book.suggested_price ? (
            <div className="detail-price-box">
              <div style={{fontSize:11,fontWeight:600,color:'var(--accent)',textTransform:'uppercase',letterSpacing:'0.06em',marginBottom:4}}>Precio sugerido por IA</div>
              <div className="detail-price-value">${book.suggested_price.toLocaleString('es-CO')} COP</div>
              {book.price_explanation && <div className="detail-price-explanation">{book.price_explanation}</div>}
            </div>
          ) : <div style={{color:'var(--text-3)',fontSize:14,fontStyle:'italic'}}>Precio no disponible aun</div>}
          {book.description && (
            <div>
              <div style={{fontSize:11,fontWeight:600,color:'var(--text-3)',textTransform:'uppercase',letterSpacing:'0.06em',marginBottom:8}}>Descripcion</div>
              <p className="detail-description">{book.description}</p>
            </div>
          )}
          <div className="detail-attrs">
            {book.publisher && <div className="detail-attr"><div className="detail-attr-label">Editorial</div><div className="detail-attr-value">{book.publisher}</div></div>}
            {book.publication_year && <div className="detail-attr"><div className="detail-attr-label">Anio</div><div className="detail-attr-value">{book.publication_year}</div></div>}
            {book.isbn && <div className="detail-attr"><div className="detail-attr-label">ISBN</div><div className="detail-attr-value" style={{fontSize:12}}>{book.isbn}</div></div>}
            {book.condition && <div className="detail-attr"><div className="detail-attr-label">Condicion</div><div className="detail-attr-value">{book.condition}</div></div>}
          </div>
          <div>{book.published_flag ? <span className="badge badge-available">Disponible</span> : <span className="badge badge-basic">No disponible</span>}</div>
        </div>
      </div>
    </div>
  )
}
