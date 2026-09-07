import { useState } from 'react'
import type { CanvasPlacement } from './MarkerCanvas'

interface Bundle {
  bundleId: string
  sizeCode: string
  memberIds: string[]
  memberCodes: string[]
}

interface Props {
  placements: CanvasPlacement[]
  selectedPieceId: string | null
  onSelectPiece: (pieceId: string) => void
  onCreateBundle: (pieceIds: string[]) => void
  onUnplaceBundle: (bundleId: string) => void
  onFlipBundle: (bundleId: string, axis: 'x' | 'y' | 'xy') => void
  onResetBundleOrientation: (bundleId: string) => void
  onSetBundleQuantity: (bundleId: string, quantity: number) => void
}

// Bundle count cap (Sec 1.3: "hard cap of 500 bundles / 5,000 pieces per marker, configurable
// ceiling"). This app has no per-marker config for that ceiling, so it's a fixed client-side
// warning rather than a real configurable/server-enforced limit.
const BUNDLE_CAP = 500

export function BundlePanel({
  placements,
  selectedPieceId,
  onSelectPiece,
  onCreateBundle,
  onUnplaceBundle,
  onFlipBundle,
  onResetBundleOrientation,
  onSetBundleQuantity,
}: Props) {
  const [draftPieceIds, setDraftPieceIds] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)
  const [quantityInputs, setQuantityInputs] = useState<Record<string, string>>({})

  const bundles: Bundle[] = (() => {
    const byId = new Map<string, Bundle>()
    for (const p of placements) {
      if (!p.bundleId) continue
      const existing = byId.get(p.bundleId)
      if (existing) {
        existing.memberIds.push(p.pieceId)
        existing.memberCodes.push(p.pieceCode)
      } else {
        byId.set(p.bundleId, { bundleId: p.bundleId, sizeCode: p.sizeCode, memberIds: [p.pieceId], memberCodes: [p.pieceCode] })
      }
    }
    return Array.from(byId.values())
  })()

  const selectedPiece = placements.find((p) => p.pieceId === selectedPieceId)
  const pieceCode = (pieceId: string) => placements.find((p) => p.pieceId === pieceId)?.pieceCode ?? pieceId

  const addSelectedToDraft = () => {
    setError(null)
    if (!selectedPieceId || draftPieceIds.includes(selectedPieceId)) return
    if (selectedPiece?.bundleId) {
      setError('That piece is already in a bundle -- unplace its bundle first to move it.')
      return
    }
    setDraftPieceIds((prev) => [...prev, selectedPieceId])
  }

  const removeFromDraft = (pieceId: string) => {
    setDraftPieceIds((prev) => prev.filter((id) => id !== pieceId))
  }

  const createBundle = () => {
    setError(null)
    if (draftPieceIds.length === 0) return
    if (bundles.length >= BUNDLE_CAP) {
      setError(`Bundle cap reached (${BUNDLE_CAP} per marker).`)
      return
    }
    const sizeCodes = new Set(draftPieceIds.map((id) => placements.find((p) => p.pieceId === id)?.sizeCode))
    if (sizeCodes.size > 1) {
      setError('A bundle is one garment, one size -- all draft pieces must share the same size code.')
      return
    }
    onCreateBundle(draftPieceIds)
    setDraftPieceIds([])
  }

  const setQuantity = (bundleId: string) => {
    const value = quantityInputs[bundleId]
    if (value === undefined || value === '') return
    onSetBundleQuantity(bundleId, Number(value))
  }

  return (
    <div className="bundle-panel">
      <h3>Bundle Management</h3>
      {error && <p className="error-text">{error}</p>}

      <section className="bundle-panel__section">
        <label>Bundle draft</label>
        <ul className="bundle-panel__list">
          {draftPieceIds.map((id) => (
            <li key={id}>
              <span>{pieceCode(id)}</span>
              <button onClick={() => removeFromDraft(id)}>Remove</button>
            </li>
          ))}
        </ul>
        <div className="bundle-panel__inline-form">
          <button disabled={!selectedPieceId || draftPieceIds.includes(selectedPieceId)} onClick={addSelectedToDraft}>
            Add Selected Piece
          </button>
        </div>
        <button disabled={draftPieceIds.length === 0} onClick={createBundle}>
          Create Bundle
        </button>
      </section>

      <section className="bundle-panel__section">
        <label>Bundles ({bundles.length})</label>
        <ul className="bundle-panel__list bundle-panel__list--stacked">
          {bundles.map((bundle, i) => (
            <li key={bundle.bundleId} className="bundle-panel__bundle-item">
              <span>
                Bundle {i + 1} ({bundle.sizeCode}) — {bundle.memberCodes.join(', ')}
              </span>
              <div className="bundle-panel__bundle-actions">
                <button onClick={() => onSelectPiece(bundle.memberIds[0])}>Select</button>
                <button onClick={() => onFlipBundle(bundle.bundleId, 'x')}>Flip X</button>
                <button onClick={() => onFlipBundle(bundle.bundleId, 'y')}>Flip Y</button>
                <button onClick={() => onFlipBundle(bundle.bundleId, 'xy')}>Flip XY</button>
                <button onClick={() => onResetBundleOrientation(bundle.bundleId)}>Reset Orientation</button>
                <button onClick={() => onUnplaceBundle(bundle.bundleId)}>Unplace / Return</button>
              </div>
              <div className="bundle-panel__inline-form">
                <input
                  placeholder="Quantity"
                  value={quantityInputs[bundle.bundleId] ?? ''}
                  onChange={(e) => setQuantityInputs((prev) => ({ ...prev, [bundle.bundleId]: e.target.value }))}
                />
                <button onClick={() => setQuantity(bundle.bundleId)}>Set Quantity</button>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
