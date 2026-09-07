import { useEffect, useMemo, useRef, useState } from 'react'
import { Stage, Layer, Line, Circle, Text } from 'react-konva'
import type Konva from 'konva'
import type { MigrationDiff, MigrationGeometry, SourceSummary } from '../api/types'

// Mirrors pattern-design-app's PatternCanvas.tsx conventions (format_interchange_plan.md Sec 6:
// "same Konva.js/canvas renderer as Pattern Design... so overlay/measure/snap-to-geometry behave
// identically to any other canvas surface in the suite") -- there's no shared npm package between
// the two apps, so this is a standalone component mirroring that one's approach rather than
// importing its code: 1px = 1mm, no Y-flip (screen Y matches geometry Y directly), wheel-zoom
// clamped to [0.2, 6] centered on the pointer, and stroke widths/radii divided by scale so they
// stay visually constant regardless of zoom.

const MIN_SCALE = 0.2
const MAX_SCALE = 6

interface MeasurePoint {
  x: number
  y: number
  label: string
}

interface Props {
  converted: MigrationGeometry | null
  sourceSummary: SourceSummary | null
  diff: MigrationDiff | null
  width?: number
  height?: number
}

export function MigrationCanvas({ converted, sourceSummary, diff, width = 720, height = 480 }: Props) {
  const stageRef = useRef<Konva.Stage>(null)
  const [scale, setScale] = useState(1)
  const [stagePos, setStagePos] = useState({ x: width / 2, y: height / 2 })
  const [snapToGeometry, setSnapToGeometry] = useState(false)
  const [pendingPoint, setPendingPoint] = useState<MeasurePoint | null>(null)
  const [measurement, setMeasurement] = useState<{ a: MeasurePoint; b: MeasurePoint } | null>(null)

  // Fit the view to the converted outline's bounding box whenever a new item is loaded.
  useEffect(() => {
    if (!converted || converted.perimeter.length === 0) return
    const xs = converted.perimeter.map((p) => p.x)
    const ys = converted.perimeter.map((p) => p.y)
    const minX = Math.min(...xs)
    const maxX = Math.max(...xs)
    const minY = Math.min(...ys)
    const maxY = Math.max(...ys)
    const spanX = Math.max(maxX - minX, 1)
    const spanY = Math.max(maxY - minY, 1)
    const fitScale = Math.min((width - 80) / spanX, (height - 80) / spanY, MAX_SCALE)
    const cx = (minX + maxX) / 2
    const cy = (minY + maxY) / 2
    setScale(fitScale)
    setStagePos({ x: width / 2 - cx * fitScale, y: height / 2 - cy * fitScale })
    setPendingPoint(null)
    setMeasurement(null)
  }, [converted, width, height])

  const rawOutline = useMemo(
    () => (sourceSummary ? sourceSummary.raw_lines.filter((l) => l.label === 'OUTLINE').map((l) => ({ x: l.x1, y: l.y1 })) : []),
    [sourceSummary],
  )
  const rawNotches = useMemo(
    () => (sourceSummary ? sourceSummary.raw_points.filter((p) => p.label === 'NOTCH') : []),
    [sourceSummary],
  )

  // Sec 2.5's "Snap to Geometry": translate the raw overlay by the diff's own computed offset so
  // only true shape differences remain visible, instead of an incidental origin offset.
  const snapOffset =
    snapToGeometry && diff?.perimeter_offset
      ? {
          dx: diff.perimeter_offset.magnitude_mm * Math.cos((diff.perimeter_offset.direction_deg * Math.PI) / 180),
          dy: diff.perimeter_offset.magnitude_mm * Math.sin((diff.perimeter_offset.direction_deg * Math.PI) / 180),
        }
      : { dx: 0, dy: 0 }

  const rawOutlineFlat = rawOutline.flatMap((p) => [p.x + snapOffset.dx, p.y + snapOffset.dy])
  const convertedOutlineFlat = converted ? converted.perimeter.flatMap((p) => [p.x, p.y]) : []

  const notchCoordByRef = useMemo(() => {
    const byRef = new Map(converted?.perimeter.map((p) => [p.point_ref, p]) ?? [])
    return (ref: string) => byRef.get(ref)
  }, [converted])

  const clickablePoints: MeasurePoint[] = useMemo(() => {
    const points: MeasurePoint[] = (converted?.perimeter ?? []).map((p) => ({ x: p.x, y: p.y, label: p.point_ref }))
    if (converted?.grain_line) {
      points.push({ x: converted.grain_line.start.x, y: converted.grain_line.start.y, label: 'grain-start' })
      points.push({ x: converted.grain_line.end.x, y: converted.grain_line.end.y, label: 'grain-end' })
    }
    return points
  }, [converted])

  const handleWheel = (e: Konva.KonvaEventObject<WheelEvent>) => {
    e.evt.preventDefault()
    const stage = stageRef.current
    const pointer = stage?.getPointerPosition()
    if (!stage || !pointer) return
    const mousePointTo = { x: (pointer.x - stagePos.x) / scale, y: (pointer.y - stagePos.y) / scale }
    const direction = e.evt.deltaY > 0 ? -1 : 1
    const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale * (1 + direction * 0.08)))
    setScale(newScale)
    setStagePos({ x: pointer.x - mousePointTo.x * newScale, y: pointer.y - mousePointTo.y * newScale })
  }

  const handlePointClick = (pt: MeasurePoint) => {
    if (!pendingPoint) {
      setPendingPoint(pt)
      setMeasurement(null)
      return
    }
    setMeasurement({ a: pendingPoint, b: pt })
    setPendingPoint(null)
  }

  const sw = (base: number) => base / scale
  const r = (base: number) => base / scale

  return (
    <div className="migration-canvas">
      <div className="migration-canvas__toolbar">
        <label>
          <input type="checkbox" checked={snapToGeometry} onChange={(e) => setSnapToGeometry(e.target.checked)} />
          Snap to Geometry
        </label>
        {pendingPoint && <span className="hint">Click a second point to measure from {pendingPoint.label}…</span>}
        {measurement && (
          <span className="hint">
            {measurement.a.label} → {measurement.b.label}: {Math.hypot(measurement.b.x - measurement.a.x, measurement.b.y - measurement.a.y).toFixed(1)}mm
          </span>
        )}
      </div>
      <Stage
        ref={stageRef}
        width={width}
        height={height}
        scaleX={scale}
        scaleY={scale}
        x={stagePos.x}
        y={stagePos.y}
        draggable
        onWheel={handleWheel}
        onDragEnd={(e) => setStagePos({ x: e.target.x(), y: e.target.y() })}
        style={{ background: '#fafafa', border: '1px solid #d8d8dc', borderRadius: 6 }}
      >
        <Layer listening={false}>
          {rawOutlineFlat.length >= 6 && (
            <Line points={rawOutlineFlat} closed stroke="#9aa0ec" strokeWidth={sw(1.5)} dash={[sw(6), sw(4)]} opacity={0.7} />
          )}
          {rawNotches.map((n, i) => (
            <Circle key={i} x={n.x + snapOffset.dx} y={n.y + snapOffset.dy} radius={r(4)} stroke="#6a6ad1" strokeWidth={sw(1)} opacity={0.7} />
          ))}
        </Layer>

        <Layer>
          {convertedOutlineFlat.length >= 6 && <Line points={convertedOutlineFlat} closed stroke="#1a1a1e" strokeWidth={sw(2)} />}
          {converted?.grain_line && (
            <Line
              points={[converted.grain_line.start.x, converted.grain_line.start.y, converted.grain_line.end.x, converted.grain_line.end.y]}
              stroke="#2e5aac"
              strokeWidth={sw(1.5)}
            />
          )}
          {converted?.notches.map((n) => {
            const p = notchCoordByRef(n.point_ref)
            if (!p) return null
            return <Circle key={n.point_ref} x={p.x} y={p.y} radius={r(5)} fill="#c96a2e" />
          })}
          {clickablePoints.map((pt) => (
            <Circle
              key={pt.label}
              x={pt.x}
              y={pt.y}
              radius={r(5)}
              fill={pendingPoint?.label === pt.label ? '#2e5aac' : '#ffffff'}
              stroke="#1a1a1e"
              strokeWidth={sw(1)}
              onClick={() => handlePointClick(pt)}
              onTap={() => handlePointClick(pt)}
            />
          ))}
          {diff?.notches.added.map((n, i) => (
            <Circle key={`added-${i}`} x={n.x} y={n.y} radius={r(9)} stroke="#1e7e34" strokeWidth={sw(1.5)} />
          ))}
          {diff?.notches.removed.map((n, i) => (
            <Circle key={`removed-${i}`} x={n.x} y={n.y} radius={r(9)} stroke="#b3261e" strokeWidth={sw(1.5)} dash={[sw(3), sw(3)]} />
          ))}
          {diff?.moved_points.map((m, i) => (
            <Line key={`moved-${i}`} points={[m.before.x, m.before.y, m.after.x, m.after.y]} stroke="#b3261e" strokeWidth={sw(1.5)} dash={[sw(3), sw(3)]} />
          ))}
          {measurement && (
            <>
              <Line
                points={[measurement.a.x, measurement.a.y, measurement.b.x, measurement.b.y]}
                stroke="#2e5aac"
                strokeWidth={sw(1)}
                dash={[sw(4), sw(4)]}
              />
              <Text
                x={(measurement.a.x + measurement.b.x) / 2}
                y={(measurement.a.y + measurement.b.y) / 2}
                text={`${Math.hypot(measurement.b.x - measurement.a.x, measurement.b.y - measurement.a.y).toFixed(1)}mm`}
                fontSize={12 / scale}
                fill="#2e5aac"
              />
            </>
          )}
        </Layer>
      </Stage>
    </div>
  )
}
