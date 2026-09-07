import { useState } from 'react'
import type { PieceOut } from '../api/types'

interface Props {
  pieces: PieceOut[]
  selectedPieceId: string | null
  onSelect: (piece: PieceOut) => void
  onCreate: (pieceCode: string, pieceName: string) => void
  creating: boolean
}

export function PieceList({ pieces, selectedPieceId, onSelect, onCreate, creating }: Props) {
  const [pieceCode, setPieceCode] = useState('')
  const [pieceName, setPieceName] = useState('')

  const submit = () => {
    if (!pieceCode.trim() || !pieceName.trim()) return
    onCreate(pieceCode.trim(), pieceName.trim())
    setPieceCode('')
    setPieceName('')
  }

  return (
    <div className="piece-list">
      <h3>Pieces</h3>
      <ul className="piece-list__items">
        {pieces.map((piece) => (
          <li key={piece.id}>
            <button
              className={`piece-list__item${piece.id === selectedPieceId ? ' piece-list__item--selected' : ''}`}
              onClick={() => onSelect(piece)}
            >
              <strong>{piece.piece_code}</strong>
              <span>{piece.piece_name}</span>
              <span className={`badge badge--${piece.workflow_status.code}`}>{piece.workflow_status.label}</span>
            </button>
          </li>
        ))}
        {pieces.length === 0 && <li className="hint">No pieces yet -- create one below.</li>}
      </ul>

      <div className="piece-list__new">
        <input placeholder="Piece code" value={pieceCode} onChange={(e) => setPieceCode(e.target.value)} />
        <input placeholder="Piece name" value={pieceName} onChange={(e) => setPieceName(e.target.value)} />
        <button onClick={submit} disabled={creating}>
          {creating ? 'Creating…' : 'New Piece'}
        </button>
      </div>
    </div>
  )
}
