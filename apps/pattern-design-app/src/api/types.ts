// Mirrors apps/pattern-design-service/app/schemas.py.

export interface Point {
  point_ref: string
  x: number
  y: number
  type: string
}

export interface InternalLine {
  line_ref: string
  point_refs: string[]
  line_type: string
}

export interface PieceGeometryDocument {
  schema_version: number
  units: string
  perimeter: Point[]
  internal_lines: InternalLine[]
  seams: unknown[]
  darts: unknown[]
  notches: unknown[]
  grain_line: unknown | null
  annotations: unknown[]
}

export interface WorkflowStatusOut {
  code: string
  label: string
}

export interface PieceOut {
  id: string
  folder_id: string
  piece_code: string
  piece_name: string
  piece_type: string
  base_size: string | null
  description: string | null
  current_version_id: string | null
  workflow_status: WorkflowStatusOut
  version: number
}

export interface FolderOut {
  id: string
  parent_id: string | null
  name: string
  path: string
  folder_type: string
}
