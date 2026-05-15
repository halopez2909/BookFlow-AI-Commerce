import React from 'react'
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
