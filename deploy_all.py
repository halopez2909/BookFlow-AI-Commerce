import os

base = "frontend-bookflow/src"

files = {}

files["index.css"] = """@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --bg: #F7F4EF;
  --bg-card: #FFFFFF;
  --bg-dark: #1C1917;
  --text: #1C1917;
  --text-2: #57534E;
  --text-3: #A8A29E;
  --accent: #C2410C;
  --accent-light: #FED7AA;
  --accent-dim: rgba(194,65,12,0.1);
  --green: #15803D;
  --green-light: #DCFCE7;
  --border: #E7E5E4;
  --border-strong: #D6D3D1;
  --shadow: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.1);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.12);
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'DM Sans', system-ui, sans-serif;
  --r: 8px;
  --r-lg: 16px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{font-family:var(--font-body);background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;min-height:100vh;}
#root{min-height:100vh;display:flex;flex-direction:column;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:var(--bg);}::-webkit-scrollbar-thumb{background:var(--border-strong);border-radius:3px;}
h1,h2,h3{font-family:var(--font-display);line-height:1.2;}
a{color:var(--accent);text-decoration:none;}
.navbar{position:sticky;top:0;z-index:100;background:rgba(28,25,23,0.96);backdrop-filter:blur(16px);padding:0 clamp(16px,4vw,64px);height:64px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);}
.navbar-brand{font-family:var(--font-display);font-size:22px;font-weight:700;color:#FAFAF9;letter-spacing:-0.02em;}
.navbar-brand span{color:#FB923C;}
.navbar-link{font-size:13px;font-weight:500;color:#A8A29E;padding:6px 14px;border-radius:6px;transition:all 0.15s;background:transparent;border:none;cursor:pointer;font-family:var(--font-body);}
.navbar-link:hover{color:#FAFAF9;background:rgba(255,255,255,0.08);}
.admin-nav{background:var(--bg-card);border-bottom:1px solid var(--border);padding:0 clamp(16px,4vw,48px);display:flex;align-items:center;gap:4px;height:48px;}
.admin-nav-btn{font-size:13px;font-weight:500;color:var(--text-2);padding:6px 14px;border-radius:6px;background:transparent;border:none;cursor:pointer;font-family:var(--font-body);transition:all 0.15s;text-decoration:none;display:inline-flex;align-items:center;}
.admin-nav-btn:hover{background:var(--bg);color:var(--text);}
.admin-nav-btn.active{background:var(--accent-dim);color:var(--accent);}
.page{max-width:1280px;margin:0 auto;padding:clamp(24px,4vw,48px) clamp(16px,4vw,48px);}
.btn{font-family:var(--font-body);font-size:13px;font-weight:600;padding:9px 18px;border-radius:var(--r);border:none;cursor:pointer;transition:all 0.15s;display:inline-flex;align-items:center;gap:6px;letter-spacing:0.02em;}
.btn-primary{background:var(--accent);color:white;}
.btn-primary:hover{background:#9A3412;transform:translateY(-1px);box-shadow:0 4px 12px rgba(194,65,12,0.3);}
.btn-primary:disabled{opacity:0.5;cursor:not-allowed;transform:none;}
.btn-ghost{background:transparent;color:var(--text-2);border:1px solid var(--border-strong);}
.btn-ghost:hover{background:var(--bg);color:var(--text);}
.btn-sm{font-size:12px;padding:6px 12px;}
input,select{font-family:var(--font-body);font-size:14px;background:var(--bg-card);border:1px solid var(--border-strong);color:var(--text);border-radius:var(--r);padding:9px 12px;outline:none;transition:border-color 0.15s,box-shadow 0.15s;width:100%;}
input:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);}
input::placeholder{color:var(--text-3);}
.badge{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;}
.badge-enriched{background:var(--green-light);color:var(--green);}
.badge-basic{background:#F5F5F4;color:var(--text-3);border:1px solid var(--border);}
.badge-available{background:var(--green-light);color:var(--green);}
.books-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px;}
@media(max-width:480px){.books-grid{grid-template-columns:repeat(2,1fr);gap:12px;}}
.book-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;cursor:pointer;transition:all 0.2s;display:flex;flex-direction:column;box-shadow:var(--shadow);}
.book-card:hover{border-color:var(--accent);box-shadow:var(--shadow-md);transform:translateY(-3px);}
.book-card-img{width:100%;aspect-ratio:2/3;object-fit:cover;background:linear-gradient(135deg,#F5F5F4,#E7E5E4);display:block;}
.book-card-placeholder{width:100%;aspect-ratio:2/3;background:linear-gradient(135deg,#FEF3C7,#FDE68A);display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-size:36px;color:#92400E;font-style:italic;}
.book-card-body{padding:14px;flex:1;display:flex;flex-direction:column;gap:5px;}
.book-card-title{font-family:var(--font-display);font-size:14px;font-weight:600;color:var(--text);line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.book-card-author{font-size:12px;color:var(--text-2);}
.book-card-footer{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:8px;flex-wrap:wrap;gap:4px;}
.book-price{font-size:14px;font-weight:700;color:var(--accent);}
.book-price-na{font-size:12px;color:var(--text-3);font-style:italic;}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
.skeleton{background:linear-gradient(90deg,#F5F5F4 25%,#E7E5E4 50%,#F5F5F4 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:var(--r);}
.skeleton-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;}
.skeleton-img{aspect-ratio:2/3;width:100%;}
.skeleton-line{height:13px;margin:8px 14px 0;}
.skeleton-line.short{width:60%;}
.skeleton-line.xshort{width:40%;margin-bottom:14px;}
.filter-bar{display:flex;gap:10px;margin-bottom:28px;flex-wrap:wrap;align-items:flex-end;}
.filter-group{display:flex;flex-direction:column;gap:4px;}
.filter-label{font-size:11px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.06em;}
.range-row{display:flex;gap:8px;align-items:center;}
.empty-state{text-align:center;padding:64px 24px;}
.empty-state p{color:var(--text-2);margin-top:8px;}
.catalog-hero{margin-bottom:36px;}
.catalog-hero h1{font-size:clamp(1.8rem,4vw,2.8rem);margin-bottom:8px;}
.catalog-hero p{color:var(--text-2);font-size:15px;}
.detail-layout{display:grid;grid-template-columns:300px 1fr;gap:40px;}
@media(max-width:768px){.detail-layout{grid-template-columns:1fr;}}
.detail-img{width:100%;border-radius:var(--r-lg);box-shadow:var(--shadow-lg);object-fit:cover;}
.detail-img-placeholder{width:100%;aspect-ratio:2/3;border-radius:var(--r-lg);background:linear-gradient(135deg,#FEF3C7,#FDE68A);display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-size:64px;color:#92400E;}
.detail-meta{display:flex;flex-direction:column;gap:16px;}
.detail-title{font-size:clamp(1.5rem,3vw,2.2rem);}
.detail-author{font-size:16px;color:var(--text-2);}
.detail-description{font-size:14px;line-height:1.7;color:var(--text-2);}
.detail-price-box{background:linear-gradient(135deg,#FFF7ED,#FFEDD5);border:1px solid #FED7AA;border-radius:var(--r-lg);padding:16px 20px;}
.detail-price-value{font-size:28px;font-weight:700;color:var(--accent);}
.detail-price-explanation{font-size:12px;color:var(--text-2);margin-top:4px;line-height:1.5;}
.detail-attrs{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;}
.detail-attr{background:var(--bg);border-radius:var(--r);padding:10px 14px;}
.detail-attr-label{font-size:10px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:3px;}
.detail-attr-value{font-size:13px;font-weight:500;color:var(--text);}
.login-page{min-height:100vh;display:grid;grid-template-columns:1fr 1fr;}
@media(max-width:768px){.login-page{grid-template-columns:1fr;}}
.login-left{background:var(--bg-dark);display:flex;align-items:center;justify-content:center;padding:48px;position:relative;overflow:hidden;}
.login-left-orb{position:absolute;border-radius:50%;filter:blur(60px);pointer-events:none;}
.login-left-content{position:relative;z-index:1;}
.login-logo{font-family:var(--font-display);font-size:40px;font-weight:700;color:#FAFAF9;}
.login-logo span{color:#FB923C;}
.login-tagline{font-size:15px;color:#78716C;margin-top:12px;line-height:1.6;max-width:280px;}
.login-right{display:flex;align-items:center;justify-content:center;padding:48px;background:var(--bg);}
.login-form-container{width:100%;max-width:360px;}
.login-form-title{font-family:var(--font-display);font-size:26px;margin-bottom:6px;}
.login-form-subtitle{color:var(--text-2);font-size:13px;margin-bottom:28px;}
.login-field{margin-bottom:16px;}
.login-label{display:block;font-size:12px;font-weight:600;color:var(--text-2);margin-bottom:6px;letter-spacing:0.04em;text-transform:uppercase;}
.login-error{background:#FEF2F2;border:1px solid #FECACA;color:#991B1B;padding:10px 14px;border-radius:var(--r);font-size:13px;margin-bottom:14px;}
.login-submit{width:100%;padding:11px;font-size:14px;margin-top:6px;}
.login-back{text-align:center;margin-top:20px;font-size:13px;color:var(--text-3);}
.table-wrap{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;}
table{width:100%;border-collapse:collapse;}
th{text-align:left;padding:12px 16px;font-size:11px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.06em;border-bottom:1px solid var(--border);background:var(--bg);}
td{padding:14px 16px;font-size:13px;border-bottom:1px solid var(--border);color:var(--text-2);vertical-align:middle;}
tr:last-child td{border-bottom:none;}
tr:hover td{background:var(--bg);color:var(--text);}
.page-header{margin-bottom:28px;}
.page-header h1{font-size:24px;margin-bottom:4px;}
.page-header p{color:var(--text-2);font-size:14px;}
.load-more{text-align:center;margin-top:36px;}
.books-count{text-align:center;color:var(--text-3);font-size:13px;margin-top:12px;}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.fade-in{animation:fadeIn 0.3s ease;}
"""

