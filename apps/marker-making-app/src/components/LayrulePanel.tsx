import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { ApplyLayruleResult, LayruleOut, LayruleSearchTableOut, WorkspaceOut } from '../api/types'

interface Props {
  markerId: string
  onApplied: (workspace: WorkspaceOut) => void
}

interface LayruleSettings {
  force_layrule_name: string | null
  layrule_search_table_id: string | null
}

function errMessage(err: unknown): string {
  return err instanceof ApiError ? err.message : String(err)
}

export function LayrulePanel({ markerId, onApplied }: Props) {
  const [searchTables, setSearchTables] = useState<LayruleSearchTableOut[]>([])
  const [layrules, setLayrules] = useState<LayruleOut[]>([])
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<ApplyLayruleResult | null>(null)

  const [forceNameInput, setForceNameInput] = useState('')
  const [searchTableSelect, setSearchTableSelect] = useState('')
  const [captureName, setCaptureName] = useState('')
  const [applyLayruleId, setApplyLayruleId] = useState('')

  const [newTableName, setNewTableName] = useState('')
  const [newTableDeviation, setNewTableDeviation] = useState('5')
  const [newTableAllowOverrides, setNewTableAllowOverrides] = useState(true)

  useEffect(() => {
    api
      .get<{ items: LayruleSearchTableOut[] }>('/layrule-search-tables')
      .then((page) => setSearchTables(page.items))
      .catch((err) => setError(errMessage(err)))
    api
      .get<{ items: LayruleOut[] }>('/layrules')
      .then((page) => setLayrules(page.items))
      .catch((err) => setError(errMessage(err)))
    api
      .get<LayruleSettings>(`/markers/${markerId}/layrules/settings`)
      .then((s) => {
        setForceNameInput(s.force_layrule_name ?? '')
        setSearchTableSelect(s.layrule_search_table_id ?? '')
      })
      .catch((err) => setError(errMessage(err)))
  }, [markerId])

  const createSearchTable = async () => {
    if (!newTableName.trim()) return
    setError(null)
    try {
      const created = await api.post<LayruleSearchTableOut>('/layrule-search-tables', {
        name: newTableName.trim(),
        area_deviation_pct: Number(newTableDeviation) || 0,
        allow_overrides: newTableAllowOverrides,
      })
      setSearchTables((prev) => [...prev, created])
      setNewTableName('')
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteSearchTable = async (id: string) => {
    setError(null)
    try {
      await api.delete(`/layrule-search-tables/${id}`)
      setSearchTables((prev) => prev.filter((t) => t.id !== id))
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const saveSettings = async () => {
    setError(null)
    try {
      const updated = await api.patch<LayruleSettings>(`/markers/${markerId}/layrules/settings`, {
        force_layrule_name: forceNameInput || null,
        layrule_search_table_id: searchTableSelect || null,
      })
      setForceNameInput(updated.force_layrule_name ?? '')
      setSearchTableSelect(updated.layrule_search_table_id ?? '')
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const captureLayrule = async () => {
    if (!captureName.trim()) return
    setError(null)
    try {
      const created = await api.post<LayruleOut>(`/markers/${markerId}/layrules/capture`, {
        name: captureName.trim(),
      })
      setLayrules((prev) => [...prev, created])
      setCaptureName('')
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteLayrule = async (id: string) => {
    setError(null)
    try {
      await api.delete(`/layrules/${id}`)
      setLayrules((prev) => prev.filter((r) => r.id !== id))
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const applyLayrule = async () => {
    if (!applyLayruleId) return
    setError(null)
    setResult(null)
    try {
      const applyResult = await api.post<ApplyLayruleResult>(`/markers/${markerId}/layrules/apply`, {
        layrule_id: applyLayruleId,
      })
      setResult(applyResult)
      const workspace = await api.get<WorkspaceOut>(`/markers/${markerId}/workspace`)
      onApplied(workspace)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  return (
    <div className="layrule-panel">
      <h3>Layrules</h3>
      {error && <p className="error-text">{error}</p>}

      <section className="layrule-panel__section">
        <label>Layrule Search Parameter Tables</label>
        <ul className="layrule-panel__list">
          {searchTables.map((t) => (
            <li key={t.id}>
              <span>
                {t.name} ({t.area_deviation_pct}% dev, {t.allow_overrides ? 'overrides ok' : 'no overrides'})
              </span>
              <button onClick={() => deleteSearchTable(t.id)}>Delete</button>
            </li>
          ))}
        </ul>
        <div className="layrule-panel__inline-form">
          <input placeholder="Name" value={newTableName} onChange={(e) => setNewTableName(e.target.value)} />
          <input
            placeholder="Area deviation %"
            value={newTableDeviation}
            onChange={(e) => setNewTableDeviation(e.target.value)}
          />
        </div>
        <label className="layrule-panel__checkbox">
          <input
            type="checkbox"
            checked={newTableAllowOverrides}
            onChange={(e) => setNewTableAllowOverrides(e.target.checked)}
          />
          Allow overrides
        </label>
        <button onClick={createSearchTable}>Add Table</button>
      </section>

      <section className="layrule-panel__section">
        <label>This marker's layrule settings</label>
        <div className="layrule-panel__inline-form">
          <input
            placeholder="Force layrule name"
            value={forceNameInput}
            onChange={(e) => setForceNameInput(e.target.value)}
          />
        </div>
        <select value={searchTableSelect} onChange={(e) => setSearchTableSelect(e.target.value)}>
          <option value="">(no search table)</option>
          {searchTables.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name}
            </option>
          ))}
        </select>
        <button onClick={saveSettings}>Save</button>
      </section>

      <section className="layrule-panel__section">
        <label>Capture this marker's layout as a layrule</label>
        <div className="layrule-panel__inline-form">
          <input placeholder="Layrule name" value={captureName} onChange={(e) => setCaptureName(e.target.value)} />
          <button onClick={captureLayrule}>Capture Layrule</button>
        </div>
      </section>

      <section className="layrule-panel__section">
        <label>Apply a layrule to this marker</label>
        <div className="layrule-panel__inline-form">
          <select value={applyLayruleId} onChange={(e) => setApplyLayruleId(e.target.value)}>
            <option value="">(choose a layrule)</option>
            {layrules.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} ({r.piece_count} pieces)
              </option>
            ))}
          </select>
          <button disabled={!applyLayruleId} onClick={applyLayrule}>
            Apply
          </button>
        </div>
        {result && (
          <p className="layrule-panel__result">
            Applied {result.applied_piece_ids.length}, unmatched {result.unmatched_piece_ids.length}
            {result.area_deviation_pct != null ? `, area deviation ${result.area_deviation_pct}%` : ''}
            {result.warning ? ` — ${result.warning}` : ''}
          </p>
        )}
      </section>

      <section className="layrule-panel__section">
        <label>All layrules ({layrules.length})</label>
        <ul className="layrule-panel__list">
          {layrules.map((r) => (
            <li key={r.id}>
              <span>
                {r.name} ({r.piece_count} pieces)
              </span>
              <button onClick={() => deleteLayrule(r.id)}>Delete</button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
