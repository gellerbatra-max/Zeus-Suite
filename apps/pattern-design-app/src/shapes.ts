// Gerber's "Create Piece - Rectangle" / "Create Piece - Circle" (pattern_design_plan.md's Piece
// Creation catalogue): generate a perimeter from typed dimensions instead of manual point-clicking.

import type { Point } from './api/types'

export function rectanglePerimeter(widthMm: number, heightMm: number): Point[] {
  const hw = widthMm / 2
  const hh = heightMm / 2
  return [
    { point_ref: crypto.randomUUID(), x: -hw, y: -hh, type: 'corner' },
    { point_ref: crypto.randomUUID(), x: hw, y: -hh, type: 'corner' },
    { point_ref: crypto.randomUUID(), x: hw, y: hh, type: 'corner' },
    { point_ref: crypto.randomUUID(), x: -hw, y: hh, type: 'corner' },
  ]
}

const CIRCLE_SEGMENTS = 36

export function circlePerimeter(radiusMm: number): Point[] {
  const points: Point[] = []
  for (let i = 0; i < CIRCLE_SEGMENTS; i++) {
    const angle = (2 * Math.PI * i) / CIRCLE_SEGMENTS
    points.push({
      point_ref: crypto.randomUUID(),
      x: Math.round(radiusMm * Math.cos(angle) * 100) / 100,
      y: Math.round(radiusMm * Math.sin(angle) * 100) / 100,
      type: 'curve',
    })
  }
  return points
}
