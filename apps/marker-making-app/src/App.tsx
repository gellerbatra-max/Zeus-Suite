import { useRef, useState } from 'react'
import { IdentityBar } from './components/IdentityBar'
import { PieceTray } from './components/PieceTray'
import { MarkerCanvas } from './components/MarkerCanvas'
import type { CanvasPlacement } from './components/MarkerCanvas'
import { NestingJobPanel } from './components/NestingJobPanel'
import { MatchingPanel } from './components/MatchingPanel'
import { api, ApiError } from './api/client'
import type { MatchGuidanceOut, WorkspaceOut } from './api/types'

// The platform's marker.fabric_width isn't wired into the workspace payload for this slice --
// the boundary here is a fixed visual reference, not tied to a real fabric width yet.
const MARKER_WIDTH = 700
const MARKER_HEIGHT = 450

function toCanvasPlacement(workspace: WorkspaceOut, pieceId: string): CanvasPlacement | null {
  const piece = workspace.available_pieces.find((p) => p.id === pieceId)
  if (!piece) return null
  const placement = workspace.placements.find((p) => p.piece_id === pieceId)
  const data = placement?.placement_data ?? {}
  return {
    pieceId,
    pieceCode: piece.piece_code,
    x: data.x ?? 20,
    y: data.y ?? 20,
    rotationDeg: data.rotation_deg ?? 0,
    flipX: data.flip_x ?? false,
    flipY: data.flip_y ?? false,
    width: data.width ?? piece.width,
    height: data.height ?? piece.height,
    sizeCode: placement?.size_code ?? 'M',
    quantity: placement?.quantity ?? 1,
    stripeMarkId: data.stripe_mark_id ?? null,
    cutterStripeNeeded: data.cutter_stripe_needed ?? true,
  }
}

const GUIDANCE_THROTTLE_MS = 150

