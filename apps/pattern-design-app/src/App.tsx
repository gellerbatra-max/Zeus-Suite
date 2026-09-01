import { useEffect, useRef, useState } from 'react'
import { IdentityBar } from './components/IdentityBar'
import { PieceList } from './components/PieceList'
import { PatternCanvas } from './components/PatternCanvas'
import type { Tool } from './components/PatternCanvas'
import { ShapeTools } from './components/ShapeTools'
import { api, ApiError } from './api/client'
import type { FolderOut, InternalLine, PieceGeometryDocument, PieceOut, Point } from './api/types'
import {
  addLineCommand,
  addPointCommand,
  deleteLineCommand,
  deletePointCommand,
  movePointCommand,
  replaceShapeCommand,
} from './commands'
import type { Command } from './commands'
import { circlePerimeter, rectanglePerimeter } from './shapes'

const DEFAULT_FOLDER_NAME = 'Pattern Design Pieces'

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
    annotations: [],
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

  const replaceShape = (newPerimeter: Point[], label: string) => {
    if (geometry.perimeter.length > 0 && !window.confirm(`${label} will replace the current perimeter. Continue?`)) {
      return
    }
    runCommand(replaceShapeCommand(newPerimeter, geometry.perimeter, geometry.internal_lines, label))
    setTool('edit')
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
                  <div className="tool-group">
                    {(['draw', 'edit', 'add-line', 'delete-line'] as Tool[]).map((t) => (
                      <button
                        key={t}
                        className={t === tool ? 'tool-button tool-button--active' : 'tool-button'}
                        onClick={() => setTool(t)}
                      >
                        {{ draw: 'Draw', edit: 'Pan/Edit', 'add-line': 'Add Line', 'delete-line': 'Delete Line' }[t]}
                      </button>
                    ))}
                  </div>
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
                    {geometry.perimeter.length} point(s), {geometry.internal_lines.length} line(s)
                  </span>
                </div>
                <ShapeTools onRectangle={createRectangle} onCircle={createCircle} disabled={saving} />
                <PatternCanvas
                  points={geometry.perimeter}
                  internalLines={geometry.internal_lines}
                  tool={tool}
                  onAddPoint={addPoint}
                  onMovePoint={movePoint}
                  onDeletePoint={deletePoint}
                  onAddLine={addLine}
                  onDeleteLine={deleteLine}
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
