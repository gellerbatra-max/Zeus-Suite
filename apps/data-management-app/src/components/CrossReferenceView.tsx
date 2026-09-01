import { useEffect, useState } from 'react'
import { api } from '../api/client'
import type { CrossReferenceOut } from '../api/types'

interface Props {
  entityType: string
  entityId: string
  onClose: () => void
  onViewActivityLog: (entityType: string, entityId: string) => void
  onViewCrossReference: (entityType: string, id: string) => void
}

export function CrossReferenceView({ entityType, entityId, onClose, onViewActivityLog, onViewCrossReference }: Props) {
  const [data, setData] = useState<CrossReferenceOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setData(null)
    setError(null)
    api
      .get<CrossReferenceOut>(`/cross-reference/${entityType}/${entityId}`)
      .catch((err) => {
        setError(err.message)
        return null
      })
      .then((result) => result && setData(result))
  }, [entityType, entityId])

  const relatedGroups = data ? Object.entries(data.related).filter(([, rows]) => rows.length > 0) : []

  return (
    <div className="cross-ref-overlay">
      <div className="cross-ref-panel">
        <div className="cross-ref-panel__header">
          <h3>
            Cross-references for <span className="badge">{entityType}</span> {entityId.slice(0, 8)}…
          </h3>
          <button onClick={onClose}>Close</button>
        </div>

        <button className="cross-ref-panel__activity-log" onClick={() => onViewActivityLog(entityType, entityId)}>
          View Activity Log for this item
        </button>

        {error && <p className="error-text">{error}</p>}
        {!data && !error && <p>Loading…</p>}

        {data && relatedGroups.length === 0 && <p className="browser__hint">No related entities found.</p>}

        {relatedGroups.map(([relatedType, rows]) => (
          <div key={relatedType} className="result-group">
            <h4>
              {relatedType} <span className="result-group__count">({rows.length})</span>
            </h4>
            <ul className="cross-ref-list">
              {rows.map((row) => (
                <li key={row.id}>
                  <span className="badge">{row.workflow_status}</span> {row.code} — {row.name}
                  <button onClick={() => onViewCrossReference(relatedType, row.id)}>Follow</button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  )
}
