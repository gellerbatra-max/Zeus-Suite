import { useEffect, useRef, useState } from 'react'
import { IdentityBar } from './components/IdentityBar'
import { PieceTray } from './components/PieceTray'
import { MarkerCanvas } from './components/MarkerCanvas'
import type { CanvasPlacement } from './components/MarkerCanvas'
import { computeBoundingBox, overlapAmount } from './geometry'
import { NestingJobPanel } from './components/NestingJobPanel'
import { MatchingPanel } from './components/MatchingPanel'
import { FuseBlockPanel } from './components/FuseBlockPanel'
import { MaterialPanel } from './components/MaterialPanel'
import { TransformPanel } from './components/TransformPanel'
import { BundlePanel } from './components/BundlePanel'
import type { BundleGroupBox } from './components/MarkerCanvas'
import { SplicePanel } from './components/SplicePanel'
import { LayrulePanel } from './components/LayrulePanel'
import { MarkerPicker } from './components/MarkerPicker'
import { pushRecentMarker } from './recentMarkers'
import { api, ApiError } from './api/client'
import type {
  BlockBufferRuleTableOut, FuseBlockOut, MarkerSibling, MatchGuidanceOut, SpliceMarkOut, WeaveLine, WorkspaceOut,
} from './api/types'

// The length axis (X) has no stored dimension -- a marker's length is however long its placed
// pieces need, so this boundary stays a fixed visual reference. The fabric-width axis (Y) *is*
// wired to the marker's real fabric_width (Sec 1.9's "Change Width of Marker"), falling back to
// this default only when the marker has none set yet.
const MARKER_WIDTH = 700
const DEFAULT_MARKER_HEIGHT = 450

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
    weaveLineOverride:
      data.weave_line_angle_deg != null && data.weave_line_offset != null
        ? { angleDeg: data.weave_line_angle_deg, offset: data.weave_line_offset }
        : null,
    stripeIndependentInSet: data.stripe_independent_in_set ?? false,
    blockBufferRuleNo: data.block_buffer_rule_no ?? null,
    bundleId: data.bundle_id ?? null,
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
  const [weaveLine, setWeaveLine] = useState<WeaveLine | null>(null)
  const [materialPattern, setMaterialPattern] = useState<{ visible: boolean; downloadUrl: string } | null>(null)
  const [fuseBlocks, setFuseBlocks] = useState<FuseBlockOut[]>([])
  const [blockBufferRuleTables, setBlockBufferRuleTables] = useState<BlockBufferRuleTableOut[]>([])
  const [targetLength, setTargetLength] = useState<number | null>(null)
  const [fabricWidth, setFabricWidth] = useState<number | null>(null)
  const [spliceMarks, setSpliceMarks] = useState<SpliceMarkOut[]>([])
  const [siblings, setSiblings] = useState<MarkerSibling[]>([])
  const lastGuidanceAt = useRef(0)

  // Undo/Redo (Sec 1.11: "Standard multi-level undo/redo on the marker canvas"). Scoped to
  // `placements` -- the actual canvas edit history -- not every side panel's own server-persisted
  // settings (matching rule tables, splice settings, etc. all have their own save/cancel already).
  // The stacks themselves live in refs (pushing a snapshot shouldn't itself trigger a render), but
  // their *lengths* are mirrored into real state so the Undo/Redo buttons' `disabled` prop reads
  // React state during render rather than a ref (refs aren't safe to read during render).
  const undoStackRef = useRef<CanvasPlacement[][]>([])
  const redoStackRef = useRef<CanvasPlacement[][]>([])
  const [undoCount, setUndoCount] = useState(0)
  const [redoCount, setRedoCount] = useState(0)

  // The ref mutation happens synchronously here in the event handler (reading `placements` from
  // the component's own closure, which is current between renders) rather than inside a
  // setPlacements updater callback -- React doesn't guarantee an updater runs synchronously (and
  // may double-invoke it under StrictMode), so mutating a ref from inside one is unsafe.
  const updatePlacements = (updater: (prev: CanvasPlacement[]) => CanvasPlacement[]) => {
    undoStackRef.current = [...undoStackRef.current, placements]
    redoStackRef.current = []
    setPlacements(updater)
    setUndoCount(undoStackRef.current.length)
    setRedoCount(0)
  }

  const clearHistory = () => {
    undoStackRef.current = []
    redoStackRef.current = []
    setUndoCount(0)
    setRedoCount(0)
  }

  const undo = () => {
    if (undoStackRef.current.length === 0) return
    const previous = undoStackRef.current[undoStackRef.current.length - 1]
    undoStackRef.current = undoStackRef.current.slice(0, -1)
    redoStackRef.current = [...redoStackRef.current, placements]
    setPlacements(previous)
    setUndoCount(undoStackRef.current.length)
    setRedoCount(redoStackRef.current.length)
  }

  const redo = () => {
    if (redoStackRef.current.length === 0) return
    const next = redoStackRef.current[redoStackRef.current.length - 1]
    redoStackRef.current = redoStackRef.current.slice(0, -1)
    undoStackRef.current = [...undoStackRef.current, placements]
    setPlacements(next)
    setUndoCount(undoStackRef.current.length)
    setRedoCount(redoStackRef.current.length)
  }

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null
      // Don't hijack the browser's own text-field undo/redo while typing in a panel input.
      if (target && ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) return
      if (!(e.ctrlKey || e.metaKey) || e.key.toLowerCase() !== 'z') return
      e.preventDefault()
      if (e.shiftKey) redo()
      else undo()
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [undo, redo])

  const openMarker = async (idOverride?: string) => {
    const markerId = (idOverride ?? markerIdInput).trim()
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
      setWeaveLine(null)
      setMaterialPattern(null)
      setFuseBlocks([])
      setBlockBufferRuleTables([])
      setTargetLength(null)
      setFabricWidth(ws.fabric_width)
      setSpliceMarks([])
      setMarkerIdInput(markerId)
      clearHistory()
      pushRecentMarker({ id: ws.marker_id, markerCode: ws.marker_code })
      api
        .get<MarkerSibling[]>(`/markers/${markerId}/siblings`)
        .then(setSiblings)
        .catch(() => setSiblings([]))
    } catch (err) {
      setWorkspace(null)
      setError(err instanceof ApiError ? err.message : String(err))
    }
  }

  // Open Next/Previous/Next Unmade/Next Made (Sec 1.11): steps through `siblings` -- every marker
  // in the current marker's folder, sorted alphanumerically by marker_code (the "current storage
  // area" the plan describes) -- optionally filtered to the first entry matching a given status.
  const stepMarker = (direction: 'next' | 'prev', statusFilter?: string) => {
    if (!workspace) return
    const idx = siblings.findIndex((s) => s.id === workspace.marker_id)
    if (idx === -1) return
    const range = direction === 'next' ? siblings.slice(idx + 1) : siblings.slice(0, idx).reverse()
    const match = statusFilter ? range.find((s) => s.workflow_status === statusFilter) : range[0]
    if (!match) {
      setError(
        `No ${direction === 'next' ? 'next' : 'previous'}${statusFilter ? ` ${statusFilter}` : ''} marker in this folder.`,
      )
      return
    }
    openMarker(match.id)
  }

  const unplacedPieces = workspace
    ? workspace.available_pieces.filter((piece) => !placements.some((p) => p.pieceId === piece.id))
    : []

  const selectedCutterStripeNeeded = placements.find((p) => p.pieceId === selectedPieceId)?.cutterStripeNeeded ?? true
  const selectedStripeIndependentInSet =
    placements.find((p) => p.pieceId === selectedPieceId)?.stripeIndependentInSet ?? false
  const selectedBlockBufferRuleNo = placements.find((p) => p.pieceId === selectedPieceId)?.blockBufferRuleNo ?? null

  const blockBufferRuleTypes: Record<number, string> = Object.fromEntries(
    blockBufferRuleTables.map((r) => [r.rule_no, r.rule_type]),
  )

  const selectedPieceCenter = (() => {
    const selected = placements.find((p) => p.pieceId === selectedPieceId)
    return selected ? { x: selected.x + selected.width / 2, y: selected.y + selected.height / 2 } : null
  })()

  const selectedOverlaps = (() => {
    const selected = placements.find((p) => p.pieceId === selectedPieceId)
    if (!selected) return []
    return placements
      .filter((p) => p.pieceId !== selected.pieceId)
      .map((other) => ({ other, amount: overlapAmount(selected, other) }))
      .filter((o): o is { other: CanvasPlacement; amount: { x: number; y: number } } => o.amount !== null)
  })()

  const handlePlace = (pieceId: string, x: number, y: number) => {
    if (!workspace) return
    const piece = workspace.available_pieces.find((p) => p.id === pieceId)
    if (!piece) return
    updatePlacements((prev) => [
      ...prev,
      {
        pieceId, pieceCode: piece.piece_code, x, y, rotationDeg: 0, flipX: false, flipY: false,
        width: piece.width, height: piece.height, sizeCode: 'M', quantity: 1, stripeMarkId: null,
        cutterStripeNeeded: true, weaveLineOverride: null, stripeIndependentInSet: false,
        blockBufferRuleNo: null, bundleId: null,
      },
    ])
    setSelectedPieceId(pieceId)
  }

  const handleMove = (pieceId: string, x: number, y: number) => {
    updatePlacements((prev) => prev.map((p) => (p.pieceId === pieceId ? { ...p, x, y } : p)))
    setGuidance(null)
  }

  const handleAssignMark = (pieceId: string, markId: string | null) => {
    updatePlacements((prev) => {
      const target = prev.find((p) => p.pieceId === pieceId)
      if (!target) return prev
      // Stripe-only-in-a-set (Sec 1.4): by default, assigning a mark to a piece syncs the same
      // mark across every other placed piece of the same garment size (a "set" sharing that
      // size) -- the doc's default before the toggle exists. A piece flagged
      // stripeIndependentInSet opts out: it neither pushes its own assignment onto its size
      // group, nor gets overwritten when another piece in that group is assigned.
      if (target.stripeIndependentInSet) {
        return prev.map((p) => (p.pieceId === pieceId ? { ...p, stripeMarkId: markId } : p))
      }
      return prev.map((p) =>
        p.pieceId === pieceId || (p.sizeCode === target.sizeCode && !p.stripeIndependentInSet)
          ? { ...p, stripeMarkId: markId }
          : p,
      )
    })
  }

  const handleSetWeaveLineOverride = (pieceId: string, override: { angleDeg: number; offset: number } | null) => {
    updatePlacements((prev) => prev.map((p) => (p.pieceId === pieceId ? { ...p, weaveLineOverride: override } : p)))
  }

  const handleAssignBlockBufferRule = (pieceId: string, ruleNo: number | null) => {
    updatePlacements((prev) => prev.map((p) => (p.pieceId === pieceId ? { ...p, blockBufferRuleNo: ruleNo } : p)))
  }

  // Bundle management (Sec 1.3): a bundle groups several placed pieces (one garment, one size)
  // by a shared bundleId riding inside placement_data, exactly like stripe_mark_id/
  // blockBufferRuleNo -- no platform schema change, no server round trip, persisted on the next
  // Save. There's no canvas multi-select, so grouping uses the same sequential "draft" workflow
  // BundlePanel already established for fuse-blocking.
  const nextBundleId = () => {
    const existing = new Set(placements.map((p) => p.bundleId).filter((id): id is string => id !== null))
    let n = existing.size + 1
    while (existing.has(`bundle-${n}`)) n++
    return `bundle-${n}`
  }

  const handleCreateBundle = (pieceIds: string[]) => {
    const bundleId = nextBundleId()
    updatePlacements((prev) => prev.map((p) => (pieceIds.includes(p.pieceId) ? { ...p, bundleId } : p)))
  }

  const handleUnplaceBundle = (bundleId: string) => {
    updatePlacements((prev) => prev.filter((p) => p.bundleId !== bundleId))
    setSelectedPieceId((prev) => (placements.find((p) => p.pieceId === prev)?.bundleId === bundleId ? null : prev))
  }

  // Bundle/Flip (Sec 1.3): same mirror-within-bounding-box math as the whole-marker flip above,
  // scoped to just this bundle's own members and their own bbox instead of the whole marker's.
  const handleFlipBundle = (bundleId: string, axis: 'x' | 'y' | 'xy') => {
    const members = placements.filter((p) => p.bundleId === bundleId)
    const bbox = computeBoundingBox(members)
    if (!bbox) return
    updatePlacements((prev) =>
      prev.map((p) => {
        if (p.bundleId !== bundleId) return p
        let { x, y, flipX, flipY } = p
        if (axis === 'x' || axis === 'xy') {
          x = bbox.minX + bbox.maxX - p.x - p.width
          flipX = !p.flipX
        }
        if (axis === 'y' || axis === 'xy') {
          y = bbox.minY + bbox.maxY - p.y - p.height
          flipY = !p.flipY
        }
        return { ...p, x, y, flipX, flipY }
      }),
    )
  }

  const handleResetBundleOrientation = (bundleId: string) => {
    updatePlacements((prev) =>
      prev.map((p) => (p.bundleId === bundleId ? { ...p, rotationDeg: 0, flipX: false, flipY: false } : p)),
    )
  }

  const handleSetBundleQuantity = (bundleId: string, quantity: number) => {
    updatePlacements((prev) => prev.map((p) => (p.bundleId === bundleId ? { ...p, quantity } : p)))
  }

  const bundleGroups: BundleGroupBox[] = (() => {
    const byId = new Map<string, CanvasPlacement[]>()
    for (const p of placements) {
      if (!p.bundleId) continue
      const list = byId.get(p.bundleId)
      if (list) list.push(p)
      else byId.set(p.bundleId, [p])
    }
    return Array.from(byId.entries()).flatMap(([bundleId, members], i) => {
      const bbox = computeBoundingBox(members)
      if (!bbox) return []
      return [{
        bundleId, label: `Bundle ${i + 1} (${members[0].sizeCode})`,
        x: bbox.minX, y: bbox.minY, width: bbox.maxX - bbox.minX, height: bbox.maxY - bbox.minY,
      }]
    })
  })()

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
    updatePlacements((prev) => prev.map((p) => (p.pieceId === selectedPieceId ? fn(p) : p)))
  }

  const unplaceSelected = () => {
    if (!selectedPieceId) return
    updatePlacements((prev) => prev.filter((p) => p.pieceId !== selectedPieceId))
    setSelectedPieceId(null)
  }

  // Whole-marker Flip X/Y/XY (Sec 1.9): mirrors every placed piece's position within the tight
  // bounding box of everything currently placed (see geometry.ts's computeBoundingBox) and
  // toggles each piece's own flip flag -- a pure local-state edit persisted on the next Save,
  // exactly like single-piece rotate/flip above.
  const flipMarker = (axis: 'x' | 'y' | 'xy') => {
    const bbox = computeBoundingBox(placements)
    if (!bbox) return
    updatePlacements((prev) =>
      prev.map((p) => {
        let { x, y, flipX, flipY } = p
        if (axis === 'x' || axis === 'xy') {
          x = bbox.minX + bbox.maxX - p.x - p.width
          flipX = !p.flipX
        }
        if (axis === 'y' || axis === 'xy') {
          y = bbox.minY + bbox.maxY - p.y - p.height
          flipY = !p.flipY
        }
        return { ...p, x, y, flipX, flipY }
      }),
    )
  }

  // Shrink and Stretch's "Apply to Placements" (Sec 1.9) already persisted the scaled geometry on
  // the platform (marker-making-service's apply-shrink-stretch endpoint) -- this just re-derives
  // each existing placement's geometry from the returned workspace, without touching selection,
  // matching, fuse-block, or any other panel's state.
  const applyWorkspaceGeometry = (ws: WorkspaceOut) => {
    setWorkspace(ws)
    updatePlacements((prev) => prev.map((p) => toCanvasPlacement(ws, p.pieceId) ?? p))
  }

  // Applying a layrule (Sec 1.5) can place pieces that had no prior local placement at all (the
  // whole point of reusing a captured layout on a marker that starts empty) -- unlike shrink/
  // stretch above, this must rebuild the full placements list from the returned workspace rather
  // than only mapping over what was already there, or newly-applied pieces would be silently
  // dropped.
  const applyLayruleWorkspace = (ws: WorkspaceOut) => {
    setWorkspace(ws)
    updatePlacements(() =>
      ws.placements.map((p) => toCanvasPlacement(ws, p.piece_id)).filter((p): p is CanvasPlacement => p !== null),
    )
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
            weave_line_angle_deg: p.weaveLineOverride?.angleDeg ?? null,
            weave_line_offset: p.weaveLineOverride?.offset ?? null,
            stripe_independent_in_set: p.stripeIndependentInSet,
            block_buffer_rule_no: p.blockBufferRuleNo,
            bundle_id: p.bundleId,
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
        <button onClick={() => openMarker()}>Open Marker</button>
        <MarkerPicker onOpenMarker={(id) => openMarker(id)} />
        {workspace && (
          <>
            <span className="badge">{workspace.marker_code}</span>
            <span className={`badge badge--${workspace.workflow_status}`}>{workspace.workflow_status}</span>
            <button onClick={save} disabled={saving}>
              {saving ? 'Saving…' : 'Save'}
            </button>
            <button onClick={undo} disabled={undoCount === 0}>
              Undo (Ctrl+Z)
            </button>
            <button onClick={redo} disabled={redoCount === 0}>
              Redo (Ctrl+⇧Z)
            </button>
            <span className="hint">Open:</span>
            <button onClick={() => stepMarker('prev')} disabled={siblings.length === 0}>
              ◀ Prev
            </button>
            <button onClick={() => stepMarker('next')} disabled={siblings.length === 0}>
              Next ▶
            </button>
            <button onClick={() => stepMarker('next', 'unmade')} disabled={siblings.length === 0}>
              Next Unmade ▶
            </button>
            <button onClick={() => stepMarker('next', 'made')} disabled={siblings.length === 0}>
              Next Made ▶
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
              markerHeight={fabricWidth ?? DEFAULT_MARKER_HEIGHT}
              placements={placements}
              onPlace={handlePlace}
              onMove={handleMove}
              onDragMove={handleDragMove}
              onSelect={setSelectedPieceId}
              selectedPieceId={selectedPieceId}
              guidance={guidance}
              weaveLine={weaveLine}
              materialPatternUrl={materialPattern?.visible ? materialPattern.downloadUrl : null}
              fuseBlocks={fuseBlocks}
              blockBufferRuleTypes={blockBufferRuleTypes}
              targetLength={targetLength}
              bundleGroups={bundleGroups}
              spliceMarks={spliceMarks}
            />
            {guidance?.result.message && <p className="matching-warning">{guidance.result.message}</p>}
            {selectedOverlaps.length > 0 && (
              <ul className="overlap-readout">
                {selectedOverlaps.map(({ other, amount }) => (
                  <li key={other.pieceId}>
                    Overlaps {other.pieceCode} by {Math.max(amount.x, amount.y).toFixed(1)}{' '}
                    ({amount.x >= amount.y ? 'x' : 'y'}-axis)
                  </li>
                ))}
              </ul>
            )}
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
              <button
                disabled={!selectedPieceId}
                onClick={() => updateSelected((p) => ({ ...p, stripeIndependentInSet: !p.stripeIndependentInSet }))}
              >
                Stripe Set: {selectedStripeIndependentInSet ? 'Independent' : 'Linked'}
              </button>
            </div>
            <div className="marker-toolbar">
              <span className="hint">Flip whole marker:</span>
              <button disabled={placements.length === 0} onClick={() => flipMarker('x')}>
                Flip X
              </button>
              <button disabled={placements.length === 0} onClick={() => flipMarker('y')}>
                Flip Y
              </button>
              <button disabled={placements.length === 0} onClick={() => flipMarker('xy')}>
                Flip XY
              </button>
            </div>
          </div>

          <MatchingPanel
            markerId={workspace.marker_id}
            matchingMethod={matchingMethod}
            matchingRuleTableId={matchingRuleTableId}
            selectedPieceId={selectedPieceId}
            selectedPieceStripeMarkId={placements.find((p) => p.pieceId === selectedPieceId)?.stripeMarkId ?? null}
            selectedPieceCenter={selectedPieceCenter}
            selectedPieceWeaveLineOverride={
              placements.find((p) => p.pieceId === selectedPieceId)?.weaveLineOverride ?? null
            }
            onMatchingApplied={(method, ruleTableId) => {
              setMatchingMethod(method)
              setMatchingRuleTableId(ruleTableId)
            }}
            onAssignMark={handleAssignMark}
            onWeaveLineChanged={setWeaveLine}
            onSetWeaveLineOverride={handleSetWeaveLineOverride}
            onMaterialPatternChanged={setMaterialPattern}
          />

          <FuseBlockPanel
            markerId={workspace.marker_id}
            placements={placements}
            selectedPieceId={selectedPieceId}
            selectedPieceBlockBufferRuleNo={selectedBlockBufferRuleNo}
            onAssignBlockBufferRule={handleAssignBlockBufferRule}
            onFuseBlocksChanged={setFuseBlocks}
            onRuleTablesChanged={setBlockBufferRuleTables}
          />

          <MaterialPanel
            markerId={workspace.marker_id}
            hasOrder={workspace.order_id != null}
            onTargetLengthChanged={setTargetLength}
          />

          <TransformPanel
            markerId={workspace.marker_id}
            hasOrder={workspace.order_id != null}
            onFabricWidthChanged={setFabricWidth}
            onWorkspaceApplied={applyWorkspaceGeometry}
          />

          <BundlePanel
            placements={placements}
            selectedPieceId={selectedPieceId}
            onSelectPiece={setSelectedPieceId}
            onCreateBundle={handleCreateBundle}
            onUnplaceBundle={handleUnplaceBundle}
            onFlipBundle={handleFlipBundle}
            onResetBundleOrientation={handleResetBundleOrientation}
            onSetBundleQuantity={handleSetBundleQuantity}
          />

          <SplicePanel markerId={workspace.marker_id} onSpliceMarksChanged={setSpliceMarks} />

          <LayrulePanel markerId={workspace.marker_id} onApplied={applyLayruleWorkspace} />

          <NestingJobPanel markerId={workspace.marker_id} orderId={workspace.order_id} />
        </div>
      )}
    </div>
  )
}
