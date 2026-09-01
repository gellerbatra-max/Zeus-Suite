// Every drawing/editing tool is a command object with do()/undo() over the geometry document --
// pattern_design_plan.md Sec 6.3: "the same command list backs undo/redo and, on save, is what
// gets diffed against the last-saved geometry document." This slice doesn't diff on save (every
// save still round-trips the whole document, per Phase 2.1), but the do/undo pairing is exactly
// the shape that diffing would build on, and it's what backs the undo/redo stack now.

import type { InternalLine, PieceGeometryDocument, Point } from './api/types'

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
