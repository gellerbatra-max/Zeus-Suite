// Whole-piece transforms (Gerber's "Rotate Piece" / "Flip Piece", pattern_design_plan.md Sec 4
// Piece Transformation -- a category Sec 7's own phase breakdown never assigns to a numbered
// sub-phase, so it's folded in here as a small, self-contained slice). Every point in the
// document has to move together: the perimeter, dart legs/apex, the grain line, and annotations
// -- internal lines/seams/notches/measurements don't carry their own coordinates (they reference
// point_refs), so they come along for free once the points they reference move.

import type { PieceGeometryDocument, Point } from './api/types'

function centroidOf(points: { x: number; y: number }[]): { x: number; y: number } {
  if (points.length === 0) return { x: 0, y: 0 }
  const sum = points.reduce((acc, p) => ({ x: acc.x + p.x, y: acc.y + p.y }), { x: 0, y: 0 })
  return { x: sum.x / points.length, y: sum.y / points.length }
}

type PointLike = { x: number; y: number }
type Transform2D = (p: PointLike, center: PointLike) => PointLike

const rotate90: Transform2D = (p, c) => ({ x: c.x - (p.y - c.y), y: c.y + (p.x - c.x) })
const flipHorizontal: Transform2D = (p, c) => ({ x: 2 * c.x - p.x, y: p.y })
const flipVertical: Transform2D = (p, c) => ({ x: p.x, y: 2 * c.y - p.y })

function applyTransform(doc: PieceGeometryDocument, transform: Transform2D): PieceGeometryDocument {
  const center = centroidOf(doc.perimeter)
  const moveXY = <T extends PointLike>(p: T): T => ({ ...p, ...transform(p, center) })

  let grainLine = doc.grain_line
  if (grainLine) {
    const start = moveXY(grainLine.start)
    const end = moveXY(grainLine.end)
    const angleDeg = (Math.atan2(end.y - start.y, end.x - start.x) * 180) / Math.PI
    grainLine = { ...grainLine, start, end, angle_deg: angleDeg }
  }

  return {
    ...doc,
    perimeter: doc.perimeter.map(moveXY) as Point[],
    darts: doc.darts.map((d) => ({ ...d, leg_a: moveXY(d.leg_a), apex: moveXY(d.apex), leg_b: moveXY(d.leg_b) })),
    grain_line: grainLine,
    annotations: doc.annotations.map(moveXY),
  }
}

export function rotatePiece90(doc: PieceGeometryDocument): PieceGeometryDocument {
  return applyTransform(doc, rotate90)
}

export function flipPieceHorizontal(doc: PieceGeometryDocument): PieceGeometryDocument {
  return applyTransform(doc, flipHorizontal)
}

export function flipPieceVertical(doc: PieceGeometryDocument): PieceGeometryDocument {
  return applyTransform(doc, flipVertical)
}
