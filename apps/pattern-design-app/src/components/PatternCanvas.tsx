import { forwardRef, useImperativeHandle, useRef, useState } from 'react'
import { Arrow, Circle, Group, Image as KonvaImage, Layer, Line, Stage, Text } from 'react-konva'
import type Konva from 'konva'
import type {
  Annotation,
  Dart,
  FreePoint,
  GradeRuleTable,
  GrainLine,
  InternalLine,
  Measurement,
  Notch,
  Point,
  SeamAllowance,
} from '../api/types'
import { gradedPerimeter, nestColorFor } from '../grading'
import { computeMeasurement } from '../measurement'

// Geometry is authored/stored in real-world mm (pattern_design_plan.md Sec 3.3/6.2) and mapped to
// canvas pixels through a single zoom/pan transform shared by every layer -- Konva's Stage
// scale/position, rather than converting coordinates per-shape. 1 canvas pixel == 1mm at scale 1.
const CANVAS_WIDTH = 900
const CANVAS_HEIGHT = 600
const GRID_EXTENT = 3000
const GRID_STEP = 50
const MIN_SCALE = 0.2
const MAX_SCALE = 6

function buildGridLines(): number[][] {
  const lines: number[][] = []
  for (let x = -GRID_EXTENT; x <= GRID_EXTENT; x += GRID_STEP) {
    lines.push([x, -GRID_EXTENT, x, GRID_EXTENT])
  }
  for (let y = -GRID_EXTENT; y <= GRID_EXTENT; y += GRID_STEP) {
    lines.push([-GRID_EXTENT, y, GRID_EXTENT, y])
  }
  return lines
}

const GRID_LINES = buildGridLines()

function centroidOf(points: { x: number; y: number }[]): { x: number; y: number } {
  if (points.length === 0) return { x: 0, y: 0 }
  const sum = points.reduce((acc, p) => ({ x: acc.x + p.x, y: acc.y + p.y }), { x: 0, y: 0 })
  return { x: sum.x / points.length, y: sum.y / points.length }
}

// One tool is active at a time (pattern_design_plan.md Sec 6.3: "Tools are registered against the
// current mode ... so the same click-on-canvas gesture means different things per mode"):
//   draw        - click empty canvas adds a perimeter point
//   edit        - drag points to move them, double-click to delete
//   add-line    - click two existing points in sequence to connect them with an internal line
//   delete-line - click an internal line to delete it
//   seam        - click a perimeter edge to set its seam allowance
//   dart        - click three points in sequence (leg, apex, leg) to add a dart
//   notch       - click an existing perimeter point to toggle a notch there
//   grain-line  - click two points in sequence to set the piece's single grain line
//   grade       - click an existing perimeter point to set its X/Y delta for the active size step
//   annotate    - click anywhere to place a text note; click an existing note to remove it
//   measure     - click two existing points in sequence to define a spec measurement between them
export type Tool =
  | 'draw'
  | 'edit'
  | 'add-line'
  | 'delete-line'
  | 'seam'
  | 'dart'
  | 'notch'
  | 'grain-line'
  | 'grade'
  | 'annotate'
  | 'measure'

interface Props {
  points: Point[]
  internalLines: InternalLine[]
  seams: SeamAllowance[]
  darts: Dart[]
  notches: Notch[]
  grainLine: GrainLine | null
  gradeRuleTable: GradeRuleTable | null
  activeSizeStep: number | null
  showGradeNest: boolean
  annotations: Annotation[]
  measurements: Measurement[]
  referenceImage: HTMLImageElement | null
  referenceImageOpacity: number
  tool: Tool
  onAddPoint: (x: number, y: number) => void
  onMovePoint: (pointRef: string, from: { x: number; y: number }, to: { x: number; y: number }) => void
  onDeletePoint: (index: number) => void
  onAddLine: (pointRefA: string, pointRefB: string) => void
  onDeleteLine: (index: number) => void
  onSetSeam: (edgeRef: [string, string]) => void
  onAddDart: (legA: FreePoint, apex: FreePoint, legB: FreePoint) => void
  onToggleNotch: (pointRef: string) => void
  onSetGrainLine: (start: FreePoint, end: FreePoint) => void
  onGradePointClick: (pointRef: string) => void
  onAnnotatePick: (x: number, y: number) => void
  onDeleteAnnotation: (index: number) => void
  onMeasurePointClick: (pointRefA: string, pointRefB: string) => void
}

