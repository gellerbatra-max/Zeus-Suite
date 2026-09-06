// Mirrors apps/format-interchange-service/app/schemas.py.

export interface ExportIgesRequest {
  include_internal_lines: boolean
  include_notches: boolean
  include_grain_line: boolean
}

export interface ExportIgesJobOut {
  job_id: string
  status: string
  piece_id: string
  piece_code: string | null
  download_url: string | null
  error_detail: string | null
}
