import type { DragEvent } from 'react'
import type { WorkspacePiece } from '../api/types'

interface Props {
  pieces: WorkspacePiece[]
}

export function PieceTray({ pieces }: Props) {
  const handleDragStart = (e: DragEvent<HTMLDivElement>, pieceId: string) => {
    e.dataTransfer.setData('text/piece-id', pieceId)
  }

  return (
    <div className="piece-tray">
      <h3>Unplaced Pieces ({pieces.length})</h3>
      {pieces.length === 0 && <p className="hint">All pieces placed.</p>}
      {pieces.map((piece) => (
        <div key={piece.id} className="piece-tray__item" draggable onDragStart={(e) => handleDragStart(e, piece.id)}>
          <strong>{piece.piece_code}</strong>
          <span>{piece.piece_name}</span>
        </div>
      ))}
    </div>
  )
}
