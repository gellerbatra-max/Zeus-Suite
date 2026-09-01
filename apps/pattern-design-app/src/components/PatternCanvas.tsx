import { useRef, useState } from 'react'
import { Circle, Layer, Line, Stage } from 'react-konva'
import type Konva from 'konva'
import type { InternalLine, Point } from '../api/types'

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

// One tool is active at a time (pattern_design_plan.md Sec 6.3: "Tools are registered against the
// current mode ... so the same click-on-canvas gesture means different things per mode"):
//   draw        - click empty canvas adds a perimeter point
//   edit        - drag points to move them, double-click to delete
//   add-line    - click two existing points in sequence to connect them with an internal line
//   delete-line - click an internal line to delete it
export type Tool = 'draw' | 'edit' | 'add-line' | 'delete-line'

interface Props {
  points: Point[]
  internalLines: InternalLine[]
  tool: Tool
  onAddPoint: (x: number, y: number) => void
  onMovePoint: (pointRef: string, from: { x: number; y: number }, to: { x: number; y: number }) => void
  onDeletePoint: (index: number) => void
  onAddLine: (pointRefA: string, pointRefB: string) => void
  onDeleteLine: (index: number) => void
}

export function PatternCanvas({
  points,
  internalLines,
  tool,
  onAddPoint,
  onMovePoint,
  onDeletePoint,
  onAddLine,
  onDeleteLine,
}: Props) {
  const stageRef = useRef<Konva.Stage>(null)
  const [scale, setScale] = useState(1)
  const [lineStartRef, setLineStartRef] = useState<string | null>(null)

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

  const handleStageClick = (e: Konva.KonvaEventObject<MouseEvent | TouchEvent>) => {
    // Points/lines are only draggable/clickable in the other three tools (see the Circle/Line
    // props below), so a plain stage click here always means "empty canvas" once tool === 'draw'.
    if (tool !== 'draw') return
    if (e.target !== e.target.getStage()) return // clicked a point, not empty canvas
    const stage = stageRef.current
    const pos = stage?.getRelativePointerPosition()
    if (!pos) return
    onAddPoint(Math.round(pos.x), Math.round(pos.y))
  }

  const handlePointClick = (pointRef: string) => {
    if (tool !== 'add-line') return
    if (lineStartRef === null) {
      setLineStartRef(pointRef)
      return
    }
    if (lineStartRef !== pointRef) {
      onAddLine(lineStartRef, pointRef)
    }
    setLineStartRef(null)
  }

  const flatPoints = effectivePoints.flatMap((p) => [p.x, p.y])

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

        {/* Piece geometry layer: perimeter + internal lines (Phase 2.2). Seams, darts, notches, and
            grain line are Phase 2.3. */}
        <Layer>
          {points.length >= 2 && (
            <Line
              points={flatPoints}
              closed={points.length >= 3}
              stroke="#2e5aac"
              strokeWidth={2 / scale}
              fill="rgba(46,90,172,0.08)"
            />
          )}

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

          {effectivePoints.map((p, i) => (
            <Circle
              key={p.point_ref}
              x={p.x}
              y={p.y}
              radius={5 / scale}
              fill={p.point_ref === lineStartRef ? '#ffb84d' : '#ffffff'}
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
              onClick={() => handlePointClick(p.point_ref)}
              onTap={() => handlePointClick(p.point_ref)}
            />
          ))}
        </Layer>
      </Stage>
      <div className="pattern-canvas__hint">
        {tool === 'draw' && 'Click to add perimeter points.'}
        {tool === 'edit' && 'Drag to pan, scroll to zoom, drag a point to move it, double-click to delete it.'}
        {tool === 'add-line' &&
          (lineStartRef ? 'Click a second point to connect it.' : 'Click a point to start an internal line.')}
        {tool === 'delete-line' && 'Click an internal line to delete it.'}
      </div>
    </div>
  )
}
