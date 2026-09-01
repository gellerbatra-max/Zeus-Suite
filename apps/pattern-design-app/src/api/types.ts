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

export interface SeamAllowance {
  edge_ref: string[]
  allowance_mm: number
  corner_type: string
}

// A point that isn't part of the perimeter -- a dart leg/apex or a grain line endpoint.
export interface FreePoint {
  point_ref: string
  x: number
  y: number
}

export interface Dart {
  dart_ref: string
  leg_a: FreePoint
  apex: FreePoint
  leg_b: FreePoint
  intake_mm: number
}

export interface Notch {
  point_ref: string
  notch_type: string
  depth_mm: number
}

export interface GrainLine {
  start: FreePoint
  end: FreePoint
  angle_deg: number
}

export interface PieceGeometryDocument {
  schema_version: number
  units: string
  perimeter: Point[]
  internal_lines: InternalLine[]
  seams: SeamAllowance[]
  darts: Dart[]
  notches: Notch[]
  grain_line: GrainLine | null
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
