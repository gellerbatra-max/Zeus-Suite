import type { DragEvent } from 'react'
import { useEffect, useState } from 'react'
import { Arrow, Circle, Group, Image as KonvaImage, Layer, Line, Rect, Stage, Text } from 'react-konva'
import type { KonvaEventObject } from 'konva/lib/Node'
import type { FuseBlockOut, MatchGuidanceOut, WeaveLine } from '../api/types'
import { boundingBoxesOverlap, weaveLineSegment } from '../geometry'

// Define Material / Material Pattern (Sec 1.4, "Show Marker's Pattern"): loads the fabric
// reference image as a plain HTMLImageElement for Konva's <Image> to draw, since this project has
// no image-loading hook dependency (e.g. `use-image`) -- this is the minimal equivalent.
function useHtmlImage(url: string | null | undefined): HTMLImageElement | null {
  const [image, setImage] = useState<HTMLImageElement | null>(null)
  useEffect(() => {
    if (!url) {
      setImage(null)
      return
    }
    const img = new window.Image()
    img.onload = () => setImage(img)
    img.src = url
    return () => {
      img.onload = null
    }
  }, [url])
  return image
}

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
  weaveLineOverride: { angleDeg: number; offset: number } | null
  stripeIndependentInSet: boolean
  blockBufferRuleNo: number | null
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
  weaveLine?: WeaveLine | null
  materialPatternUrl?: string | null
  fuseBlocks?: FuseBlockOut[]
  blockBufferRuleTypes?: Record<number, string>
  targetLength?: number | null
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
  weaveLine,
  materialPatternUrl,
  fuseBlocks = [],
  blockBufferRuleTypes = {},
  targetLength = null,
}: Props) {
  const materialImage = useHtmlImage(materialPatternUrl)
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
          {materialImage && (
            <KonvaImage
              image={materialImage} x={0} y={0} width={markerWidth} height={markerHeight}
              opacity={0.6} listening={false}
            />
          )}
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
              {p.stripeIndependentInSet && (
                // Stripe-only-in-a-set (Sec 1.4): marks a piece that manages its own stripe mark
                // independently of other pieces sharing its garment size, instead of the default
                // where assigning a mark to one syncs it across the whole size group.
                <Text text="S" x={12} y={0} fontSize={9} fontStyle="bold" fill="#8a2be2" />
              )}
              {p.blockBufferRuleNo != null && (
                // Block/Buffer toolbox toggle (Sec 1.6): "BL"/"BU" flag per the plan doc, per the
                // rule's type (defaults to "BU" if the rule table lookup isn't loaded yet).
                <Text
                  text={blockBufferRuleTypes[p.blockBufferRuleNo] === 'block' ? 'BL' : 'BU'}
                  x={p.width - 18} y={0} fontSize={9} fontStyle="bold" fill="#0f766e"
                />
              )}
            </Group>
          ))}
        </Layer>
        {weaveLine?.visible && (
          <Layer listening={false}>
            {(() => {
              const length = Math.sqrt(markerWidth ** 2 + markerHeight ** 2) * 1.5
              const seg = weaveLineSegment(
                weaveLine.angle_deg, weaveLine.offset, markerWidth / 2, markerHeight / 2, length,
              )
              return (
                <>
                  <Line points={[seg.x1, seg.y1, seg.x2, seg.y2]} stroke="#8a6d3b" strokeWidth={1} dash={[6, 4]} />
                  {/* "Font on Weaveline Upwards always" (Sec 1.4): the label is never rotated
                      with the line -- it always renders upright. */}
                  <Text text="WEAVE" x={seg.midX + 4} y={seg.midY - 14} fontSize={10} fill="#8a6d3b" />
                </>
              )
            })()}
          </Layer>
        )}
        {placements.some((p) => p.weaveLineOverride) && (
          // Per-piece weave-line override (Sec 1.4: "Edit Weave Line" for a single piece) --
          // a shorter segment scoped to just that piece's own bounding box, drawn in canvas
          // space (not inside the piece's own rotated Group) since the override angle is a
          // marker-space direction, independent of how the piece itself is rotated/flipped.
          <Layer listening={false}>
            {placements.map((p) => {
              if (!p.weaveLineOverride) return null
              const centerX = p.x + p.width / 2
              const centerY = p.y + p.height / 2
              const length = Math.sqrt(p.width ** 2 + p.height ** 2) * 1.2
              const seg = weaveLineSegment(p.weaveLineOverride.angleDeg, p.weaveLineOverride.offset, centerX, centerY, length)
              return (
                <Line
                  key={p.pieceId}
                  points={[seg.x1, seg.y1, seg.x2, seg.y2]}
                  stroke="#8a6d3b" strokeWidth={1.5} dash={[3, 3]}
                />
              )
            })}
          </Layer>
        )}
        {fuseBlocks.length > 0 && (
          <Layer listening={false}>
            {fuseBlocks.map((block) => {
              // Block Fuse settings (Sec 1.6): block_amount is "extra space added around a
              // grouped block" -- the stored x/y/width/height are the tight bbox of member
              // pieces, so the visual outline inflates it by block_amount on every side.
              const bx = block.x - block.block_amount
              const by = block.y - block.block_amount
              const bw = block.width + block.block_amount * 2
              const bh = block.height + block.block_amount * 2
              const notchY = by + bh / 2
              return (
                <Group key={block.id}>
                  <Rect x={bx} y={by} width={bw} height={bh} stroke="#0f766e" strokeWidth={1.5} dash={[8, 4]} />
                  {/* Block Notch (Sec 1.4/1.6): V-shaped mark at the cutter's Op-Stop pause
                      point, depth = Block Fuse Amount - Reduce Fuse Amount. No real cut-file
                      pipeline exists yet, so this is a visual/informational marker only. */}
                  <Line
                    points={[bx, notchY - 5, bx + 6, notchY, bx, notchY + 5]}
                    stroke="#0f766e" strokeWidth={1.5}
                  />
                  <Text text={`notch ${(block.block_amount - block.reduce_amount).toFixed(2)}`} x={bx + 10} y={notchY - 14} fontSize={9} fill="#0f766e" />
                </Group>
              )
            })}
          </Layer>
        )}
        {targetLength != null && (
          // Target line (Sec 1.7): a dotted marker-length target read from the order's
          // target_length -- drawn along the length axis (X, the same convention this app's
          // bite-boundary validation already assumes) so it reads as "cut fabric up to here".
          <Layer listening={false}>
            <Line points={[targetLength, 0, targetLength, markerHeight]} stroke="#8a2be2" strokeWidth={1.5} dash={[4, 4]} />
            <Text text="TARGET" x={targetLength + 4} y={4} fontSize={10} fill="#8a2be2" />
          </Layer>
        )}
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