export default function App() {
  const [markerIdInput, setMarkerIdInput] = useState('')
  const [workspace, setWorkspace] = useState<WorkspaceOut | null>(null)
  const [placements, setPlacements] = useState<CanvasPlacement[]>([])
  const [selectedPieceId, setSelectedPieceId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [matchingMethod, setMatchingMethod] = useState<string | null>(null)
  const [matchingRuleTableId, setMatchingRuleTableId] = useState<string | null>(null)
  const [guidance, setGuidance] = useState<{ pieceId: string; result: MatchGuidanceOut } | null>(null)
  const lastGuidanceAt = useRef(0)

  const openMarker = async () => {
    const markerId = markerIdInput.trim()
    if (!markerId) return
    setError(null)
    try {
      const ws = await api.get<WorkspaceOut>(`/markers/${markerId}/workspace`)
      setWorkspace(ws)
      setPlacements(
        ws.placements.map((p) => toCanvasPlacement(ws, p.piece_id)).filter((p): p is CanvasPlacement => p !== null),
      )
      setSelectedPieceId(null)
      setMatchingMethod(ws.matching_method)
      setMatchingRuleTableId(ws.matching_rule_table_id)
      setGuidance(null)
    } catch (err) {
      setWorkspace(null)
      setError(err instanceof ApiError ? err.message : String(err))
    }
  }

  const unplacedPieces = workspace
    ? workspace.available_pieces.filter((piece) => !placements.some((p) => p.pieceId === piece.id))
    : []

  const selectedCutterStripeNeeded = placements.find((p) => p.pieceId === selectedPieceId)?.cutterStripeNeeded ?? true

  const handlePlace = (pieceId: string, x: number, y: number) => {
    if (!workspace) return
    const piece = workspace.available_pieces.find((p) => p.id === pieceId)
    if (!piece) return
    setPlacements((prev) => [
      ...prev,
      {
        pieceId, pieceCode: piece.piece_code, x, y, rotationDeg: 0, flipX: false, flipY: false,
        width: piece.width, height: piece.height, sizeCode: 'M', quantity: 1, stripeMarkId: null,
        cutterStripeNeeded: true,
      },
    ])
    setSelectedPieceId(pieceId)
  }

  const handleMove = (pieceId: string, x: number, y: number) => {
    setPlacements((prev) => prev.map((p) => (p.pieceId === pieceId ? { ...p, x, y } : p)))
    setGuidance(null)
  }

  const handleAssignMark = (pieceId: string, markId: string | null) => {
    setPlacements((prev) => prev.map((p) => (p.pieceId === pieceId ? { ...p, stripeMarkId: markId } : p)))
  }

  const handleDragMove = (pieceId: string, x: number, y: number) => {
    const piece = placements.find((p) => p.pieceId === pieceId)
    if (!piece?.stripeMarkId || !workspace) return
    const now = Date.now()
    if (now - lastGuidanceAt.current < GUIDANCE_THROTTLE_MS) return
    lastGuidanceAt.current = now
    api
      .post<MatchGuidanceOut>(`/markers/${workspace.marker_id}/matching/guidance`, {
        piece_id: pieceId, stripe_mark_id: piece.stripeMarkId, x, y,
      })
      .then((result) => setGuidance({ pieceId, result }))
      .catch(() => setGuidance(null))
  }

  const updateSelected = (fn: (p: CanvasPlacement) => CanvasPlacement) => {
    if (!selectedPieceId) return
    setPlacements((prev) => prev.map((p) => (p.pieceId === selectedPieceId ? fn(p) : p)))
  }

  const unplaceSelected = () => {
    if (!selectedPieceId) return
    setPlacements((prev) => prev.filter((p) => p.pieceId !== selectedPieceId))
    setSelectedPieceId(null)
  }

  const save = async () => {
    if (!workspace) return
    setSaving(true)
    setError(null)
    try {
      const updated = await api.put<WorkspaceOut>(`/markers/${workspace.marker_id}/workspace`, {
        placements: placements.map((p) => ({
          piece_id: p.pieceId,
          size_code: p.sizeCode,
          quantity: p.quantity,
          placement_data: {
            x: p.x, y: p.y, rotation_deg: p.rotationDeg, flip_x: p.flipX, flip_y: p.flipY,
            width: p.width, height: p.height, stripe_mark_id: p.stripeMarkId,
            cutter_stripe_needed: p.cutterStripeNeeded,
          },
        })),
      })
      setWorkspace(updated)
      setMatchingMethod(updated.matching_method)
      setMatchingRuleTableId(updated.matching_rule_table_id)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="app">
      <header className="app__header">
        <h1>Zeus Suite — Marker Making</h1>
        <IdentityBar />
      </header>

      <div className="app__toolbar">
        <input
          placeholder="Marker ID (uuid)"
          value={markerIdInput}
          onChange={(e) => setMarkerIdInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && openMarker()}
        />
        <button onClick={openMarker}>Open Marker</button>
        {workspace && (
          <>
            <span className="badge">{workspace.marker_code}</span>
            <span className={`badge badge--${workspace.workflow_status}`}>{workspace.workflow_status}</span>
            <button onClick={save} disabled={saving}>
              {saving ? 'Saving…' : 'Save'}
            </button>
          </>
        )}
      </div>

      {error && <p className="error-text">{error}</p>}

      {workspace && (
        <div className="app__main">
          <PieceTray pieces={unplacedPieces} />

          <div className="app__canvas-column">
            <MarkerCanvas
              markerWidth={MARKER_WIDTH}
              markerHeight={MARKER_HEIGHT}
              placements={placements}
              onPlace={handlePlace}
              onMove={handleMove}
              onDragMove={handleDragMove}
              onSelect={setSelectedPieceId}
              selectedPieceId={selectedPieceId}
              guidance={guidance}
            />
            {guidance?.result.message && <p className="matching-warning">{guidance.result.message}</p>}
            <div className="piece-toolbar">
              <button disabled={!selectedPieceId} onClick={() => updateSelected((p) => ({ ...p, rotationDeg: (p.rotationDeg + 90) % 360 }))}>
                Rotate 90°
              </button>
              <button disabled={!selectedPieceId} onClick={() => updateSelected((p) => ({ ...p, flipX: !p.flipX }))}>
                Flip H
              </button>
              <button disabled={!selectedPieceId} onClick={() => updateSelected((p) => ({ ...p, flipY: !p.flipY }))}>
                Flip V
              </button>
              <button disabled={!selectedPieceId} onClick={unplaceSelected}>
                Unplace
              </button>
              <button
                disabled={!selectedPieceId}
                onClick={() => updateSelected((p) => ({ ...p, cutterStripeNeeded: !p.cutterStripeNeeded }))}
              >
                Cutter Stripe: {selectedCutterStripeNeeded ? 'Needed' : 'Not Needed'}
              </button>
            </div>
          </div>

          <MatchingPanel
            markerId={workspace.marker_id}
            matchingMethod={matchingMethod}
            matchingRuleTableId={matchingRuleTableId}
            selectedPieceId={selectedPieceId}
            selectedPieceStripeMarkId={placements.find((p) => p.pieceId === selectedPieceId)?.stripeMarkId ?? null}
            onMatchingApplied={(method, ruleTableId) => {
              setMatchingMethod(method)
              setMatchingRuleTableId(ruleTableId)
            }}
            onAssignMark={handleAssignMark}
          />

          <NestingJobPanel markerId={workspace.marker_id} orderId={workspace.order_id} />
        </div>
      )}
    </div>
  )
}
