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
