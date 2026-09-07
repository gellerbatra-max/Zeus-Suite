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

export interface ImportIgesOptions {
  closure_amount_mm?: number
  trim_tolerance?: number
  paste_internal_to_notch?: boolean
  points_to_drill_holes?: boolean
  unit_override?: 'mm' | 'in' | null
  target_collection?: string | null
  stage_only?: boolean
  auto_approve?: boolean
  import_profile_id?: string | null
}

export interface ImportWarning {
  code: string
  message: string
  detail: Record<string, unknown>
}

export interface ImportIgesJobOut {
  job_id: string
  status: string // queued | staged | committed | failed
  target_piece_id: string | null
  geometry: {
    perimeter: { point_ref: string; x: number; y: number; type: string }[]
    internal_lines: unknown[]
    notches: unknown[]
    grain_line: unknown | null
  } | null
  source_summary: { line_count: number; point_count: number; composite_curve_count: number; declared_unit: string } | null
  warnings: ImportWarning[]
  error_detail: string | null
}
