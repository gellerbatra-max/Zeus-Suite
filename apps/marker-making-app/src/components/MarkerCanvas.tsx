import type { DragEvent } from 'react'
import { Group, Layer, Rect, Stage, Text } from 'react-konva'
import type { KonvaEventObject } from 'konva/lib/Node'

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
}

interface Props {
  markerWidth: number
  markerHeight: number
  placements: CanvasPlacement[]
  onPlace: (pieceId: string, x: number, y: number) => void
  onMove: (pieceId: string, x: number, y: number) => void
  onSelect: (pieceId: string | null) => void
  selectedPieceId: string | null
}

function boundingBoxesOverlap(a: CanvasPlacement, b: CanvasPlacement): boolean {
  return a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y
}

export function MarkerCanvas({ markerWidth, markerHeight, placements, onPlace, onMove, onSelect, selectedPieceId }: Props) {
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
            </Group>
          ))}
        </Layer>
      </Stage>
    </div>
  )
}