files["components/catalog/EnrichmentBadge.tsx"] = """import React from 'react'
type Props = { isEnriched: boolean }
export default function EnrichmentBadge({ isEnriched }: Props) {
  return isEnriched
    ? <span className="badge badge-enriched">Enriquecido</span>
    : <span className="badge badge-basic">Basico</span>
}
"""

files["components/catalog/PriceSummary.tsx"] = """import React from 'react'
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
"""

files["components/catalog/BookCard.tsx"] = """import React from 'react'
import type { Book } from '../../utils/types'
import EnrichmentBadge from './EnrichmentBadge'
import PriceSummary from './PriceSummary'
type Props = { book: Book; onClick?: () => void }
export default function BookCard({ book, onClick }: Props) {
  const initials = book.title.split(' ').slice(0,2).map((w:string)=>w[0]).join('').toUpperCase()
  return (
    <div className="book-card fade-in" onClick={onClick}>
      {book.cover_url
        ? <img className="book-card-img" src={book.cover_url} alt={book.title} loading="lazy"
            onError={(e)=>{const t=e.currentTarget as HTMLImageElement;t.style.display='none';const p=t.nextElementSibling as HTMLElement;if(p)p.style.display='flex';}} />
        : null}
      <div className="book-card-placeholder" style={{display:book.cover_url?'none':'flex'}}>{initials}</div>
      <div className="book-card-body">
        <EnrichmentBadge isEnriched={book.enriched_flag} />
        <div className="book-card-title">{book.title}</div>
        <div className="book-card-author">{book.author}</div>
        <div className="book-card-footer">
          <PriceSummary suggestedPrice={book.suggested_price} />
          {book.published_flag && <span className="badge badge-available">Disponible</span>}
        </div>
      </div>
    </div>
  )
}
"""

