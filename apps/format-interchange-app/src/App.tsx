import { useState } from 'react'
import { IdentityBar } from './components/IdentityBar'
import { api, ApiError } from './api/client'
import type { ExportIgesJobOut } from './api/types'

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
      </div>
    </div>
  )
}
