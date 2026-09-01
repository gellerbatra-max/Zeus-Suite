import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { ReportDefinitionOut, ReportRunOut } from '../api/types'

export function ReportsPanel() {
  const [definitions, setDefinitions] = useState<ReportDefinitionOut[]>([])
  const [selectedCode, setSelectedCode] = useState('')
  const [entityId, setEntityId] = useState('')
  const [run, setRun] = useState<ReportRunOut | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [running, setRunning] = useState(false)

  useEffect(() => {
    api.get<ReportDefinitionOut[]>('/reports/definitions').then((defs) => {
      setDefinitions(defs)
      if (defs.length > 0) setSelectedCode(defs[0].code)
    })
  }, [])

  const runReport = () => {
    if (!selectedCode) return
    setRunning(true)
    setError(null)
    setRun(null)
    api
      .post<ReportRunOut>('/reports/run', { report_code: selectedCode, entity_id: entityId || null })
      .then(setRun)
      .catch((err) => setError(err instanceof ApiError ? `${err.code}: ${err.message}` : String(err)))
      .finally(() => setRunning(false))
  }

  return (
    <div className="reports-panel">
      <div className="reports-panel__form">
        <label>
          Report
          <select value={selectedCode} onChange={(e) => setSelectedCode(e.target.value)}>
            {definitions.map((d) => (
              <option key={d.code} value={d.code}>
                {d.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Entity ID (optional — a piece/folder/marker id, depending on the report)
          <input value={entityId} onChange={(e) => setEntityId(e.target.value)} placeholder="uuid" />
        </label>
        <button onClick={runReport} disabled={running || !selectedCode}>
          {running ? 'Running…' : 'Run report'}
        </button>
      </div>

      {definitions.find((d) => d.code === selectedCode)?.description && (
        <p className="reports-panel__description">{definitions.find((d) => d.code === selectedCode)?.description}</p>
      )}

      {error && <p className="error-text">{error}</p>}

      {run && (
        <div className="reports-panel__result">
          <h4>
            Result <span className="badge">{run.status}</span>
          </h4>
          <pre>{JSON.stringify(run.result_inline, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