export const PatternCanvas = forwardRef<Konva.Stage, Props>(function PatternCanvas(
  {
    points,
    internalLines,
    seams,
    darts,
    notches,
    grainLine,
    gradeRuleTable,
    activeSizeStep,
    showGradeNest,
    annotations,
    measurements,
    referenceImage,
    referenceImageOpacity,
    tool,
    onAddPoint,
    onMovePoint,
    onDeletePoint,
    onAddLine,
    onDeleteLine,
    onSetSeam,
    onAddDart,
    onToggleNotch,
    onSetGrainLine,
    onGradePointClick,
    onAnnotatePick,
    onDeleteAnnotation,
    onMeasurePointClick,
  }: Props,
  forwardedRef,
) {
  const stageRef = useRef<Konva.Stage>(null)
  useImperativeHandle(forwardedRef, () => stageRef.current as Konva.Stage, [])
  const [scale, setScale] = useState(1)
  const [lineStartRef, setLineStartRef] = useState<string | null>(null)
  const [measureStartRef, setMeasureStartRef] = useState<string | null>(null)
  const [pendingClicks, setPendingClicks] = useState<{ x: number; y: number }[]>([])

  // A drag gesture only commits one movePointCommand, on drag end -- not one per mousemove
  // event, which would flood the undo stack. dragOriginRef remembers the pre-drag position for
  // that single command's "from"; liveDrag overrides the dragged point's rendered coordinates
  // (for the perimeter outline and any attached internal lines) while the gesture is in progress,
  // purely a rendering concern that never touches the geometry document itself.
  const dragOriginRef = useRef<{ x: number; y: number } | null>(null)
  const [liveDrag, setLiveDrag] = useState<{ ref: string; x: number; y: number } | null>(null)

  const effectivePoints =
    liveDrag === null ? points : points.map((p) => (p.point_ref === liveDrag.ref ? { ...p, x: liveDrag.x, y: liveDrag.y } : p))
  const pointsByRef = new Map(effectivePoints.map((p) => [p.point_ref, p]))
  const notchedRefs = new Set(notches.map((n) => n.point_ref))
  const centroid = centroidOf(effectivePoints)
  const gradedForActiveStep = new Set(
    activeSizeStep === null
      ? []
      : (gradeRuleTable?.rules ?? []).filter((r) => r.size_step === activeSizeStep).map((r) => r.point_ref),
  )

  const handleWheel = (e: Konva.KonvaEventObject<WheelEvent>) => {
    e.evt.preventDefault()
    const stage = stageRef.current
    if (!stage) return
    const oldScale = stage.scaleX()
    const pointer = stage.getPointerPosition()
    if (!pointer) return
    const mousePointTo = { x: (pointer.x - stage.x()) / oldScale, y: (pointer.y - stage.y()) / oldScale }
    const factor = 1.05
    const newScale = e.evt.deltaY > 0 ? oldScale / factor : oldScale * factor
    const clamped = Math.min(Math.max(newScale, MIN_SCALE), MAX_SCALE)
    stage.scale({ x: clamped, y: clamped })
    stage.position({ x: pointer.x - mousePointTo.x * clamped, y: pointer.y - mousePointTo.y * clamped })
    setScale(clamped)
  }

  // Shared by both an empty-canvas click (dart apex, grain line endpoints don't have to land on
  // an existing point) and a click on an existing point (dart legs / grain line often do) --
  // either way, this tool only cares about the (x, y) that was clicked.
  const handleFreePick = (x: number, y: number) => {
    if (tool === 'dart') {
      const next = [...pendingClicks, { x, y }]
      if (next.length < 3) {
        setPendingClicks(next)
        return
      }
      const [a, apex, b] = next
      onAddDart(
        { point_ref: crypto.randomUUID(), x: a.x, y: a.y },
        { point_ref: crypto.randomUUID(), x: apex.x, y: apex.y },
        { point_ref: crypto.randomUUID(), x: b.x, y: b.y },
      )
      setPendingClicks([])
    } else if (tool === 'grain-line') {
      const next = [...pendingClicks, { x, y }]
      if (next.length < 2) {
        setPendingClicks(next)
        return
      }
      const [start, end] = next
      onSetGrainLine(
        { point_ref: crypto.randomUUID(), x: start.x, y: start.y },
        { point_ref: crypto.randomUUID(), x: end.x, y: end.y },
      )
      setPendingClicks([])
    } else if (tool === 'annotate') {
      onAnnotatePick(x, y)
    }
  }

  const pickAtPointer = () => {
    const stage = stageRef.current
    const pos = stage?.getRelativePointerPosition()
    if (!pos) return
    handleFreePick(Math.round(pos.x), Math.round(pos.y))
  }

  const handleStageClick = (e: Konva.KonvaEventObject<MouseEvent | TouchEvent>) => {
    if (e.target !== e.target.getStage()) return // a point/line/edge handles its own click
    const stage = stageRef.current
    const pos = stage?.getRelativePointerPosition()
    if (!pos) return
    if (tool === 'draw') onAddPoint(Math.round(pos.x), Math.round(pos.y))
    else handleFreePick(Math.round(pos.x), Math.round(pos.y))
  }

  // The perimeter is a filled shape once closed, so a dart-apex, grain-line, or annotation click
  // that lands *inside* the piece (the common case) hits this Line instead of empty stage, and
  // would otherwise be silently swallowed by handleStageClick's "only empty canvas" guard above.
  const handlePerimeterClick = () => {
    if (tool === 'dart' || tool === 'grain-line' || tool === 'annotate') pickAtPointer()
  }

  const handlePointClick = (pointRef: string, x: number, y: number) => {
    if (tool === 'add-line') {
      if (lineStartRef === null) {
        setLineStartRef(pointRef)
        return
      }
      if (lineStartRef !== pointRef) onAddLine(lineStartRef, pointRef)
      setLineStartRef(null)
    } else if (tool === 'notch') {
      onToggleNotch(pointRef)
    } else if (tool === 'dart' || tool === 'grain-line') {
      handleFreePick(x, y)
    } else if (tool === 'grade') {
      onGradePointClick(pointRef)
    } else if (tool === 'measure') {
      if (measureStartRef === null) {
        setMeasureStartRef(pointRef)
        return
      }
      if (measureStartRef !== pointRef) onMeasurePointClick(measureStartRef, pointRef)
      setMeasureStartRef(null)
    }
  }

  const flatPoints = effectivePoints.flatMap((p) => [p.x, p.y])
  const edges: [Point, Point][] =
    effectivePoints.length >= 3
      ? effectivePoints.map((p, i) => [p, effectivePoints[(i + 1) % effectivePoints.length]])
      : effectivePoints.length === 2
        ? [[effectivePoints[0], effectivePoints[1]]]
        : []

  return (
    <div className="pattern-canvas">
      <Stage
        ref={stageRef}
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        x={CANVAS_WIDTH / 2}
        y={CANVAS_HEIGHT / 2}
        draggable={tool !== 'draw'}
        onWheel={handleWheel}
        onClick={handleStageClick}
        onTap={handleStageClick}
      >
        {/* Background/grid layer (pattern_design_plan.md Sec 6.1): redrawn only on zoom/pan, never on edit. */}
        <Layer listening={false}>
          {GRID_LINES.map((pts, i) => (
            <Line key={i} points={pts} stroke="#eceef2" strokeWidth={1 / scale} />
          ))}
          <Line points={[-GRID_EXTENT, 0, GRID_EXTENT, 0]} stroke="#9aa1af" strokeWidth={1.5 / scale} />
          <Line points={[0, -GRID_EXTENT, 0, GRID_EXTENT]} stroke="#9aa1af" strokeWidth={1.5 / scale} />
        </Layer>

        {/* Digitized-source overlay layer (pattern_design_plan.md Sec 6.1/6.5): a scanned/
            photographed pattern shown at reduced opacity under the geometry layer so the operator
            can trace over it with the Draw tool. Client-side only in this slice -- the image is
            loaded via the browser's File API and never uploaded/persisted (see App.tsx); real
            camera-capture calibration and server-side contour auto-detection are deferred. */}
        {referenceImage && (
          <Layer listening={false} opacity={referenceImageOpacity}>
            <KonvaImage
              image={referenceImage}
              x={-referenceImage.width / 2}
              y={-referenceImage.height / 2}
              width={referenceImage.width}
              height={referenceImage.height}
            />
          </Layer>
        )}

        {/* Piece geometry layer: perimeter, internal lines, seams, darts, notches, grain line. */}
        <Layer>
          {points.length >= 2 && (
            <Line
              points={flatPoints}
              closed={points.length >= 3}
              stroke="#2e5aac"
              strokeWidth={2 / scale}
              fill="rgba(46,90,172,0.08)"
              onClick={handlePerimeterClick}
              onTap={handlePerimeterClick}
            />
          )}

          {/* Invisible-ish per-edge hit targets, only interactive in the seam tool -- the visible
              perimeter Line above is one shape and can't report which segment was clicked. */}
          {tool === 'seam' &&
            edges.map(([a, b], i) => (
              <Line
                key={`edge-${i}`}
                points={[a.x, a.y, b.x, b.y]}
                stroke="#2e5aac"
                strokeWidth={2 / scale}
                hitStrokeWidth={16 / scale}
                onClick={() => onSetSeam([a.point_ref, b.point_ref])}
                onTap={() => onSetSeam([a.point_ref, b.point_ref])}
              />
            ))}

          {seams.map((seam) => {
            const a = pointsByRef.get(seam.edge_ref[0])
            const b = pointsByRef.get(seam.edge_ref[1])
            if (!a || !b) return null
            const dx = b.x - a.x
            const dy = b.y - a.y
            const len = Math.hypot(dx, dy) || 1
            let px = -dy / len
            let py = dx / len
            const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }
            // Point the offset away from the piece's centroid, i.e. outward.
            if (px * (mid.x - centroid.x) + py * (mid.y - centroid.y) < 0) {
              px = -px
              py = -py
            }
            const offset = seam.allowance_mm
            const oa = { x: a.x + px * offset, y: a.y + py * offset }
            const ob = { x: b.x + px * offset, y: b.y + py * offset }
            return (
              <Line
                key={`seam-${seam.edge_ref.join('-')}`}
                points={[oa.x, oa.y, ob.x, ob.y]}
                stroke="#1e7e34"
                strokeWidth={1.5 / scale}
                dash={[6 / scale, 3 / scale]}
                listening={false}
              />
            )
          })}

          {internalLines.map((line, i) => {
            const a = pointsByRef.get(line.point_refs[0])
            const b = pointsByRef.get(line.point_refs[1])
            if (!a || !b) return null
            return (
              <Line
                key={line.line_ref}
                points={[a.x, a.y, b.x, b.y]}
                stroke={tool === 'delete-line' ? '#b3261e' : '#5a7dc4'}
                strokeWidth={2 / scale}
                dash={[8 / scale, 4 / scale]}
                hitStrokeWidth={12 / scale}
                onClick={() => tool === 'delete-line' && onDeleteLine(i)}
                onTap={() => tool === 'delete-line' && onDeleteLine(i)}
              />
            )
          })}

          {darts.map((dart) => (
            <Line
              key={dart.dart_ref}
              points={[dart.leg_a.x, dart.leg_a.y, dart.apex.x, dart.apex.y, dart.leg_b.x, dart.leg_b.y]}
              stroke="#b3261e"
              strokeWidth={1.5 / scale}
              listening={false}
            />
          ))}
          {darts.map((dart) => (
            <Text
              key={`${dart.dart_ref}-label`}
              x={dart.apex.x + 6 / scale}
              y={dart.apex.y}
              text={`${dart.intake_mm}mm`}
              fontSize={11 / scale}
              fill="#b3261e"
              listening={false}
            />
          ))}

          {notches.map((notch) => {
            const p = pointsByRef.get(notch.point_ref)
            if (!p) return null
            const dx = centroid.x - p.x
            const dy = centroid.y - p.y
            const len = Math.hypot(dx, dy) || 1
            const tipX = p.x + (dx / len) * notch.depth_mm
            const tipY = p.y + (dy / len) * notch.depth_mm
            return (
              <Line
                key={`notch-${notch.point_ref}`}
                points={[p.x, p.y, tipX, tipY]}
                stroke="#7a5c00"
                strokeWidth={2.5 / scale}
                listening={false}
              />
            )
          })}

          {grainLine && (
            <Arrow
              points={[grainLine.start.x, grainLine.start.y, grainLine.end.x, grainLine.end.y]}
              stroke="#1a1a1e"
              fill="#1a1a1e"
              strokeWidth={1.5 / scale}
              pointerAtBeginning
              pointerAtEnding
              pointerLength={8 / scale}
              pointerWidth={6 / scale}
              listening={false}
            />
          )}

          {measurements.map((m) => {
            const { actualMm, withinTolerance } = computeMeasurement(m, pointsByRef)
            const a = pointsByRef.get(m.point_ref_a)
            const b = pointsByRef.get(m.point_ref_b)
            if (!a || !b || actualMm === null) return null
            const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }
            const statusColor = withinTolerance === null ? '#0a7ea4' : withinTolerance ? '#1e7e34' : '#b3261e'
            const statusMark = withinTolerance === null ? '' : withinTolerance ? ' ✓' : ' ✗'
            return (
              <Group key={m.measurement_ref} listening={false}>
                <Line points={[a.x, a.y, b.x, b.y]} stroke={statusColor} strokeWidth={1 / scale} dash={[3 / scale, 3 / scale]} />
                <Text
                  x={mid.x + 4 / scale}
                  y={mid.y - 16 / scale}
                  text={`${m.label}: ${actualMm.toFixed(1)}mm${statusMark}`}
                  fontSize={11 / scale}
                  fill={statusColor}
                />
              </Group>
            )
          })}

          {annotations.map((a, i) => (
            <Group
              key={a.annotation_ref}
              x={a.x}
              y={a.y}
              onClick={() => tool === 'annotate' && onDeleteAnnotation(i)}
              onTap={() => tool === 'annotate' && onDeleteAnnotation(i)}
            >
              <Text
                text={a.text}
                fontSize={12 / scale}
                fill="#1a1a1e"
                padding={3 / scale}
                fontStyle="italic"
              />
            </Group>
          ))}

          {pendingClicks.map((c, i) => (
            <Circle key={`pending-${i}`} x={c.x} y={c.y} radius={4 / scale} fill="#ffb84d" listening={false} />
          ))}

          {effectivePoints.map((p, i) => (
            <Circle
              key={p.point_ref}
              x={p.x}
              y={p.y}
              radius={5 / scale}
              fill={
                p.point_ref === lineStartRef || p.point_ref === measureStartRef || notchedRefs.has(p.point_ref)
                  ? '#ffb84d'
                  : gradedForActiveStep.has(p.point_ref)
                    ? '#8e44ad'
                    : '#ffffff'
              }
              stroke="#2e5aac"
              strokeWidth={1.5 / scale}
              draggable={tool === 'edit'}
              onDragStart={(e) => {
                dragOriginRef.current = { x: e.target.x(), y: e.target.y() }
              }}
              onDragMove={(e) =>
                setLiveDrag({ ref: p.point_ref, x: Math.round(e.target.x()), y: Math.round(e.target.y()) })
              }
              onDragEnd={(e) => {
                const from = dragOriginRef.current
                dragOriginRef.current = null
                setLiveDrag(null)
                if (!from) return
                const to = { x: Math.round(e.target.x()), y: Math.round(e.target.y()) }
                if (from.x !== to.x || from.y !== to.y) onMovePoint(p.point_ref, from, to)
              }}
              onDblClick={() => tool === 'edit' && onDeletePoint(i)}
              onDblTap={() => tool === 'edit' && onDeletePoint(i)}
              onClick={() => handlePointClick(p.point_ref, p.x, p.y)}
              onTap={() => handlePointClick(p.point_ref, p.x, p.y)}
            />
          ))}
        </Layer>

        {/* Grade-nest overlay layer (pattern_design_plan.md Sec 6.1): every other size's outline,
            low-opacity and color-coded, drawn on top of the base-size outline above. Its own layer
            so toggling it is a visibility flip, not a re-render of the (potentially large)
            geometry layer underneath. */}
        {showGradeNest && gradeRuleTable && points.length >= 3 && (
          <Layer listening={false}>
            {gradeRuleTable.size_range
              .filter((size) => size !== gradeRuleTable.base_size)
              .map((size, i) => {
                const outline = gradedPerimeter(points, gradeRuleTable, size)
                const flat = outline.flatMap((p) => [p.x, p.y])
                return (
                  <Line key={size} points={flat} closed stroke={nestColorFor(i)} strokeWidth={1.5 / scale} opacity={0.55} />
                )
              })}
            {gradeRuleTable.size_range
              .filter((size) => size !== gradeRuleTable.base_size)
              .map((size, i) => {
                const outline = gradedPerimeter(points, gradeRuleTable, size)
                const label = outline[0]
                if (!label) return null
                return (
                  <Text
                    key={`${size}-label`}
                    x={label.x + 6 / scale}
                    y={label.y - 14 / scale}
                    text={size}
                    fontSize={12 / scale}
                    fill={nestColorFor(i)}
                    opacity={0.85}
                  />
                )
              })}
          </Layer>
        )}
      </Stage>
      <div className="pattern-canvas__hint">
        {tool === 'draw' && 'Click to add perimeter points.'}
        {tool === 'edit' && 'Drag to pan, scroll to zoom, drag a point to move it, double-click to delete it.'}
        {tool === 'add-line' &&
          (lineStartRef ? 'Click a second point to connect it.' : 'Click a point to start an internal line.')}
        {tool === 'delete-line' && 'Click an internal line to delete it.'}
        {tool === 'seam' && 'Click a perimeter edge to set its seam allowance.'}
        {tool === 'dart' &&
          `Click leg, apex, leg in order to add a dart (${pendingClicks.length}/3 picked).`}
        {tool === 'notch' && 'Click a perimeter point to add or remove a notch.'}
        {tool === 'grain-line' &&
          `Click two points to set the grain line (${pendingClicks.length}/2 picked).`}
        {tool === 'grade' &&
          (activeSizeStep === null
            ? 'Set a size range and pick a step to grade first.'
            : 'Click a perimeter point to set its X/Y delta for the active step.')}
        {tool === 'annotate' && 'Click to place a note. Click an existing note to remove it.'}
        {tool === 'measure' &&
          (measureStartRef ? 'Click a second point to measure to.' : 'Click a point to start a measurement.')}
      </div>
    </div>
  )
})
