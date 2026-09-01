import { Fragment, useEffect, useState } from 'react'
import { api } from '../api/client'
import type { AuditLogOut, Page } from '../api/types'

interface Props {
  presetFilter: { entityType: string; entityId: string } | null
  onClearPreset: () => void
}

export function ActivityLogViewer({ presetFilter, onClearPreset }: Props) {
  const [entityType, setEntityType] = useState('')
  const [entityId, setEntityId] = useState('')
  const [action, setAction] = useState('')
  const [result, setResult] = useState('')
  const [rows, setRows] = useState<AuditLogOut[]>([])
  const [expanded, setExpanded] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (presetFilter) {
      setEntityType(presetFilter.entityType)
      setEntityId(presetFilter.entityId)
    }
  }, [presetFilter])

  const load = () => {
    api
      .get<Page<AuditLogOut>>('/audit-log', {
        entity_type: entityType || undefined,
        entity_id: entityId || undefined,
        action: action || undefined,
        result: result || undefined,
        page_size: 100,
      })
      .then((page) => setRows(page.items))
      .catch((err) => setError(err.message))
  }

  useEffect(load, [entityType, entityId, action, result])

  return (
    <div className="activity-log">
      <div className="activity-log__filters">
        <label>
          Entity type
          <input value={entityType} onChange={(e) => setEntityType(e.target.value)} placeholder="piece" />
        </label>
        <label>
          Entity ID
          <input value={entityId} onChange={(e) => setEntityId(e.target.value)} placeholder="uuid" />
        </label>
        <label>
          Action
          <input value={action} onChange={(e) => setAction(e.target.value)} placeholder="piece.create" />
        </label>
        <label>
          Result
          <select value={result} onChange={(e) => setResult(e.target.value)}>
            <option value="">any</option>
            <option value="success">success</option>
            <option value="denied">denied</option>
            <option value="error">error</option>
          </select>
        </label>
        {(entityType || entityId) && (
          <button
            onClick={() => {
              setEntityType('')
              setEntityId('')
              onClearPreset()
            }}
          >
            Clear filter
          </button>
        )}
      </div>

      {error && <p className="error-text">{error}</p>}

      <table className="data-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Action</th>
            <th>Entity</th>
            <th>Result</th>
            <th>Detail</th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 && (
            <tr>
              <td colSpan={5} className="data-table__empty">
                No matching activity.
              </td>
            </tr>
          )}
          {rows.map((row) => (
            <Fragment key={row.id}>
              <tr className="activity-log__row" onClick={() => setExpanded(expanded === row.id ? null : row.id)}>
                <td>{new Date(row.occurred_at).toLocaleString()}</td>
                <td>{row.action}</td>
                <td>
                  {row.entity_type}
                  {row.entity_id ? ` ${row.entity_id.slice(0, 8)}…` : ''}
                </td>
                <td>
                  <span className={`badge badge--${row.result}`}>{row.result}</span>
                </td>
                <td>{row.detail ?? ''}</td>
              </tr>
              {expanded === row.id && (
                <tr className="activity-log__detail-row">
                  <td colSpan={5}>
                    <div className="activity-log__diff">
                      <div>
                        <strong>Before</strong>
                        <pre>{JSON.stringify(row.before_state, null, 2) ?? 'null'}</pre>
                      </div>
                      <div>
                        <strong>After</strong>
                        <pre>{JSON.stringify(row.after_state, null, 2) ?? 'null'}</pre>
                      </div>
                    </div>
                  </td>
                </tr>
              )}
            </Fragment>
          ))}
        </tbody>
      </table>
    </div>
  )
}
