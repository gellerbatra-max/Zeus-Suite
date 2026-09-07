import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { MarkerSearchResponse, MarkerSearchResult } from '../api/types'
import { loadRecentMarkers, type RecentMarker } from '../recentMarkers'

interface Props {
  onOpenMarker: (markerId: string) => void
}

function errMessage(err: unknown): string {
  return err instanceof ApiError ? err.message : String(err)
}

const STATUS_OPTIONS = ['unmade', 'needs_approval', 'partial', 'made', 'approved']

export function MarkerPicker({ onOpenMarker }: Props) {
  const [open, setOpen] = useState(false)
  const [text, setText] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [results, setResults] = useState<MarkerSearchResult[] | null>(null)
  const [recent, setRecent] = useState<RecentMarker[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (open) {
      setRecent(loadRecentMarkers())
      // Reopening always starts on Recent, not whatever was searched last time.
      setResults(null)
      setText('')
      setStatusFilter('')
      setError(null)
    }
  }, [open])

  const search = async () => {
    setLoading(true)
    setError(null)
    try {
      const resp = await api.post<MarkerSearchResponse>('/markers/search', {
        text: text.trim() || null,
        workflow_status: statusFilter ? [statusFilter] : null,
      })
      setResults(resp.results)
    } catch (err) {
      setError(errMessage(err))
    } finally {
      setLoading(false)
    }
  }

  const handleOpen = (markerId: string) => {
    setOpen(false)
    onOpenMarker(markerId)
  }

  return (
    <div className="marker-picker">
      <button onClick={() => setOpen((v) => !v)}>{open ? 'Close Browse' : 'Browse Markers'}</button>
      {open && (
        <div className="marker-picker__panel">
          {error && <p className="error-text">{error}</p>}
          <div className="marker-picker__inline-form">
            <input
              placeholder="Search by code or name"
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && search()}
            />
            <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              <option value="">Any status</option>
              {STATUS_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
            <button onClick={search} disabled={loading}>
              {loading ? 'Searching…' : 'Search'}
            </button>
          </div>

          {results != null && (
            <ul className="marker-picker__list">
              {results.length === 0 && <li className="hint">No markers found.</li>}
              {results.map((m) => (
                <li key={m.id}>
                  <button className="marker-picker__result" onClick={() => handleOpen(m.id)}>
                    <span className="marker-picker__result-code">{m.code}</span>
                    <span className="hint">{m.name}</span>
                    <span className={`badge badge--${m.workflow_status}`}>{m.workflow_status}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}

          {results == null && recent.length > 0 && (
            <>
              <label>Recent</label>
              <ul className="marker-picker__list">
                {recent.map((m) => (
                  <li key={m.id}>
                    <button className="marker-picker__result" onClick={() => handleOpen(m.id)}>
                      <span className="marker-picker__result-code">{m.markerCode}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  )
}
