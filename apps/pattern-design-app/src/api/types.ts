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

// The delta from size_range[size_step] to size_range[size_step + 1] for one point (Richpeace's
// "Point Grading" / "Create new delta grading rule") -- the real AccuMark/Gerber model, deltas
// between adjacent sizes rather than absolute per-size offsets.
export interface GradeRule {
  point_ref: string
  size_step: number
  delta_x: number
  delta_y: number
}

export interface GradeRuleTable {
  size_range: string[]
  base_size: string
  rules: GradeRule[]
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
  grade_rule_table: GradeRuleTable | null
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
