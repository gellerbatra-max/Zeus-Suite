// Mirrors apps/marker-making-service/app/schemas.py.

export interface PlacementData {
  x: number
  y: number
  rotation_deg: number
  flip_x: boolean
  flip_y: boolean
  width: number
  height: number
  stripe_mark_id?: string | null
  cutter_stripe_needed?: boolean
  weave_line_angle_deg?: number | null
  weave_line_offset?: number | null
  stripe_independent_in_set?: boolean
  block_buffer_rule_no?: number | null
  bundle_id?: string | null
}

export interface WorkspacePiece {
  id: string
  piece_code: string
  piece_name: string
  width: number
  height: number
}

export interface WorkspacePlacement {
  piece_id: string
  piece_version_id: string | null
  size_code: string
  quantity: number
  placement_data: Partial<PlacementData>
}

export interface WorkspaceOut {
  marker_id: string
  marker_code: string
  workflow_status: string
  order_id: string | null
  style_id: string | null
  fabric_width: number | null
  matching_method: string | null
  matching_rule_table_id: string | null
  available_pieces: WorkspacePiece[]
  placements: WorkspacePlacement[]
}

export interface NestingJobOut {
  id: string
  status: string
  progress_pct: number | null
  result_ref: Record<string, unknown> | null
  error_detail: string | null
}

// -- Matching (marker_making_production_plan.md Sec 1.4, new) -----------------------------------

export interface OffsetsIn {
  horizontal: number[]
  vertical: number[]
}

export interface StripeDefinition {
  id: string
  name: string
  kind: string
  origin_x: number
  origin_y: number
  h_distance: number
  v_distance: number
  h_angle_deg: number
  v_angle_deg: number
  params_abcd: Record<string, number> | null
}

export interface StripeMark {
  id: string
  sequence: number
  name: string
  size: number
  stripe_definition_id: string | null
  position: { x: number; y: number }
}

export interface WeaveLine {
  angle_deg: number
  offset: number
  visible: boolean
}

export interface MaterialPatternInfo {
  name: string | null
  visible: boolean
}

export interface MaterialPatternBeginResponse {
  upload_url: string
  storage_container: string
  storage_key: string
  expires_at: string
}

export interface MaterialPatternDownloadUrlOut {
  download_url: string
  expires_at: string
}

export interface MatchingRuleTableOut {
  id: string
  name: string
  method: string
  plaid_repeat: number | null
  stripe_repeat: number | null
  offsets: OffsetsIn
  stripe_definitions: StripeDefinition[]
  stripe_marks: StripeMark[]
  weave_line: WeaveLine | null
  material_pattern: MaterialPatternInfo | null
  version: number
}

export interface MatchGuidanceTarget {
  axis: string
  dx: number
  dy: number
  target_x: number
  target_y: number
}

export interface MatchGuidanceOut {
  found: boolean
  targets: MatchGuidanceTarget[]
  message: string | null
}

export interface BiteViolation {
  piece_id_a: string
  piece_id_b: string
  stripe_mark_id: string
  bite_index_a: number
  bite_index_b: number
}

export interface ValidateBiteOut {
  bite_length: number
  ok: boolean
  violations: BiteViolation[]
}

// -- Block / buffer / fuse-blocking (Sec 1.6, new) -----------------------------------------------

export interface BlockBufferRuleTableOut {
  id: string
  name: string
  rule_no: number
  rule_type: string
  mode: string
  left_amt: number
  top_amt: number
  right_amt: number
  bottom_amt: number
  version: number
}

export interface FuseBlockOut {
  id: string
  marker_id: string
  shape: string
  x: number
  y: number
  width: number
  height: number
  piece_placement_ids: string[]
  block_amount: number
  reduce_amount: number
  notch_depth: number
  version: number
}

// -- Material calculation / utilization (Sec 1.7, new) -------------------------------------------

export interface MaterialSummaryOut {
  fabric_width: number | null
  ply_count: number | null
  fabric_weight_per_unit_area: number | null
  marker_length: number | null
  utilization_pct: number | null
  computed_marker_length: number | null
  computed_total_piece_area: number | null
  computed_total_perimeter: number | null
  computed_utilization_pct: number | null
  target_length: number | null
  target_utilization_pct: number | null
}

export interface RequiredLengthOut {
  required_length: number
}

export interface MaterialWeightOut {
  weight: number
}

// -- Marker transformations (Sec 1.9, new) --------------------------------------------------------

export interface TransformSettingsOut {
  fabric_width: number | null
  shrink_x_pct: number | null
  shrink_y_pct: number | null
}

export interface ChangeWidthOut {
  fabric_width: number
}

// -- Layrules (Sec 1.5, new) -----------------------------------------------------------------

export interface LayruleSearchTableOut {
  id: string
  name: string
  area_compare: boolean
  area_deviation_pct: number
  copy_dynamics: boolean
  allow_overrides: boolean
  include_marker_name: boolean
  include_marker_description: boolean
  comment: string | null
  version: number
}

export interface LayruleOut {
  id: string
  name: string
  source_marker_id: string
  piece_count: number
  comment: string | null
  version: number
}

export interface ApplyLayruleResult {
  applied_piece_ids: string[]
  unmatched_piece_ids: string[]
  area_deviation_pct: number | null
  warning: string | null
}

// -- Splice marks / fabric-roll handling (Sec 1.8, new) -------------------------------------------

export interface SpliceMarkOut {
  id: string
  marker_id: string
  start_x: number
  end_x: number
  source: string
  roll_id: string | null
  version: number
}

export interface SpliceSettingsOut {
  min_length: number | null
  max_length: number | null
  margin: number | null
  separation: number | null
}

// -- Marker picker (Sec 1.11, new) -----------------------------------------------------------

export interface MarkerSearchResult {
  id: string
  code: string
  name: string
  folder_path: string | null
  workflow_status: string
  updated_at: string
}

export interface MarkerSearchResponse {
  results: MarkerSearchResult[]
  total: number
}

export interface MarkerSibling {
  id: string
  marker_code: string
  workflow_status: string
}
