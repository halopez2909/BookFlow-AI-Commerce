export type ImportBatch = {
  id: string
  file_name: string
  upload_date: string
  total_rows: number
  valid_rows: number
  invalid_rows: number
  status: string
  success_percentage?: number
}

export type BatchError = {
  id: string
  batch_id?: string
  row_number: number
  error_type: string
  message: string
  fix_hint?: string
}

export type Book = {
  id: string
  title: string
  author: string
  publisher: string
  category_id: string
  isbn?: string
  issn?: string
  description?: string
  cover_url?: string
  publication_year?: number
  volume?: string
  enriched_flag: boolean
  published_flag: boolean
}

export type Category = {
  id: string
  name: string
  description?: string
}

export type ConfigParams = Record<string, string>

// ---------- Pricing domain types ----------

export type PricingStatus = 'suggested' | 'applied' | 'pending' | 'overridden'

export type PricingSource = {
  name: string
  url?: string
  price?: number
}

export type PricingExplanation = {
  summary: string
  factors?: string[]
  method?: string
  notes?: string
}

export type PricingDecision = {
  id: string
  book_id: string
  title: string
  author: string
  condition: string
  suggested_price: number
  final_price?: number
  manual_price?: number
  currency?: string
  condition_factor: number
  reference_count: number
  sources: PricingSource[]
  explanation: PricingExplanation | string
  status: PricingStatus
  updated_at?: string
}