import React from 'react'
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