files["components/catalog/SkeletonCard.tsx"] = """import React from 'react'
export default function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-img" />
      <div style={{padding:14}}>
        <div className="skeleton skeleton-line" style={{marginBottom:6}} />
        <div className="skeleton skeleton-line" />
        <div className="skeleton skeleton-line short" />
        <div className="skeleton skeleton-line xshort" />
      </div>
    </div>
  )
}
"""

files["components/catalog/FilterBar.tsx"] = """import React from 'react'
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
"""

files["components/shared/EmptyState.tsx"] = """import React from 'react'
type Props = { message: string; onRetry?: () => void }
export default function EmptyState({ message, onRetry }: Props) {
  return (
    <div className="empty-state">
      <div style={{fontSize:40,marginBottom:12,opacity:0.4}}>📚</div>
      <p>{message}</p>
      {onRetry && <button className="btn btn-ghost" onClick={onRetry} style={{marginTop:16}}>Reintentar</button>}
    </div>
  )
}
"""

files["utils/types.ts"] = """export type ImportBatch = {
  id: string; file_name: string; upload_date: string; total_rows: number
  valid_rows: number; invalid_rows: number; status: string; success_percentage?: number
}
export type BatchError = {
  id: string; batch_id: string; row_number: number; error_type: string; message: string; fix_hint?: string
}
export type Book = {
  id: string; title: string; author: string; publisher: string; category_id: string
  isbn?: string; issn?: string; description?: string; cover_url?: string
  publication_year?: number; volume?: string; enriched_flag: boolean; published_flag: boolean
  suggested_price?: number | null; price_explanation?: string | null; condition?: string | null
}
export type Category = { id: string; name: string; description?: string }
export type ConfigParams = Record<string, string>
export type PricingDecision = {
  id: string; book_id: string; book_reference?: string; title?: string; author?: string
  condition?: string; suggested_price: number; manual_price?: number; explanation?: string
  condition_factor?: number; reference_count?: number; currency?: string; status?: string
  created_at?: string; sources?: Array<{name: string}>
}
"""

