import { useState } from 'react'
import { IdentityBar } from './components/IdentityBar'
import { MigrationPanel } from './components/MigrationPanel'
import { api, ApiError } from './api/client'
import type { ExportIgesJobOut, ImportIgesJobOut } from './api/types'

// This app's whole job is single-piece IGES export (format_interchange_plan.md Sec 7 Step 1) --
// there's no piece browser here (that's Pattern Design's job); the operator supplies a piece_id
// obtained from there, matching how a real interchange utility is a targeted conversion tool, not
// a general piece manager.
export default function App() {
  const [pieceId, setPieceId] = useState('')
  const [includeInternalLines, setIncludeInternalLines] = useState(true)
  const [includeNotches, setIncludeNotches] = useState(true)
  const [includeGrainLine, setIncludeGrainLine] = useState(true)
  const [exporting, setExporting] = useState(false)
  const [result, setResult] = useState<ExportIgesJobOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [pollJobId, setPollJobId] = useState('')
  const [polling, setPolling] = useState(false)

  const [importFile, setImportFile] = useState<File | null>(null)
  const [closureAmount, setClosureAmount] = useState('2')
  const [trimTolerance, setTrimTolerance] = useState('0')
  const [pasteInternalToNotch, setPasteInternalToNotch] = useState(false)
  const [pointsToDrillHoles, setPointsToDrillHoles] = useState(false)
  const [unitOverride, setUnitOverride] = useState('')
  const [targetCollection, setTargetCollection] = useState('')
  const [stageOnly, setStageOnly] = useState(true)
  const [importing, setImporting] = useState(false)
  const [importResult, setImportResult] = useState<ImportIgesJobOut | null>(null)
  const [importError, setImportError] = useState<string | null>(null)
  const [committing, setCommitting] = useState(false)

  const runExport = async () => {
    if (!pieceId.trim()) return
    setExporting(true)
    setError(null)
    setResult(null)
    try {
      const job = await api.post<ExportIgesJobOut>(`/pieces/${pieceId.trim()}/export/iges`, {
        include_internal_lines: includeInternalLines,
        include_notches: includeNotches,
        include_grain_line: includeGrainLine,
      })
      setResult(job)
      setPollJobId(job.job_id)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setExporting(false)
    }
  }

  const checkJob = async () => {
    if (!pollJobId.trim()) return
    setPolling(true)
    setError(null)
    try {
      const job = await api.get<ExportIgesJobOut>(`/export/iges/jobs/${pollJobId.trim()}`)
      setResult(job)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setPolling(false)
    }
  }

  const runImport = async () => {
    if (!importFile) return
    setImporting(true)
    setImportError(null)
    setImportResult(null)
    try {
      const options = {
        closure_amount_mm: Number(closureAmount) || 0,
        trim_tolerance: Number(trimTolerance) || 0,
        paste_internal_to_notch: pasteInternalToNotch,
        points_to_drill_holes: pointsToDrillHoles,
        unit_override: unitOverride || null,
        target_collection: targetCollection.trim() || null,
        stage_only: stageOnly,
      }
      const form = new FormData()
      form.append('file', importFile)
      form.append('options', JSON.stringify(options))
      const job = await api.postForm<ImportIgesJobOut>('/import/iges', form)
      setImportResult(job)
    } catch (err) {
      setImportError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setImporting(false)
    }
  }

  const commitImport = async () => {
    if (!importResult) return
    setCommitting(true)
    setImportError(null)
    try {
      const job = await api.post<ImportIgesJobOut>(`/import/iges/jobs/${importResult.job_id}/commit`)
      setImportResult(job)
    } catch (err) {
      setImportError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setCommitting(false)
    }
  }

  return (
    <div className="app">
      <header className="app__header">
        <h1>Zeus Suite — Format Interchange</h1>
        <IdentityBar />
      </header>

      <div className="app__main">
        <section className="panel">
          <h2>Export Piece to IGES</h2>
          <div className="field">
            <label htmlFor="piece-id">Piece ID</label>
            <input
              id="piece-id"
              value={pieceId}
              onChange={(e) => setPieceId(e.target.value)}
              placeholder="uuid from Pattern Design"
              onKeyDown={(e) => e.key === 'Enter' && runExport()}
            />
          </div>
          <div className="checkbox-row">
            <label>
              <input type="checkbox" checked={includeInternalLines} onChange={(e) => setIncludeInternalLines(e.target.checked)} />
              Internal lines
            </label>
            <label>
              <input type="checkbox" checked={includeNotches} onChange={(e) => setIncludeNotches(e.target.checked)} />
              Notches
            </label>
            <label>
              <input type="checkbox" checked={includeGrainLine} onChange={(e) => setIncludeGrainLine(e.target.checked)} />
              Grain line
            </label>
          </div>
          <button onClick={runExport} disabled={exporting || !pieceId.trim()}>
            {exporting ? 'Exporting…' : 'Export to IGES'}
          </button>
        </section>

        <section className="panel">
          <h2>Check Export Job Status</h2>
          <div className="field">
            <label htmlFor="job-id">Job ID</label>
            <input
              id="job-id"
              value={pollJobId}
              onChange={(e) => setPollJobId(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && checkJob()}
            />
          </div>
          <button onClick={checkJob} disabled={polling || !pollJobId.trim()}>
            {polling ? 'Checking…' : 'Check Status'}
          </button>
        </section>

        {error && <p className="error-text">{error}</p>}

        {result && (
          <section className="panel result">
            <h2>Result</h2>
            <p>
              <span className="hint">Job:</span> {result.job_id}
            </p>
            <p>
              <span className="hint">Piece:</span> {result.piece_code ?? result.piece_id}
            </p>
            <p>
              <span className={`badge badge--${result.status}`}>{result.status}</span>
            </p>
            {result.download_url && (
              <p>
                <a href={result.download_url} target="_blank" rel="noreferrer">
                  Download IGES file
                </a>
              </p>
            )}
            {result.error_detail && <p className="error-text">{result.error_detail}</p>}
          </section>
        )}

        <section className="panel">
          <h2>Import IGES</h2>
          <div className="field">
            <label htmlFor="import-file">IGES file</label>
            <input
              id="import-file"
              type="file"
              accept=".igs,.iges"
              onChange={(e) => setImportFile(e.target.files?.[0] ?? null)}
            />
          </div>
          <div className="field">
            <label htmlFor="closure-amount">Closure amount (mm)</label>
            <input id="closure-amount" value={closureAmount} onChange={(e) => setClosureAmount(e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="trim-tolerance">Trim tolerance (mm)</label>
            <input id="trim-tolerance" value={trimTolerance} onChange={(e) => setTrimTolerance(e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="unit-override">Unit override</label>
            <select id="unit-override" value={unitOverride} onChange={(e) => setUnitOverride(e.target.value)}>
              <option value="">Auto-detect</option>
              <option value="mm">mm</option>
              <option value="in">in</option>
            </select>
          </div>
          <div className="field">
            <label htmlFor="target-collection">Target folder ID (target_collection)</label>
            <input
              id="target-collection"
              value={targetCollection}
              onChange={(e) => setTargetCollection(e.target.value)}
              placeholder="uuid -- required to commit"
            />
          </div>
          <div className="checkbox-row">
            <label>
              <input
                type="checkbox"
                checked={pasteInternalToNotch}
                onChange={(e) => setPasteInternalToNotch(e.target.checked)}
              />
              Paste internal to notch
            </label>
            <label>
              <input
                type="checkbox"
                checked={pointsToDrillHoles}
                onChange={(e) => setPointsToDrillHoles(e.target.checked)}
              />
              Points → drill holes
            </label>
            <label>
              <input type="checkbox" checked={stageOnly} onChange={(e) => setStageOnly(e.target.checked)} />
              Stage only (review before commit)
            </label>
          </div>
          <button onClick={runImport} disabled={importing || !importFile}>
            {importing ? 'Importing…' : 'Import IGES'}
          </button>
        </section>

        {importError && <p className="error-text">{importError}</p>}

        {importResult && (
          <section className="panel result">
            <h2>Import Viewer</h2>
            <p>
              <span className="hint">Job:</span> {importResult.job_id}
            </p>
            <p>
              <span className={`badge badge--${importResult.status}`}>{importResult.status}</span>
            </p>
            {importResult.target_piece_id && (
              <p>
                <span className="hint">Committed piece:</span> {importResult.target_piece_id}
              </p>
            )}
            {importResult.geometry && (
              <p>
                <span className="hint">Converted:</span> {importResult.geometry.perimeter.length} perimeter points,{' '}
                {importResult.geometry.internal_lines.length} internal lines, {importResult.geometry.notches.length} notches,{' '}
                {importResult.geometry.grain_line ? 'grain line present' : 'no grain line'}
              </p>
            )}
            {importResult.source_summary && (
              <p>
                <span className="hint">Raw source:</span> {importResult.source_summary.line_count} lines,{' '}
                {importResult.source_summary.point_count} points, declared unit{' '}
                {importResult.source_summary.declared_unit}
              </p>
            )}
            {importResult.warnings.length > 0 && (
              <div>
                <span className="hint">Warnings:</span>
                <ul>
                  {importResult.warnings.map((w, i) => (
                    <li key={i}>
                      <strong>{w.code}</strong>: {w.message}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {importResult.error_detail && <p className="error-text">{importResult.error_detail}</p>}
            {importResult.status === 'staged' && (
              <button onClick={commitImport} disabled={committing}>
                {committing ? 'Committing…' : 'Approve & Commit'}
              </button>
            )}
          </section>
        )}

        <MigrationPanel />
      </div>
    </div>
  )
}
