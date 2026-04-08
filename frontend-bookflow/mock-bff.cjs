const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')
const multer = require('multer')
const fs = require('fs')
const path = require('path')

const app = express()
app.use(bodyParser.json())
app.use(cors({ origin: 'http://localhost:5173' }))
app.use((req, res, next) => { console.log('[MOCK] ', req.method, req.path); next(); })


const upload = multer({ storage: multer.memoryStorage() })

const BATCHES_FILE = path.resolve(__dirname, 'batches.json')

// cargar batches desde archivo si existe, o inicializar con demo
let batches = [
  {
    id: '1',
    file_name: 'demo.csv',
    upload_date: new Date().toISOString(),
    processed_rows: 10,
    valid_rows: 8,
    invalid_rows: 2,
    status: 'processed'
  }
]

try {
  if (fs.existsSync(BATCHES_FILE)) {
    const raw = fs.readFileSync(BATCHES_FILE, 'utf8')
    const parsed = JSON.parse(raw)
    if (Array.isArray(parsed)) batches = parsed
    console.log('Loaded batches from', BATCHES_FILE)
  } else {
    // inicializar archivo con batch demo
    fs.writeFileSync(BATCHES_FILE, JSON.stringify(batches, null, 2), 'utf8')
    console.log('Created batches file at', BATCHES_FILE)
  }
} catch (err) {
  console.error('Error loading batches file:', err)
}

// endpoints
app.post('/api/auth/login', (req, res) => {
  const { username } = req.body
  return res.json({ token: 'demo-token', user: { username: username || 'demo' } })
})

app.get('/api/inventory/batches', (req, res) => {
  return res.json(batches)
})

app.get('/api/inventory/batches/:id/errors', (req, res) => {
  const { id } = req.params
  return res.json([
    { id: `${id}-e1`, row_number: 2, error_type: 'MISSING_ISBN', message: 'Falta ISBN', fix_hint: 'Revisar columna ISBN' },
    { id: `${id}-e2`, row_number: 5, error_type: 'INVALID_DATE', message: 'Fecha inválida', fix_hint: 'Formato YYYY-MM-DD' }
  ])
})

app.post('/api/inventory/upload', upload.single('file'), (req, res) => {
  try {
    const filename = req.file?.originalname || 'unknown'
    const importResult = {
      id: String(Date.now()),
      file_name: filename,
      upload_date: new Date().toISOString(),
      processed_rows: 10,
      valid_rows: 8,
      invalid_rows: 2,
      status: 'processed'
    }

    // almacenar en memoria al inicio del array
    batches.unshift(importResult)

    // persistir en batches.json (escritura síncrona simple)
    try {
      fs.writeFileSync(BATCHES_FILE, JSON.stringify(batches, null, 2), 'utf8')
    } catch (wfErr) {
      console.error('Error writing batches file:', wfErr)
      // no bloquear la respuesta al frontend por fallo de persistencia
    }

    return res.json(importResult)
  } catch (err) {
    console.error('Upload handler error:', err)
    return res.status(500).json({ message: 'Upload failed' })
  }
})

// DELETE batch by id
app.delete('/api/inventory/batches/:id', (req, res) => {
  try {
    const { id } = req.params
    const idx = batches.findIndex(b => b.id === id)
    if (idx === -1) return res.status(404).json({ message: 'Batch not found' })
    const removed = batches.splice(idx, 1)[0]
    // persistir cambios
    try {
      fs.writeFileSync(BATCHES_FILE, JSON.stringify(batches, null, 2), 'utf8')
    } catch (wfErr) {
      console.error('Error writing batches file:', wfErr)
    }
    return res.json({ message: 'Deleted', removed })
  } catch (err) {
    console.error('Delete handler error:', err)
    return res.status(500).json({ message: 'Delete failed' })
  }
})


// health endpoint
app.get('/health', (_req, res) => res.json({ status: 'ok' }))
// GET config params
app.get('/api/config/params', (req, res) => {
  // ejemplo de parámetros (ajusta según necesites)
  return res.json({
    site_name: 'BookFlow',
    default_currency: 'ARS',
    max_upload_mb: 5
  })
})

// PUT config params (dev) — devuelve lo recibido (puedes persistir si quieres)
app.put('/api/config/params', (req, res) => {
  // opcional: validar req.body aquí
  return res.json(req.body)
})



app.listen(8000, () => console.log('Mock BFF listening on http://localhost:8000'))
