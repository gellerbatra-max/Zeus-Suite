// Grading computation (pattern_design_plan.md Sec 5.2/6.1): applying deltas to a base piece
// across a size range is O(points x sizes), not an optimization solve, so it runs entirely
// client-side for instant grade-nest review -- no backend job needed (Sec 1's own reasoning for
// why this doesn't need the platform's async-job pattern).

import type { GradeRuleTable, Point } from './api/types'

// Deltas are defined per adjacent step (size_range[i] -> size_range[i+1]), so resolving an
// arbitrary target size walks the cumulative sum of steps between it and the base size --
// forward and summed as-is past the base, backward and negated before it.
export function gradedPosition(
  pointRef: string,
  base: { x: number; y: number },
  table: GradeRuleTable,
  targetSize: string,
): { x: number; y: number } {
  const baseIdx = table.size_range.indexOf(table.base_size)
  const targetIdx = table.size_range.indexOf(targetSize)
  if (baseIdx === -1 || targetIdx === -1 || baseIdx === targetIdx) return base

  let dx = 0
  let dy = 0
  if (targetIdx > baseIdx) {
    for (let step = baseIdx; step < targetIdx; step++) {
      const rule = table.rules.find((r) => r.point_ref === pointRef && r.size_step === step)
      if (rule) {
        dx += rule.delta_x
        dy += rule.delta_y
      }
    }
  } else {
    for (let step = targetIdx; step < baseIdx; step++) {
      const rule = table.rules.find((r) => r.point_ref === pointRef && r.size_step === step)
      if (rule) {
        dx -= rule.delta_x
        dy -= rule.delta_y
      }
    }
  }
  return { x: base.x + dx, y: base.y + dy }
}

export function gradedPerimeter(perimeter: Point[], table: GradeRuleTable, targetSize: string): Point[] {
  return perimeter.map((p) => ({ ...p, ...gradedPosition(p.point_ref, p, table, targetSize) }))
}

// A palette distinct from the base outline's blue and the seam/dart/notch colors, cycled if
// size_range is longer than the palette.
const NEST_COLORS = ['#c0392b', '#8e44ad', '#16a085', '#d35400', '#2980b9', '#27ae60']

export function nestColorFor(sizeIndex: number): string {
  return NEST_COLORS[sizeIndex % NEST_COLORS.length]
}
