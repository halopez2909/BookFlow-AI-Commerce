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
  batch_id: string
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