files["hooks/useCatalog.ts"] = """import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../services/apiClient'
import type { Book } from '../utils/types'
type CatalogData = { items: Book[]; total: number; page: number; page_size: number }
type Filters = { title?: string; min_price?: number; max_price?: number; available?: boolean }
export function useCatalog() {
  const [filters, setFiltersState] = useState<Filters>({})
  const [page, setPage] = useState(1)
  const [extraItems, setExtraItems] = useState<Book[]>([])
  const { data, isLoading, isError, refetch } = useQuery<CatalogData>({
    queryKey: ['catalog', filters, page],
    queryFn: async () => {
      const params: Record<string, string> = { page: String(page), page_size: '20' }
      if (filters.title) params.title = filters.title
      if (filters.min_price !== undefined) params.min_price = String(filters.min_price)
      if (filters.max_price !== undefined) params.max_price = String(filters.max_price)
      if (filters.available) params.available = 'true'
      const { data } = await api.get<CatalogData>('/api/catalog/books', { params })
      return data
    },
    staleTime: 1000 * 30,
  })
  function fetchNextPage() {
    if (data && (data.items.length + extraItems.length) < data.total) {
      setExtraItems(prev => [...prev, ...(data.items ?? [])])
      setPage(p => p + 1)
    }
  }
  function setFilters(f: Filters) { setFiltersState(f); setPage(1); setExtraItems([]) }
  const items = page === 1 ? (data?.items ?? []) : extraItems
  return { data: data ? { ...data, items } : undefined, isLoading, isError, refetch, filters, setFilters, fetchNextPage }
}
"""

files["pages/catalog/CatalogPage.tsx"] = """import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCatalog } from '../../hooks/useCatalog'
import BookCard from '../../components/catalog/BookCard'
import SkeletonCard from '../../components/catalog/SkeletonCard'
import FilterBar from '../../components/catalog/FilterBar'
import EmptyState from '../../components/shared/EmptyState'
export default function CatalogPage() {
  const navigate = useNavigate()
  const { data, isLoading, isError, refetch, filters, setFilters, fetchNextPage } = useCatalog()
  const [titleInput, setTitleInput] = useState('')
  function handleTitleChange(v: string) { setTitleInput(v); setFilters({ ...filters, title: v }) }
  return (
    <div className="page">
      <div className="catalog-hero">
        <h1>Libreria BookFlow</h1>
        <p>{data?.total ? `${data.total} libros disponibles` : 'Explora nuestra coleccion'}</p>
      </div>
      <FilterBar
        title={titleInput} onTitleChange={handleTitleChange}
        minPrice={filters.min_price} maxPrice={filters.max_price}
        onMinPriceChange={v=>setFilters({...filters,min_price:v})}
        onMaxPriceChange={v=>setFilters({...filters,max_price:v})}
        available={filters.available} onAvailableChange={v=>setFilters({...filters,available:v})}
      />
      {isError && <EmptyState message="No se pudo cargar el catalogo." onRetry={()=>refetch()} />}
      {isLoading && (
        <div className="books-grid">{Array.from({length:12}).map((_,i)=><SkeletonCard key={i} />)}</div>
      )}
      {!isLoading && !isError && data?.items?.length === 0 && <EmptyState message="No se encontraron libros." />}
      {!isLoading && !isError && data?.items && data.items.length > 0 && (
        <>
          <div className="books-grid">
            {data.items.map(book=>(
              <BookCard key={book.id} book={book} onClick={()=>navigate('/catalog/'+book.id)} />
            ))}
          </div>
          {data.items.length < data.total && (
            <div className="load-more">
              <button className="btn btn-ghost" onClick={fetchNextPage}>Cargar mas libros</button>
            </div>
          )}
          <div className="books-count">Mostrando {data.items.length} de {data.total} libros</div>
        </>
      )}
    </div>
  )
}
"""

files["pages/catalog/BookDetailPage.tsx"] = """import React from 'react'
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
"""

