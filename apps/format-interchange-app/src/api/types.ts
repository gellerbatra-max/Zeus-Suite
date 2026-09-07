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
  geometry: MigrationGeometry | null
  source_summary: SourceSummary | null
  warnings: ImportWarning[]
  error_detail: string | null
}

// -- Legacy Migration (Steps 3-4) -----------------------------------------------------------

export interface MigrationGeometryPoint {
  point_ref: string
  x: number
  y: number
  type: string
}

export interface MigrationGeometry {
  perimeter: MigrationGeometryPoint[]
  internal_lines: { line_ref: string; point_refs: string[] }[]
  notches: { point_ref: string; notch_type: string }[]
  grain_line: { start: { x: number; y: number }; end: { x: number; y: number }; angle_deg: number } | null
}

export interface RawLine {
  x1: number
  y1: number
  x2: number
  y2: number
  label: string
}

export interface RawPoint {
  x: number
  y: number
  label: string
}

export interface SourceSummary {
  raw_lines: RawLine[]
  raw_points: RawPoint[]
  line_count: number
  point_count: number
  composite_curve_count: number
  declared_unit: string
}

export interface MigrationFindingOut {
  id: string
  code: string
  severity: 'error' | 'warning'
  message: string
  geometry_ref: Record<string, unknown>
  resolved: boolean
}

export interface MigrationDiff {
  perimeter_offset: { magnitude_mm: number; direction_deg: number } | null
  moved_points: { index: number; before: { x: number; y: number }; after: { x: number; y: number }; distance_mm: number }[]
  notches: {
    added: { x: number; y: number }[]
    removed: { x: number; y: number }[]
    moved: { before: { x: number; y: number }; after: { x: number; y: number }; distance_mm: number }[]
  }
}

export interface MigrationItemOut {
  id: string
  batch_id: string
  source_style_ref: string
  status: string // pending | converted | converted_with_warning | error | blocked | resolved
  needs_review: boolean
  warning_accepted: boolean
  block_note: string | null
  target_piece_id: string | null
  converted_geometry: MigrationGeometry | null
  source_summary: SourceSummary | null
  diff: MigrationDiff | null
  error_detail: string | null
  findings: MigrationFindingOut[]
}

export interface MigrationBatchOut {
  id: string
  source_system: string
  status: string // pending | completed | committed
  auto_sort_flagged: boolean
  chunk_count: number
  item_count: number
  counts: Record<string, number>
  commit_blocked_by: string[]
}
