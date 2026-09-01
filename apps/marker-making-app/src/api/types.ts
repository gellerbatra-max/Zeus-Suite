// Mirrors apps/marker-making-service/app/schemas.py.

export interface PlacementData {
  x: number
  y: number
  rotation_deg: number
  flip_x: boolean
  flip_y: boolean
  width: number
  height: number
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
