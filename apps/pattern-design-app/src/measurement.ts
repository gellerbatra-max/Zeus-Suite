// Live distance computation for a spec measurement (Gerber's "Straight-Line Distance Between Two
// Points" / spec-chart concept, pattern_design_plan.md Sec 4 Measurement & Spec Charts). Computed
// from current point positions on every render rather than stored -- see Measurement's docstring
// in app/schemas.py for why a frozen value would defeat the point of a spec check.

import type { Measurement, Point } from './api/types'

export interface MeasurementResult {
  measurement: Measurement
  actualMm: number | null
  withinTolerance: boolean | null
}

export function computeMeasurement(measurement: Measurement, pointsByRef: Map<string, Point>): MeasurementResult {
  const a = pointsByRef.get(measurement.point_ref_a)
  const b = pointsByRef.get(measurement.point_ref_b)
  if (!a || !b) return { measurement, actualMm: null, withinTolerance: null }

  const actualMm = Math.hypot(b.x - a.x, b.y - a.y)
  if (measurement.target_value_mm === null) {
    return { measurement, actualMm, withinTolerance: null }
  }
  const tolerance = measurement.tolerance_mm ?? 0
  const withinTolerance = Math.abs(actualMm - measurement.target_value_mm) <= tolerance
  return { measurement, actualMm, withinTolerance }
}
