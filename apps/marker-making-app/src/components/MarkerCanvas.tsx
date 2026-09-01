import type { DragEvent } from 'react'
import { Arrow, Circle, Group, Layer, Rect, Stage, Text } from 'react-konva'
import type { KonvaEventObject } from 'konva/lib/Node'
import type { MatchGuidanceOut } from '../api/types'
import { boundingBoxesOverlap } from '../geometry'

export interface CanvasPlacement {
  pieceId: string
  pieceCode: string
  x: number
  y: number
  rotationDeg: number
  flipX: boolean
  flipY: boolean
  width: number
  height: number
  sizeCode: string
  quantity: number
  stripeMarkId: string | null
  cutterStripeNeeded: boolean
}

interface Props {
  markerWidth: number
  markerHeight: number
  placements: CanvasPlacement[]
  onPlace: (pieceId: string, x: number, y: number) => void
  onMove: (pieceId: string, x: number, y: number) => void
  onDragMove?: (pieceId: string, x: number, y: number) => void
  onSelect: (pieceId: string | null) => void
  selectedPieceId: string | null
  guidance?: { pieceId: string; result: MatchGuidanceOut } | null
}

export function MarkerCanvas({
  markerWidth,
  markerHeight,
  placements,
  onPlace,
  onMove,
  onDragMove,
  onSelect,
  selectedPieceId,
  guidance,
}: Props) {
  const overlapping = new Set<string>()
  for (let i = 0; i < placements.length; i++) {
    for (let j = i + 1; j < placements.length; j++) {
      if (boundingBoxesOverlap(placements[i], placements[j])) {
        overlapping.add(placements[i].pieceId)
        overlapping.add(placements[j].pieceId)
      }
    }
  }

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const pieceId = e.dataTransfer.getData('text/piece-id')
    if (!pieceId) return
    const bounds = e.currentTarget.getBoundingClientRect()
    onPlace(pieceId, Math.max(0, e.clientX - bounds.left), Math.max(0, e.clientY - bounds.top))
  }

  const handleStageMouseDown = (e: KonvaEventObject<MouseEvent>) => {
    if (e.target === e.target.getStage()) onSelect(null)
  }

  return (
    <div className="marker-canvas" onDragOver={(e) => e.preventDefault()} onDrop={handleDrop}>
      <Stage width={markerWidth} height={markerHeight} onMouseDown={handleStageMouseDown}>
        <Layer>
          <Rect x={0} y={0} width={markerWidth} height={markerHeight} stroke="#333333" strokeWidth={2} />
          {placements.map((p) => (
            <Group
              key={p.pieceId}
              x={p.x}
              y={p.y}
              draggable
              onDragMove={(e) => onDragMove?.(p.pieceId, e.target.x(), e.target.y())}
              onDragEnd={(e) => onMove(p.pieceId, e.target.x(), e.target.y())}
              onClick={() => onSelect(p.pieceId)}
              onTap={() => onSelect(p.pieceId)}
              rotation={p.rotationDeg}
              scaleX={p.flipX ? -1 : 1}
              scaleY={p.flipY ? -1 : 1}
            >
              <Rect
                width={p.width}
                height={p.height}
                fill={selectedPieceId === p.pieceId ? '#dbe7ff' : '#f6f6f7'}
                stroke={overlapping.has(p.pieceId) ? '#c0392b' : '#555555'}
                strokeWidth={overlapping.has(p.pieceId) ? 3 : 1}
              />
              <Text
                text={p.pieceCode}
                width={p.width}
                height={p.height}
                align="center"
                verticalAlign="middle"
                fontSize={11}
                scaleX={p.flipX ? -1 : 1}
                scaleY={p.flipY ? -1 : 1}
                x={p.flipX ? p.width : 0}
                y={p.flipY ? p.height : 0}
              />
              {p.stripeMarkId && (
                // Cutter stripe setup (Sec 1.4): orange while the piece still needs
                // auto-cutter stripe matching, blue once it's been marked as not needed.
                <Circle
                  x={6} y={6} radius={4}
                  fill={p.cutterStripeNeeded ? '#e08600' : '#2e5aac'}
                  stroke="#ffffff"
                  strokeWidth={1}
                />
              )}
            </Group>
          ))}
        </Layer>
        {guidance && guidance.result.targets.length > 0 && (
          <Layer listening={false}>
            {guidance.result.targets.map((target, i) => {
              const piece = placements.find((p) => p.pieceId === guidance.pieceId)
              if (!piece) return null
              const fromX = piece.x + piece.width / 2
              const fromY = piece.y + piece.height / 2
              return (
                <Arrow
                  key={i}
                  points={[fromX, fromY, target.target_x, target.target_y]}
                  stroke="#2e8b57"
                  fill="#2e8b57"
                  strokeWidth={2}
                  pointerLength={8}
                  pointerWidth={8}
                />
              )
            })}
          </Layer>
        )}
      </Stage>
    </div>
  )
}
