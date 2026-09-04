import { useEffect, useRef, useState } from 'react'
import type Konva from 'konva'
import { IdentityBar } from './components/IdentityBar'
import { PieceList } from './components/PieceList'
import { PatternCanvas } from './components/PatternCanvas'
import type { Tool } from './components/PatternCanvas'
import { ShapeTools } from './components/ShapeTools'
import { GradingTools } from './components/GradingTools'
import { api, ApiError } from './api/client'
import type { FolderOut, FreePoint, InternalLine, PieceGeometryDocument, PieceOut, Point } from './api/types'
import {
  addAnnotationCommand,
  addDartCommand,
  addLineCommand,
  addMeasurementCommand,
  addNotchCommand,
  addPointCommand,
  deleteLineCommand,
  deletePointCommand,
  movePointCommand,
  removeAnnotationCommand,
  removeNotchCommand,
  replaceShapeCommand,
  setGradeRuleCommand,
  setGrainLineCommand,
  setSeamCommand,
  setSizeRangeCommand,
  transformDocumentCommand,
} from './commands'
import type { Command } from './commands'
import { circlePerimeter, rectanglePerimeter } from './shapes'
import { flipPieceHorizontal, flipPieceVertical, rotatePiece90 } from './transform'

const DEFAULT_FOLDER_NAME = 'Pattern Design Pieces'

const TOOL_LABELS: Record<Tool, string> = {
  draw: 'Draw',
  edit: 'Pan/Edit',
  'add-line': 'Add Line',
  'delete-line': 'Delete Line',
  seam: 'Seam',
  dart: 'Dart',
  notch: 'Notch',
  'grain-line': 'Grain Line',
  grade: 'Grade',
  annotate: 'Annotate',
  measure: 'Measure',
}

function emptyGeometry(): PieceGeometryDocument {
  return {
    schema_version: 1,
    units: 'mm',
    perimeter: [],
    internal_lines: [],
    seams: [],
    darts: [],
    notches: [],
    grain_line: null,
    grade_rule_table: null,
    annotations: [],
    measurements: [],
  }
}

async function ensureDefaultFolder(): Promise<FolderOut> {
  const existing = await api.get<FolderOut[]>('/folders')
  const found = existing.find((f) => f.name === DEFAULT_FOLDER_NAME)
  if (found) return found

  try {
    return await api.post<FolderOut>('/folders', { name: DEFAULT_FOLDER_NAME })
  } catch (err) {
    // Another tab/session may have created it in the window between the list and this create --
    // re-list rather than surfacing a spurious error for a folder that now genuinely exists.
    const retryExisting = await api.get<FolderOut[]>('/folders')
    const retryFound = retryExisting.find((f) => f.name === DEFAULT_FOLDER_NAME)
    if (retryFound) return retryFound
    throw err
  }
}

interface EditorState {
  geometry: PieceGeometryDocument
  undoStack: Command[]
  redoStack: Command[]
}

function initialEditorState(): EditorState {
  return { geometry: emptyGeometry(), undoStack: [], redoStack: [] }
}

