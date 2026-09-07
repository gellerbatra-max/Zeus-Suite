// Every drawing/editing tool is a command object with do()/undo() over the geometry document --
// pattern_design_plan.md Sec 6.3: "the same command list backs undo/redo and, on save, is what
// gets diffed against the last-saved geometry document." This slice doesn't diff on save (every
// save still round-trips the whole document, per Phase 2.1), but the do/undo pairing is exactly
// the shape that diffing would build on, and it's what backs the undo/redo stack now.

import type {
  Annotation,
  Dart,
  GradeRule,
  GradeRuleTable,
  GrainLine,
  InternalLine,
  Measurement,
  Notch,
  PieceGeometryDocument,
  Point,
  SeamAllowance,
} from './api/types'

export interface Command {
  label: string
  do(doc: PieceGeometryDocument): PieceGeometryDocument
  undo(doc: PieceGeometryDocument): PieceGeometryDocument
}

export function addPointCommand(point: Point): Command {
  return {
    label: 'Add point',
    do: (doc) => ({ ...doc, perimeter: [...doc.perimeter, point] }),
    undo: (doc) => ({ ...doc, perimeter: doc.perimeter.filter((p) => p.point_ref !== point.point_ref) }),
  }
}

export function deletePointCommand(point: Point, index: number): Command {
  return {
    label: 'Delete point',
    do: (doc) => ({ ...doc, perimeter: doc.perimeter.filter((p) => p.point_ref !== point.point_ref) }),
    undo: (doc) => {
      const perimeter = [...doc.perimeter]
      perimeter.splice(index, 0, point)
      return { ...doc, perimeter }
    },
  }
}

export function movePointCommand(
  pointRef: string,
  from: { x: number; y: number },
  to: { x: number; y: number },
): Command {
  return {
    label: 'Move point',
    do: (doc) => ({
      ...doc,
      perimeter: doc.perimeter.map((p) => (p.point_ref === pointRef ? { ...p, x: to.x, y: to.y } : p)),
    }),
    undo: (doc) => ({
      ...doc,
      perimeter: doc.perimeter.map((p) => (p.point_ref === pointRef ? { ...p, x: from.x, y: from.y } : p)),
    }),
  }
}

export function addLineCommand(line: InternalLine): Command {
  return {
    label: 'Add line',
    do: (doc) => ({ ...doc, internal_lines: [...doc.internal_lines, line] }),
    undo: (doc) => ({ ...doc, internal_lines: doc.internal_lines.filter((l) => l.line_ref !== line.line_ref) }),
  }
}

export function deleteLineCommand(line: InternalLine, index: number): Command {
  return {
    label: 'Delete line',
    do: (doc) => ({ ...doc, internal_lines: doc.internal_lines.filter((l) => l.line_ref !== line.line_ref) }),
    undo: (doc) => {
      const internal_lines = [...doc.internal_lines]
      internal_lines.splice(index, 0, line)
      return { ...doc, internal_lines }
    },
  }
}

// Seams are keyed one-per-edge (edge_ref) -- setting a seam on an edge that already has one
// replaces it, so the whole previous `seams` array is what undo restores rather than trying to
// track the single prior value.
export function setSeamCommand(seam: SeamAllowance, previousSeams: SeamAllowance[]): Command {
  return {
    label: 'Set seam allowance',
    do: (doc) => ({
      ...doc,
      seams: [...doc.seams.filter((s) => !sameEdge(s.edge_ref, seam.edge_ref)), seam],
    }),
    undo: (doc) => ({ ...doc, seams: previousSeams }),
  }
}

function sameEdge(a: string[], b: string[]): boolean {
  return a.length === b.length && a.every((ref) => b.includes(ref))
}

export function removeSeamCommand(seam: SeamAllowance, index: number): Command {
  return {
    label: 'Remove seam allowance',
    do: (doc) => ({ ...doc, seams: doc.seams.filter((s) => !sameEdge(s.edge_ref, seam.edge_ref)) }),
    undo: (doc) => {
      const seams = [...doc.seams]
      seams.splice(index, 0, seam)
      return { ...doc, seams }
    },
  }
}

export function addDartCommand(dart: Dart): Command {
  return {
    label: 'Add dart',
    do: (doc) => ({ ...doc, darts: [...doc.darts, dart] }),
    undo: (doc) => ({ ...doc, darts: doc.darts.filter((d) => d.dart_ref !== dart.dart_ref) }),
  }
}

export function removeDartCommand(dart: Dart, index: number): Command {
  return {
    label: 'Remove dart',
    do: (doc) => ({ ...doc, darts: doc.darts.filter((d) => d.dart_ref !== dart.dart_ref) }),
    undo: (doc) => {
      const darts = [...doc.darts]
      darts.splice(index, 0, dart)
      return { ...doc, darts }
    },
  }
}

