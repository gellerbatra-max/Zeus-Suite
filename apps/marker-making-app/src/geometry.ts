export interface BoxLike {
  x: number
  y: number
  width: number
  height: number
}

export function boundingBoxesOverlap(a: BoxLike, b: BoxLike): boolean {
  return a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y
}

// Overlapped checking (marker_making_production_plan.md Sec 1.4): how far two pieces' bounding
// boxes intrude into each other on each axis, for reading the max overlap value against a
// neighbour once pieces are flagged as overlapping. Same axis-aligned-bounding-box simplification
// as boundingBoxesOverlap above (no rotation-aware polygon intersection) -- visual/informational
// only, not a hard placement block.
export function overlapAmount(a: BoxLike, b: BoxLike): { x: number; y: number } | null {
  const x = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x)
  const y = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y)
  if (x <= 0 || y <= 0) return null
  return { x, y }
}

// Weave-line tools (Sec 1.4): the line at angle_deg (measured from +X, standard math convention)
// offset perpendicular to that direction by `offset` from the canvas origin. Points on the line
// satisfy dot((x,y), perpendicular) == offset, where perpendicular = (-sin, cos).
export function weaveLineOffsetForPoint(angleDeg: number, x: number, y: number): number {
  const angle = (angleDeg * Math.PI) / 180
  return -x * Math.sin(angle) + y * Math.cos(angle)
}

// A long segment of the weave line, centered on whichever point of the (infinite) line is
// closest to the canvas center -- so it visually spans the canvas without exact line/rectangle
// clipping. `length` should be generous relative to the canvas (e.g. its diagonal * 1.5).
export function weaveLineSegment(
  angleDeg: number,
  offset: number,
  canvasWidth: number,
  canvasHeight: number,
  length: number,
): { x1: number; y1: number; x2: number; y2: number; midX: number; midY: number } {
  const angle = (angleDeg * Math.PI) / 180
  const dx = Math.cos(angle)
  const dy = Math.sin(angle)
  const px = -Math.sin(angle)
  const py = Math.cos(angle)
  const baseX = offset * px
  const baseY = offset * py
  const centerX = canvasWidth / 2
  const centerY = canvasHeight / 2
  const t = (centerX - baseX) * dx + (centerY - baseY) * dy
  const midX = baseX + t * dx
  const midY = baseY + t * dy
  return {
    x1: midX - (length / 2) * dx, y1: midY - (length / 2) * dy,
    x2: midX + (length / 2) * dx, y2: midY + (length / 2) * dy,
    midX, midY,
  }
}