files["pages/Login.tsx"] = """import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/apiClient'
import { AuthContext } from '../context/AuthContext'
export default function Login() {
  const { dispatch } = useContext(AuthContext)
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string|null>(null)
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault(); setError(null); setLoading(true)
    try {
      const { data } = await api.post('/api/auth/login', { email, password })
      dispatch({ type: 'LOGIN', payload: { token: data.access_token, user: data } })
      navigate('/admin/batches', { replace: true })
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Credenciales incorrectas')
    } finally { setLoading(false) }
  }
  return (
    <div className="login-page">
      <div className="login-left">
        <div className="login-left-orb" style={{width:350,height:350,background:'rgba(251,146,60,0.1)',top:-80,right:-80}} />
        <div className="login-left-orb" style={{width:200,height:200,background:'rgba(0,0,0,0.2)',bottom:-60,left:-40}} />
        <div className="login-left-content">
          <div className="login-logo">Book<span>Flow</span></div>
          <p className="login-tagline">Plataforma inteligente de comercio de libros con IA para pricing y enriquecimiento.</p>
        </div>
      </div>
      <div className="login-right">
        <div className="login-form-container">
          <h2 className="login-form-title">Portal Admin</h2>
          <p className="login-form-subtitle">Ingresa tus credenciales para continuar</p>
          <form onSubmit={handleSubmit}>
            <div className="login-field">
              <label className="login-label">Correo</label>
              <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required placeholder="admin@bookflow.com" autoComplete="email" />
            </div>
            <div className="login-field">
              <label className="login-label">Contrasena</label>
              <input type="password" value={password} onChange={e=>setPassword(e.target.value)} required placeholder="..." autoComplete="current-password" />
            </div>
            {error && <div className="login-error">{error}</div>}
            <button type="submit" disabled={loading} className="btn btn-primary login-submit">{loading?'Ingresando...':'Ingresar'}</button>
          </form>
          <div className="login-back"><a href="/catalog">Ver catalogo publico</a></div>
        </div>
      </div>
    </div>
  )
}
"""

files["pages/admin/AdminBatches.tsx"] = """import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useInventoryBatches } from '../../hooks/useInventoryBatches'
import BatchTable from '../../components/inventory/BatchTable'
import FileUploader from '../../components/inventory/FileUploader'
export default function AdminBatches() {
  const navigate = useNavigate()
  const { data: batches, isLoading, isError, error, refetch } = useInventoryBatches()
  return (
    <>
      <div className="admin-nav">
        <button className="admin-nav-btn active" onClick={()=>navigate('/admin/batches')}>Inventario</button>
        <button className="admin-nav-btn" onClick={()=>navigate('/admin/pricing')}>Pricing</button>
        <button className="admin-nav-btn" onClick={()=>navigate('/admin/config')}>Configuracion</button>
        <div style={{marginLeft:'auto'}}><a href="/catalog" className="admin-nav-btn" style={{fontSize:12,color:'var(--text-3)'}}>Ver catalogo</a></div>
      </div>
      <div className="page">
        <div className="page-header"><h1>Importacion de Inventario</h1><p>Sube archivos Excel o CSV con libros para procesar en lote</p></div>
        <FileUploader onUploaded={refetch} />
        {isError && <p style={{color:'var(--accent)',margin:'12px 0'}}>Error: {error?.message}</p>}
        {isLoading
          ? <div style={{color:'var(--text-3)',padding:24,textAlign:'center'}}>Cargando lotes...</div>
          : <div className="table-wrap" style={{marginTop:24}}><BatchTable batches={batches||[]} onRowClick={id=>navigate('/admin/batches/'+id+'/errors')} /></div>}
      </div>
    </>
  )
}
"""

files["pages/admin/AdminConfig.tsx"] = """import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useConfigParams } from '../../hooks/useConfigParams'
export default function AdminConfig() {
  const navigate = useNavigate()
  const { params, isLoading } = useConfigParams()
  return (
    <>
      <div className="admin-nav">
        <button className="admin-nav-btn" onClick={()=>navigate('/admin/batches')}>Inventario</button>
        <button className="admin-nav-btn" onClick={()=>navigate('/admin/pricing')}>Pricing</button>
        <button className="admin-nav-btn active" onClick={()=>navigate('/admin/config')}>Configuracion</button>
      </div>
      <div className="page">
        <div className="page-header"><h1>Configuracion del Sistema</h1><p>Parametros configurables sin tocar el codigo</p></div>
        {isLoading ? <div style={{color:'var(--text-3)'}}>Cargando...</div> : (
          <div className="table-wrap">
            <table><thead><tr><th>Parametro</th><th>Valor</th></tr></thead>
              <tbody>{Object.entries(params||{}).map(([k,v])=><tr key={k}><td style={{fontFamily:'monospace',fontSize:12}}>{k}</td><td>{v as string}</td></tr>)}</tbody>
            </table>
          </div>
        )}
      </div>
    </>
  )
}
"""

files["App.tsx"] = """import React from 'react'
import RoutesApp from './routes'
export default function App() { return <RoutesApp /> }
"""

for rel_path, content in files.items():
    full_path = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: {rel_path}")

print("\\nDone!")