export function addNotchCommand(notch: Notch): Command {
  return {
    label: 'Add notch',
    do: (doc) => ({ ...doc, notches: [...doc.notches, notch] }),
    undo: (doc) => ({ ...doc, notches: doc.notches.filter((n) => n.point_ref !== notch.point_ref) }),
  }
}

export function removeNotchCommand(notch: Notch, index: number): Command {
  return {
    label: 'Remove notch',
    do: (doc) => ({ ...doc, notches: doc.notches.filter((n) => n.point_ref !== notch.point_ref) }),
    undo: (doc) => {
      const notches = [...doc.notches]
      notches.splice(index, 0, notch)
      return { ...doc, notches }
    },
  }
}

// One grain line per piece (Richpeace depth, Sec 4 -- the only category with no Gerber
// equivalent at all), so setting a new one always replaces whatever was there. `newLine: null`
// clears it.
export function setGrainLineCommand(newLine: GrainLine | null, previousLine: GrainLine | null): Command {
  return {
    label: 'Set grain line',
    do: (doc) => ({ ...doc, grain_line: newLine }),
    undo: (doc) => ({ ...doc, grain_line: previousLine }),
  }
}

// Defining/changing the size range resets any existing rules -- their size_step indices are
// positions into the old size_range and would silently point at the wrong steps otherwise.
export function setSizeRangeCommand(
  sizeRange: string[],
  baseSize: string,
  previousTable: GradeRuleTable | null,
): Command {
  return {
    label: 'Set size range',
    do: (doc) => ({ ...doc, grade_rule_table: { size_range: sizeRange, base_size: baseSize, rules: [] } }),
    undo: (doc) => ({ ...doc, grade_rule_table: previousTable }),
  }
}

// A grade rule is keyed one-per-(point_ref, size_step) -- setting one that already exists
// replaces it, so undo restores the whole previous table rather than tracking the single prior
// rule (same pattern as setSeamCommand).
export function setGradeRuleCommand(table: GradeRuleTable, rule: GradeRule): Command {
  const nextRules = [
    ...table.rules.filter((r) => !(r.point_ref === rule.point_ref && r.size_step === rule.size_step)),
    rule,
  ]
  return {
    label: 'Set grade rule',
    do: (doc) => ({ ...doc, grade_rule_table: { ...table, rules: nextRules } }),
    undo: (doc) => ({ ...doc, grade_rule_table: table }),
  }
}

// Rectangle/circle piece creation (Gerber's "Create Piece - Rectangle"/"Create Piece - Circle")
// replace the whole perimeter and drop any internal lines, since those lines referenced the old
// perimeter's point_refs and would otherwise dangle.
export function replaceShapeCommand(
  newPerimeter: Point[],
  oldPerimeter: Point[],
  oldInternalLines: InternalLine[],
  label: string,
): Command {
  return {
    label,
    do: (doc) => ({ ...doc, perimeter: newPerimeter, internal_lines: [] }),
    undo: (doc) => ({ ...doc, perimeter: oldPerimeter, internal_lines: oldInternalLines }),
  }
}

export function addAnnotationCommand(annotation: Annotation): Command {
  return {
    label: 'Add annotation',
    do: (doc) => ({ ...doc, annotations: [...doc.annotations, annotation] }),
    undo: (doc) => ({
      ...doc,
      annotations: doc.annotations.filter((a) => a.annotation_ref !== annotation.annotation_ref),
    }),
  }
}

export function removeAnnotationCommand(annotation: Annotation, index: number): Command {
  return {
    label: 'Remove annotation',
    do: (doc) => ({
      ...doc,
      annotations: doc.annotations.filter((a) => a.annotation_ref !== annotation.annotation_ref),
    }),
    undo: (doc) => {
      const annotations = [...doc.annotations]
      annotations.splice(index, 0, annotation)
      return { ...doc, annotations }
    },
  }
}

export function addMeasurementCommand(measurement: Measurement): Command {
  return {
    label: 'Add measurement',
    do: (doc) => ({ ...doc, measurements: [...doc.measurements, measurement] }),
    undo: (doc) => ({
      ...doc,
      measurements: doc.measurements.filter((m) => m.measurement_ref !== measurement.measurement_ref),
    }),
  }
}

export function removeMeasurementCommand(measurement: Measurement, index: number): Command {
  return {
    label: 'Remove measurement',
    do: (doc) => ({
      ...doc,
      measurements: doc.measurements.filter((m) => m.measurement_ref !== measurement.measurement_ref),
    }),
    undo: (doc) => {
      const measurements = [...doc.measurements]
      measurements.splice(index, 0, measurement)
      return { ...doc, measurements }
    },
  }
}

// Whole-piece rotate/flip (transform.ts) replaces the entire document in one shot -- simplest
// correct undo is restoring the pre-transform document wholesale, same pattern as
// replaceShapeCommand above.
export function transformDocumentCommand(newDoc: PieceGeometryDocument, oldDoc: PieceGeometryDocument, label: string): Command {
  return {
    label,
    do: () => newDoc,
    undo: () => oldDoc,
  }
}
