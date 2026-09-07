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