export default function App() {
  const [folder, setFolder] = useState<FolderOut | null>(null)
  const [pieces, setPieces] = useState<PieceOut[]>([])
  const [selectedPiece, setSelectedPiece] = useState<PieceOut | null>(null)
  // Geometry + undo/redo stacks live in one state object updated via a single, side-effect-free
  // setEditor call per action -- React StrictMode invokes a setState updater function twice in
  // dev to catch exactly this class of bug, and an earlier version of this code nested
  // setGeometry/setRedoStack calls *inside* setUndoStack's updater, which doubled every undo.
  // One pure updater per action, computed from one previous-state snapshot, is safe to call twice.
  const [editor, setEditor] = useState<EditorState>(initialEditorState)
  const { geometry, undoStack, redoStack } = editor
  const [tool, setTool] = useState<Tool>('draw')
  // Seam allowance and dart intake need a numeric value from the operator after the canvas click
  // sequence completes. window.prompt() looked like the fast way to get one, but blocking native
  // dialogs are blind to the app's own state changes and get silently auto-dismissed by automated
  // browser tooling (returns null, same as a real Cancel) -- so these are inline toolbar inputs.
  const [pendingSeamEdge, setPendingSeamEdge] = useState<[string, string] | null>(null)
  const [seamValue, setSeamValue] = useState('10')
  const [pendingDart, setPendingDart] = useState<{ legA: FreePoint; apex: FreePoint; legB: FreePoint } | null>(null)
  const [dartValue, setDartValue] = useState('20')
  const [activeSizeStep, setActiveSizeStep] = useState<number | null>(null)
  const [showGradeNest, setShowGradeNest] = useState(false)
  const [pendingGradePoint, setPendingGradePoint] = useState<string | null>(null)
  const [gradeDeltaX, setGradeDeltaX] = useState('0')
  const [gradeDeltaY, setGradeDeltaY] = useState('0')
  const [pendingAnnotation, setPendingAnnotation] = useState<{ x: number; y: number } | null>(null)
  const [annotationText, setAnnotationText] = useState('')
  const [pendingMeasurement, setPendingMeasurement] = useState<[string, string] | null>(null)
  const [measurementLabel, setMeasurementLabel] = useState('')
  const [measurementTarget, setMeasurementTarget] = useState('')
  const [measurementTolerance, setMeasurementTolerance] = useState('2')
  // The trace-reference image (Sec 6.5's camera/scan digitizing path) is loaded via the browser's
  // File API and lives only in this component's memory -- never uploaded to the backend, never
  // part of the saved geometry document. See PatternCanvas.tsx's overlay-layer comment for why.
  const [referenceImage, setReferenceImage] = useState<HTMLImageElement | null>(null)
  const [referenceImageOpacity, setReferenceImageOpacity] = useState(0.5)
  const canvasStageRef = useRef<Konva.Stage | null>(null)
  const [creating, setCreating] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Phase 2.1 has no folder-browser UI of its own (that's the Data Management Platform's job) --
  // this app just needs *a* folder to create pieces into, so it resolves/creates one fixed
  // default folder at the root on load.
  const folderEnsureStarted = useRef(false)

  useEffect(() => {
    // Guards against React StrictMode's double effect-invocation in dev racing two
    // POST /folders calls for the same name -- data-platform-api doesn't turn that race into a
    // clean 409, it 500s (no unique-name conflict handling), so this has to not send it twice.
    // No cancellation flag: the ref already makes this run exactly once for the component's
    // lifetime, and StrictMode's synthetic cleanup-then-remount must not cancel the one real
    // in-flight request -- there'd be nothing left to pick it back up.
    if (folderEnsureStarted.current) return
    folderEnsureStarted.current = true

    ;(async () => {
      try {
        const resolved = await ensureDefaultFolder()
        setFolder(resolved)
        const folderPieces = await api.get<PieceOut[]>(`/pieces?folder_id=${resolved.id}`)
        setPieces(folderPieces)
      } catch (err) {
        setError(err instanceof ApiError ? err.message : String(err))
      }
    })()
  }, [])

  // Command stack (pattern_design_plan.md Sec 6.3): every edit is a do()/undo() pair, so undo/redo
  // and the eventual save-time diff (not built yet -- Phase 2.1 still saves the whole document)
  // both work off the same command list.
  const runCommand = (cmd: Command) => {
    setEditor((state) => ({
      geometry: cmd.do(state.geometry),
      undoStack: [...state.undoStack, cmd],
      redoStack: [],
    }))
  }

  const undo = () => {
    setEditor((state) => {
      if (state.undoStack.length === 0) return state
      const cmd = state.undoStack[state.undoStack.length - 1]
      return {
        geometry: cmd.undo(state.geometry),
        undoStack: state.undoStack.slice(0, -1),
        redoStack: [...state.redoStack, cmd],
      }
    })
  }

  const redo = () => {
    setEditor((state) => {
      if (state.redoStack.length === 0) return state
      const cmd = state.redoStack[state.redoStack.length - 1]
      return {
        geometry: cmd.do(state.geometry),
        redoStack: state.redoStack.slice(0, -1),
        undoStack: [...state.undoStack, cmd],
      }
    })
  }

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null
      if (target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA')) return
      if (!(e.metaKey || e.ctrlKey) || e.key.toLowerCase() !== 'z') return
      e.preventDefault()
      if (e.shiftKey) redo()
      else undo()
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const refreshPieces = async (folderId: string) => {
    const folderPieces = await api.get<PieceOut[]>(`/pieces?folder_id=${folderId}`)
    setPieces(folderPieces)
  }

  const resetEditorState = (doc: PieceGeometryDocument) => {
    setEditor({ geometry: doc, undoStack: [], redoStack: [] })
    setTool(doc.perimeter.length === 0 ? 'draw' : 'edit')
    setPendingSeamEdge(null)
    setPendingDart(null)
    setPendingGradePoint(null)
    setActiveSizeStep(null)
    setShowGradeNest(false)
    setPendingAnnotation(null)
    setPendingMeasurement(null)
    setReferenceImage(null)
  }

  // Switching tools mid-sequence abandons any pending seam/dart/grade/annotation/measurement pick
  // rather than leaving stale inline-input UI referencing points from before the switch.
  const changeTool = (next: Tool) => {
    setTool(next)
    setPendingSeamEdge(null)
    setPendingDart(null)
    setPendingGradePoint(null)
    setPendingAnnotation(null)
    setPendingMeasurement(null)
  }

  const createPiece = async (pieceCode: string, pieceName: string) => {
    if (!folder) return
    setCreating(true)
    setError(null)
    try {
      const piece = await api.post<PieceOut>('/pieces', {
        folder_id: folder.id,
        piece_code: pieceCode,
        piece_name: pieceName,
      })
      await refreshPieces(folder.id)
      setSelectedPiece(piece)
      resetEditorState(emptyGeometry())
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setCreating(false)
    }
  }

  const openPiece = async (piece: PieceOut) => {
    setError(null)
    setSelectedPiece(piece)
    try {
      const doc = await api.get<PieceGeometryDocument>(`/pieces/${piece.id}/geometry`)
      resetEditorState(doc)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    }
  }

  const addPoint = (x: number, y: number) => {
    const point: Point = { point_ref: crypto.randomUUID(), x, y, type: 'corner' }
    runCommand(addPointCommand(point))
  }

  const movePoint = (pointRef: string, from: { x: number; y: number }, to: { x: number; y: number }) => {
    runCommand(movePointCommand(pointRef, from, to))
  }

  const deletePoint = (index: number) => {
    const point = geometry.perimeter[index]
    if (point) runCommand(deletePointCommand(point, index))
  }

  const addLine = (pointRefA: string, pointRefB: string) => {
    const line: InternalLine = { line_ref: crypto.randomUUID(), point_refs: [pointRefA, pointRefB], line_type: 'internal' }
    runCommand(addLineCommand(line))
  }

  const deleteLine = (index: number) => {
    const line = geometry.internal_lines[index]
    if (line) runCommand(deleteLineCommand(line, index))
  }

  const beginSeam = (edgeRef: [string, string]) => {
    const existing = geometry.seams.find(
      (s) => s.edge_ref.length === 2 && s.edge_ref.includes(edgeRef[0]) && s.edge_ref.includes(edgeRef[1]),
    )
    setSeamValue(existing ? String(existing.allowance_mm) : '10')
    setPendingSeamEdge(edgeRef)
  }

  const applySeam = () => {
    if (!pendingSeamEdge) return
    const allowanceMm = Number(seamValue)
    if (!(allowanceMm >= 0)) return
    runCommand(
      setSeamCommand({ edge_ref: pendingSeamEdge, allowance_mm: allowanceMm, corner_type: 'regular' }, geometry.seams),
    )
    setPendingSeamEdge(null)
  }

  const beginDart = (legA: FreePoint, apex: FreePoint, legB: FreePoint) => {
    setDartValue('20')
    setPendingDart({ legA, apex, legB })
  }

  const applyDart = () => {
    if (!pendingDart) return
    const intakeMm = Number(dartValue)
    if (!(intakeMm > 0)) return
    runCommand(
      addDartCommand({
        dart_ref: crypto.randomUUID(),
        leg_a: pendingDart.legA,
        apex: pendingDart.apex,
        leg_b: pendingDart.legB,
        intake_mm: intakeMm,
      }),
    )
    setPendingDart(null)
  }

  const toggleNotch = (pointRef: string) => {
    const index = geometry.notches.findIndex((n) => n.point_ref === pointRef)
    if (index >= 0) {
      runCommand(removeNotchCommand(geometry.notches[index], index))
    } else {
      runCommand(addNotchCommand({ point_ref: pointRef, notch_type: 'V', depth_mm: 5 }))
    }
  }

  const setGrainLine = (start: FreePoint, end: FreePoint) => {
    const angleDeg = (Math.atan2(end.y - start.y, end.x - start.x) * 180) / Math.PI
    runCommand(setGrainLineCommand({ start, end, angle_deg: angleDeg }, geometry.grain_line))
  }

  const clearGrainLine = () => {
    if (!geometry.grain_line) return
    runCommand(setGrainLineCommand(null, geometry.grain_line))
  }

  const setSizeRange = (sizeRange: string[], baseSize: string) => {
    if (
      geometry.grade_rule_table &&
      geometry.grade_rule_table.rules.length > 0 &&
      !window.confirm('Changing the size range clears all existing grade rules. Continue?')
    ) {
      return
    }
    runCommand(setSizeRangeCommand(sizeRange, baseSize, geometry.grade_rule_table))
    setActiveSizeStep(null)
  }

  const beginGradeRule = (pointRef: string) => {
    if (activeSizeStep === null || !geometry.grade_rule_table) return
    const existing = geometry.grade_rule_table.rules.find(
      (r) => r.point_ref === pointRef && r.size_step === activeSizeStep,
    )
    setGradeDeltaX(existing ? String(existing.delta_x) : '0')
    setGradeDeltaY(existing ? String(existing.delta_y) : '0')
    setPendingGradePoint(pointRef)
  }

  const applyGradeRule = () => {
    if (!pendingGradePoint || activeSizeStep === null || !geometry.grade_rule_table) return
    const deltaX = Number(gradeDeltaX)
    const deltaY = Number(gradeDeltaY)
    if (!Number.isFinite(deltaX) || !Number.isFinite(deltaY)) return
    runCommand(
      setGradeRuleCommand(geometry.grade_rule_table, {
        point_ref: pendingGradePoint,
        size_step: activeSizeStep,
        delta_x: deltaX,
        delta_y: deltaY,
      }),
    )
    setPendingGradePoint(null)
  }

  const beginAnnotation = (x: number, y: number) => {
    setAnnotationText('')
    setPendingAnnotation({ x, y })
  }

  const applyAnnotation = () => {
    if (!pendingAnnotation || !annotationText.trim()) return
    runCommand(
      addAnnotationCommand({
        annotation_ref: crypto.randomUUID(),
        x: pendingAnnotation.x,
        y: pendingAnnotation.y,
        text: annotationText.trim(),
      }),
    )
    setPendingAnnotation(null)
  }

  const deleteAnnotation = (index: number) => {
    const annotation = geometry.annotations[index]
    if (annotation) runCommand(removeAnnotationCommand(annotation, index))
  }

  const beginMeasurement = (pointRefA: string, pointRefB: string) => {
    setMeasurementLabel('')
    const a = geometry.perimeter.find((p) => p.point_ref === pointRefA)
    const b = geometry.perimeter.find((p) => p.point_ref === pointRefB)
    setMeasurementTarget(a && b ? String(Math.round(Math.hypot(b.x - a.x, b.y - a.y))) : '')
    setPendingMeasurement([pointRefA, pointRefB])
  }

  const applyMeasurement = () => {
    if (!pendingMeasurement || !measurementLabel.trim()) return
    const targetMm = measurementTarget.trim() === '' ? null : Number(measurementTarget)
    const toleranceMm = measurementTolerance.trim() === '' ? null : Number(measurementTolerance)
    runCommand(
      addMeasurementCommand({
        measurement_ref: crypto.randomUUID(),
        label: measurementLabel.trim(),
        point_ref_a: pendingMeasurement[0],
        point_ref_b: pendingMeasurement[1],
        target_value_mm: targetMm !== null && Number.isFinite(targetMm) ? targetMm : null,
        tolerance_mm: toleranceMm !== null && Number.isFinite(toleranceMm) ? toleranceMm : null,
      }),
    )
    setPendingMeasurement(null)
  }

  const onReferenceImageSelected = (file: File | null) => {
    if (!file) {
      setReferenceImage(null)
      return
    }
    const reader = new FileReader()
    reader.onload = () => {
      const img = new Image()
      img.onload = () => setReferenceImage(img)
      img.src = reader.result as string
    }
    reader.readAsDataURL(file)
  }

  const applyWholePieceTransform = (transform: (doc: PieceGeometryDocument) => PieceGeometryDocument, label: string) => {
    if (geometry.perimeter.length === 0) return
    runCommand(transformDocumentCommand(transform(geometry), geometry, label))
  }

  const openPlotPreview = () => {
    const stage = canvasStageRef.current
    if (!stage) return
    const dataUrl = stage.toDataURL({ pixelRatio: 2 })
    const win = window.open()
    if (win) {
      win.document.write(
        `<title>${selectedPiece?.piece_code ?? 'Piece'} - Plot Preview</title>` +
          `<img src="${dataUrl}" style="max-width:100%" />`,
      )
    }
  }

  const replaceShape = (newPerimeter: Point[], label: string) => {
    if (geometry.perimeter.length > 0 && !window.confirm(`${label} will replace the current perimeter. Continue?`)) {
      return
    }
    runCommand(replaceShapeCommand(newPerimeter, geometry.perimeter, geometry.internal_lines, label))
    changeTool('edit')
  }

  const createRectangle = (widthMm: number, heightMm: number) => {
    if (!(widthMm > 0) || !(heightMm > 0)) return
    replaceShape(rectanglePerimeter(widthMm, heightMm), 'Create rectangle')
  }

  const createCircle = (radiusMm: number) => {
    if (!(radiusMm > 0)) return
    replaceShape(circlePerimeter(radiusMm), 'Create circle')
  }

  const saveGeometry = async () => {
    if (!selectedPiece || !folder) return
    setSaving(true)
    setError(null)
    try {
      const updatedPiece = await api.put<PieceOut>(`/pieces/${selectedPiece.id}/geometry`, geometry)
      setSelectedPiece(updatedPiece)
      await refreshPieces(folder.id)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setSaving(false)
    }
  }

  const submitForApproval = async () => {
    if (!selectedPiece || !folder) return
    setError(null)
    try {
      const updatedPiece = await api.post<PieceOut>(`/pieces/${selectedPiece.id}/status`, {
        to_status: 'needs_approval',
      })
      setSelectedPiece(updatedPiece)
      await refreshPieces(folder.id)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    }
  }

  return (
    <div className="app">
      <header className="app__header">
        <h1>Zeus Suite — Pattern Design</h1>
        <IdentityBar />
      </header>

      {error && <p className="error-text">{error}</p>}

      {!folder ? (
        <p className="hint">Connecting to pattern-design-service…</p>
      ) : (
        <div className="app__main">
          <PieceList
            pieces={pieces}
            selectedPieceId={selectedPiece?.id ?? null}
            onSelect={openPiece}
            onCreate={createPiece}
            creating={creating}
          />

          <div className="app__canvas-column">
            {selectedPiece ? (
              <>
                <div className="app__toolbar">
                  <span className="badge">{selectedPiece.piece_code}</span>
                  <span className={`badge badge--${selectedPiece.workflow_status.code}`}>
                    {selectedPiece.workflow_status.label}
                  </span>
                  <button onClick={undo} disabled={undoStack.length === 0} title="Ctrl/Cmd+Z">
                    Undo
                  </button>
                  <button onClick={redo} disabled={redoStack.length === 0} title="Ctrl/Cmd+Shift+Z">
                    Redo
                  </button>
                  <button onClick={saveGeometry} disabled={saving || geometry.perimeter.length < 3}>
                    {saving ? 'Saving…' : 'Save Geometry'}
                  </button>
                  <button
                    onClick={submitForApproval}
                    disabled={selectedPiece.workflow_status.code !== 'unmade' || !selectedPiece.current_version_id}
                  >
                    Submit for Approval
                  </button>
                  <span className="hint">
                    {geometry.perimeter.length} pt, {geometry.internal_lines.length} line,{' '}
                    {geometry.seams.length} seam, {geometry.darts.length} dart, {geometry.notches.length} notch,{' '}
                    {geometry.grade_rule_table?.rules.length ?? 0} grade rule, {geometry.annotations.length} note,{' '}
                    {geometry.measurements.length} measurement
                    {geometry.grain_line ? ', grain line set' : ''}
                  </span>
                </div>
                <div className="app__toolbar">
                  <div className="tool-group">
                    {(['draw', 'edit', 'add-line', 'delete-line'] as Tool[]).map((t) => (
                      <button
                        key={t}
                        className={t === tool ? 'tool-button tool-button--active' : 'tool-button'}
                        onClick={() => changeTool(t)}
                      >
                        {TOOL_LABELS[t]}
                      </button>
                    ))}
                  </div>
                  <div className="tool-group">
                    {(['seam', 'dart', 'notch', 'grain-line', 'grade', 'annotate', 'measure'] as Tool[]).map((t) => (
                      <button
                        key={t}
                        className={t === tool ? 'tool-button tool-button--active' : 'tool-button'}
                        onClick={() => changeTool(t)}
                      >
                        {TOOL_LABELS[t]}
                      </button>
                    ))}
                  </div>
                  <button onClick={clearGrainLine} disabled={!geometry.grain_line}>
                    Clear Grain Line
                  </button>
                </div>
                <div className="app__toolbar">
                  <div className="tool-group">
                    <button onClick={() => applyWholePieceTransform(rotatePiece90, 'Rotate 90°')}>Rotate 90°</button>
                    <button onClick={() => applyWholePieceTransform(flipPieceHorizontal, 'Flip horizontal')}>
                      Flip H
                    </button>
                    <button onClick={() => applyWholePieceTransform(flipPieceVertical, 'Flip vertical')}>
                      Flip V
                    </button>
                  </div>
                  <button onClick={openPlotPreview} disabled={geometry.perimeter.length < 3}>
                    Plot Preview
                  </button>
                  <span className="hint">Trace reference:</span>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => onReferenceImageSelected(e.target.files?.[0] ?? null)}
                  />
                  {referenceImage && (
                    <>
                      <input
                        type="range"
                        min="0.1"
                        max="1"
                        step="0.1"
                        value={referenceImageOpacity}
                        onChange={(e) => setReferenceImageOpacity(Number(e.target.value))}
                      />
                      <button onClick={() => setReferenceImage(null)}>Clear Image</button>
                    </>
                  )}
                </div>
                <GradingTools
                  key={selectedPiece.id}
                  table={geometry.grade_rule_table}
                  activeSizeStep={activeSizeStep}
                  onSetSizeRange={setSizeRange}
                  onSetActiveSizeStep={setActiveSizeStep}
                  showGradeNest={showGradeNest}
                  onToggleGradeNest={setShowGradeNest}
                  disabled={saving}
                />
                {pendingSeamEdge && (
                  <div className="app__toolbar">
                    <span className="hint">Seam allowance:</span>
                    <input
                      type="number"
                      min="0"
                      value={seamValue}
                      onChange={(e) => setSeamValue(e.target.value)}
                      autoFocus
                    />
                    <span className="hint">mm</span>
                    <button onClick={applySeam}>Apply</button>
                    <button onClick={() => setPendingSeamEdge(null)}>Cancel</button>
                  </div>
                )}
                {pendingDart && (
                  <div className="app__toolbar">
                    <span className="hint">Dart intake:</span>
                    <input
                      type="number"
                      min="0"
                      value={dartValue}
                      onChange={(e) => setDartValue(e.target.value)}
                      autoFocus
                    />
                    <span className="hint">mm</span>
                    <button onClick={applyDart}>Apply</button>
                    <button onClick={() => setPendingDart(null)}>Cancel</button>
                  </div>
                )}
                {pendingGradePoint && (
                  <div className="app__toolbar">
                    <span className="hint">Delta X:</span>
                    <input
                      type="number"
                      value={gradeDeltaX}
                      onChange={(e) => setGradeDeltaX(e.target.value)}
                      autoFocus
                    />
                    <span className="hint">Delta Y:</span>
                    <input type="number" value={gradeDeltaY} onChange={(e) => setGradeDeltaY(e.target.value)} />
                    <span className="hint">mm</span>
                    <button onClick={applyGradeRule}>Apply</button>
                    <button onClick={() => setPendingGradePoint(null)}>Cancel</button>
                  </div>
                )}
                {pendingAnnotation && (
                  <div className="app__toolbar">
                    <span className="hint">Note text:</span>
                    <input
                      value={annotationText}
                      onChange={(e) => setAnnotationText(e.target.value)}
                      autoFocus
                      onKeyDown={(e) => e.key === 'Enter' && applyAnnotation()}
                    />
                    <button onClick={applyAnnotation}>Apply</button>
                    <button onClick={() => setPendingAnnotation(null)}>Cancel</button>
                  </div>
                )}
                {pendingMeasurement && (
                  <div className="app__toolbar">
                    <span className="hint">Label:</span>
                    <input value={measurementLabel} onChange={(e) => setMeasurementLabel(e.target.value)} autoFocus />
                    <span className="hint">Target:</span>
                    <input
                      type="number"
                      value={measurementTarget}
                      onChange={(e) => setMeasurementTarget(e.target.value)}
                    />
                    <span className="hint">± tolerance:</span>
                    <input
                      type="number"
                      value={measurementTolerance}
                      onChange={(e) => setMeasurementTolerance(e.target.value)}
                    />
                    <span className="hint">mm</span>
                    <button onClick={applyMeasurement}>Apply</button>
                    <button onClick={() => setPendingMeasurement(null)}>Cancel</button>
                  </div>
                )}
                <ShapeTools onRectangle={createRectangle} onCircle={createCircle} disabled={saving} />
                <PatternCanvas
                  ref={canvasStageRef}
                  points={geometry.perimeter}
                  internalLines={geometry.internal_lines}
                  seams={geometry.seams}
                  darts={geometry.darts}
                  notches={geometry.notches}
                  grainLine={geometry.grain_line}
                  gradeRuleTable={geometry.grade_rule_table}
                  activeSizeStep={activeSizeStep}
                  showGradeNest={showGradeNest}
                  annotations={geometry.annotations}
                  measurements={geometry.measurements}
                  referenceImage={referenceImage}
                  referenceImageOpacity={referenceImageOpacity}
                  tool={tool}
                  onAddPoint={addPoint}
                  onMovePoint={movePoint}
                  onDeletePoint={deletePoint}
                  onAddLine={addLine}
                  onDeleteLine={deleteLine}
                  onSetSeam={beginSeam}
                  onAddDart={beginDart}
                  onToggleNotch={toggleNotch}
                  onSetGrainLine={setGrainLine}
                  onGradePointClick={beginGradeRule}
                  onAnnotatePick={beginAnnotation}
                  onDeleteAnnotation={deleteAnnotation}
                  onMeasurePointClick={beginMeasurement}
                />
              </>
            ) : (
              <p className="hint">Select a piece, or create a new one, to start drawing its perimeter.</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
