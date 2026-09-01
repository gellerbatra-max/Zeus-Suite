import { useState } from 'react'
import { api } from '../api/client'
import { SEARCHABLE_ENTITY_TYPES } from '../api/types'
import type { SearchResponse, SearchResultRow } from '../api/types'

interface Props {
  onViewCrossReference: (entityType: string, id: string) => void
}

export function SearchPanel({ onViewCrossReference }: Props) {
  const [text, setText] = useState('')
  const [entityTypes, setEntityTypes] = useState<string[]>([...SEARCHABLE_ENTITY_TYPES])
  const [results, setResults] = useState<SearchResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const toggleType = (type: string) => {
    setEntityTypes((prev) => (prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]))
  }

  const runSearch = () => {
    setLoading(true)
    setError(null)
    api
      .post<SearchResponse>('/search', {
        entity_types: entityTypes,
        text: text.trim() || null,
        page: 1,
        page_size: 50,
      })
      .then(setResults)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  return (
    <div className="search-panel">
      <div className="search-panel__form">
        <input
          className="search-panel__text"
          placeholder="Search by code or name (e.g. PANEL, STY-0001)…"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && runSearch()}
        />
        <div className="search-panel__types">
          {SEARCHABLE_ENTITY_TYPES.map((type) => (
            <label key={type}>
              <input type="checkbox" checked={entityTypes.includes(type)} onChange={() => toggleType(type)} />
              {type}
            </label>
          ))}
        </div>
        <button onClick={runSearch} disabled={loading}>
          {loading ? 'Searching…' : 'Search'}
        </button>
      </div>

      {error && <p className="error-text">{error}</p>}

      {results && (
        <div className="search-panel__results">
          {Object.entries(results.results).map(([entityType, rows]) => (
            <ResultGroup
              key={entityType}
              entityType={entityType}
              rows={rows}
              total={results.total_by_type[entityType] ?? rows.length}
              onViewCrossReference={onViewCrossReference}
            />
          ))}
        </div>
      )}
    </div>
  )
}

function ResultGroup({
  entityType,
  rows,
  total,
  onViewCrossReference,
}: {
  entityType: string
  rows: SearchResultRow[]
  total: number
  onViewCrossReference: (entityType: string, id: string) => void
}) {
  if (rows.length === 0) return null
  return (
    <div className="result-group">
      <h4>
        {entityType} <span className="result-group__count">({total})</span>
      </h4>
      <table className="data-table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Folder</th>
            <th>Status</th>
            <th>Updated</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>{row.code}</td>
              <td>{row.name}</td>
              <td>{row.folder_path ?? '—'}</td>
              <td>
                <span className="badge">{row.workflow_status}</span>
              </td>
              <td>{new Date(row.updated_at).toLocaleString()}</td>
              <td>
                <button onClick={() => onViewCrossReference(entityType, row.id)}>Cross-references</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
