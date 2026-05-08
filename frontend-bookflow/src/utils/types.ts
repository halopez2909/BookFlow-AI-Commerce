export type ImportBatch = {
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
