export type ImportBatch = {
  id: string
  file_name: string
  upload_date: string
  processed_rows: number
  valid_rows: number
  invalid_rows: number
  status: string
}
