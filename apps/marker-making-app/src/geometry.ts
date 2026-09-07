export interface BoxLike {
  x: number
  y: number
  width: number
  height: number
}

export function boundingBoxesOverlap(a: BoxLike, b: BoxLike): boolean {
  return a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y
}

// Whole-marker Flip X/Y/XY (Sec 1.9): the tight bounding box of everything currently placed, so a
// marker-wide flip mirrors pieces within their own occupied footprint rather than an arbitrary
// fixed canvas rectangle -- consistent with how fuse-blocking/material-calc already treat bbox as
// the natural reference frame instead of the (unbounded, purely visual) canvas dimensions.
export function computeBoundingBox(boxes: BoxLike[]): { minX: number; minY: number; maxX: number; maxY: number } | null {
  if (boxes.length === 0) return null
  let minX = Infinity
  let minY = Infinity
  let maxX = -Infinity
  let maxY = -Infinity
  for (const b of boxes) {
    minX = Math.min(minX, b.x)
    minY = Math.min(minY, b.y)
    maxX = Math.max(maxX, b.x + b.width)
    maxY = Math.max(maxY, b.y + b.height)
  }
  return { minX, minY, maxX, maxY }
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

// A segment of the weave line, centered on whichever point of the (infinite) line is closest to
// (nearX, nearY) -- so it visually spans the relevant area without exact line/rectangle clipping.
// `length` should be generous relative to that area (e.g. its diagonal * 1.5): the canvas center
// for the rule table's global line, or a piece's own center (with its own bbox diagonal) for a
// per-piece override.
export function weaveLineSegment(
  angleDeg: number,
  offset: number,
  nearX: number,
  nearY: number,
  length: number,
): { x1: number; y1: number; x2: number; y2: number; midX: number; midY: number } {
  const angle = (angleDeg * Math.PI) / 180
  const dx = Math.cos(angle)
  const dy = Math.sin(angle)
  const px = -Math.sin(angle)
  const py = Math.cos(angle)
  const baseX = offset * px
  const baseY = offset * py
  const t = (nearX - baseX) * dx + (nearY - baseY) * dy
  const midX = baseX + t * dx
  const midY = baseY + t * dy
  return {
    x1: midX - (length / 2) * dx, y1: midY - (length / 2) * dy,
    x2: midX + (length / 2) * dx, y2: midY + (length / 2) * dy,
    midX, midY,
  }
}
