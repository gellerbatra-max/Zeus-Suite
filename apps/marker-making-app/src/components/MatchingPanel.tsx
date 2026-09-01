import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { MatchingRuleTableOut, StripeDefinition, ValidateBiteOut } from '../api/types'

interface Props {
  markerId: string
  matchingMethod: string | null
  matchingRuleTableId: string | null
  selectedPieceId: string | null
  selectedPieceStripeMarkId: string | null
  onMatchingApplied: (method: string | null, ruleTableId: string | null) => void
  onAssignMark: (pieceId: string, markId: string | null) => void
}

function errMessage(err: unknown): string {
  return err instanceof ApiError ? err.message : String(err)
}

export function MatchingPanel({
  markerId,
  matchingMethod,
  matchingRuleTableId,
  selectedPieceId,
  selectedPieceStripeMarkId,
  onMatchingApplied,
  onAssignMark,
}: Props) {
  const [tables, setTables] = useState<MatchingRuleTableOut[]>([])
  const [table, setTable] = useState<MatchingRuleTableOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [newTableName, setNewTableName] = useState('')
  const [newTableMethod, setNewTableMethod] = useState<'standard' | 'five_star'>('standard')

  const [offsetsH, setOffsetsH] = useState<string>('')
  const [offsetsV, setOffsetsV] = useState<string>('')

  const [defForm, setDefForm] = useState({ name: '', origin_x: '0', origin_y: '0', h_distance: '', v_distance: '' })
  const [markForm, setMarkForm] = useState({ name: '', stripe_definition_id: '', x: '0', y: '0' })

  const [biteLength, setBiteLength] = useState('20')
  const [biteResult, setBiteResult] = useState<ValidateBiteOut | null>(null)

  useEffect(() => {
    api
      .get<{ items: MatchingRuleTableOut[] }>('/matching-rule-tables')
      .then((page) => setTables(page.items))
      .catch((err) => setError(errMessage(err)))
  }, [])

  useEffect(() => {
    if (!matchingRuleTableId) {
      setTable(null)
      return
    }
    api
      .get<MatchingRuleTableOut>(`/matching-rule-tables/${matchingRuleTableId}`)
      .then((t) => {
        setTable(t)
        setOffsetsH(t.offsets.horizontal.join(', '))
        setOffsetsV(t.offsets.vertical.join(', '))
      })
      .catch((err) => setError(errMessage(err)))
  }, [matchingRuleTableId])

  const refreshTable = (t: MatchingRuleTableOut) => {
    setTable(t)
    setTables((prev) => (prev.some((x) => x.id === t.id) ? prev.map((x) => (x.id === t.id ? t : x)) : [...prev, t]))
  }

  const createTable = async () => {
    if (!newTableName.trim()) return
    setError(null)
    try {
      const created = await api.post<MatchingRuleTableOut>('/matching-rule-tables', {
        name: newTableName.trim(),
        method: newTableMethod,
      })
      setTables((prev) => [...prev, created])
      setNewTableName('')
      await applyMatching(created.id, matchingMethod ?? newTableMethod)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const applyMatching = async (ruleTableId: string | null, method: string | null) => {
    setError(null)
    try {
      const body: Record<string, string | null> = {}
      if (ruleTableId !== undefined) body.matching_rule_table_id = ruleTableId
      if (method !== undefined) body.matching_method = method
      await api.post(`/markers/${markerId}/matching/apply`, body)
      onMatchingApplied(method ?? matchingMethod, ruleTableId ?? matchingRuleTableId)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const saveOffsets = async () => {
    if (!table) return
    setError(null)
    try {
      const horizontal = offsetsH.split(',').map((s) => s.trim()).filter(Boolean).map(Number).slice(0, 3)
      const vertical = offsetsV.split(',').map((s) => s.trim()).filter(Boolean).map(Number).slice(0, 3)
      const updated = await api.put<MatchingRuleTableOut>(`/matching-rule-tables/${table.id}/offsets`, {
        horizontal, vertical,
      })
      refreshTable(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const addStripeDefinition = async () => {
    if (!table || !defForm.name.trim()) return
    setError(null)
    try {
      const updated = await api.post<MatchingRuleTableOut>(`/matching-rule-tables/${table.id}/stripe-definitions`, {
        name: defForm.name.trim(),
        origin_x: Number(defForm.origin_x) || 0,
        origin_y: Number(defForm.origin_y) || 0,
        h_distance: Number(defForm.h_distance) || 0,
        v_distance: Number(defForm.v_distance) || 0,
      })
      refreshTable(updated)
      setDefForm({ name: '', origin_x: '0', origin_y: '0', h_distance: '', v_distance: '' })
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteStripeDefinition = async (def: StripeDefinition) => {
    if (!table) return
    setError(null)
    try {
      const updated = await api.delete<MatchingRuleTableOut>(`/matching-rule-tables/${table.id}/stripe-definitions/${def.id}`)
      refreshTable(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const addStripeMark = async () => {
    if (!table || !markForm.name.trim()) return
    setError(null)
    try {
      const updated = await api.post<MatchingRuleTableOut>(`/matching-rule-tables/${table.id}/stripe-marks`, {
        name: markForm.name.trim(),
        stripe_definition_id: markForm.stripe_definition_id || null,
        position: { x: Number(markForm.x) || 0, y: Number(markForm.y) || 0 },
      })
      refreshTable(updated)
      setMarkForm({ name: '', stripe_definition_id: '', x: '0', y: '0' })
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteStripeMark = async (markId: string) => {
    if (!table) return
    setError(null)
    try {
      const updated = await api.delete<MatchingRuleTableOut>(`/matching-rule-tables/${table.id}/stripe-marks/${markId}`)
      refreshTable(updated)
      if (selectedPieceId && selectedPieceStripeMarkId === markId) onAssignMark(selectedPieceId, null)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const stepMark = async (markId: string, direction: 'next' | 'prev') => {
    if (!table) return
    setError(null)
    try {
      const adjacent = await api.post<{ id: string }>(
        `/matching-rule-tables/${table.id}/stripe-marks/${markId}/step`,
        { direction },
      )
      if (selectedPieceId) onAssignMark(selectedPieceId, adjacent.id)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const runValidateBite = async () => {
    setError(null)
    try {
      const result = await api.get<ValidateBiteOut>(
        `/markers/${markerId}/matching/validate-bite?bite_length=${encodeURIComponent(biteLength)}`,
      )
      setBiteResult(result)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const sortedMarks = table ? [...table.stripe_marks].sort((a, b) => a.sequence - b.sequence) : []

  return (
    <div className="matching-panel">
      <h3>Matching</h3>
      {error && <p className="error-text">{error}</p>}

      <section className="matching-panel__section">
        <label>Rule table</label>
        <select
          value={matchingRuleTableId ?? ''}
          onChange={(e) => applyMatching(e.target.value || null, matchingMethod)}
        >
          <option value="">(none)</option>
          {tables.map((t) => (
            <option key={t.id} value={t.id}>{t.name}</option>
          ))}
        </select>
        <div className="matching-panel__inline-form">
          <input placeholder="New table name" value={newTableName} onChange={(e) => setNewTableName(e.target.value)} />
          <select value={newTableMethod} onChange={(e) => setNewTableMethod(e.target.value as 'standard' | 'five_star')}>
            <option value="standard">Standard</option>
            <option value="five_star">5-Star</option>
          </select>
          <button onClick={createTable}>Add</button>
        </div>
      </section>

      {matchingRuleTableId && (
        <section className="matching-panel__section">
          <label>Method</label>
          <div className="matching-panel__radio-row">
            <label>
              <input
                type="radio" name="matching-method" value="standard"
                checked={matchingMethod === 'standard'}
                onChange={() => applyMatching(matchingRuleTableId, 'standard')}
              />
              Standard
            </label>
            <label>
              <input
                type="radio" name="matching-method" value="five_star"
                checked={matchingMethod === 'five_star'}
                onChange={() => applyMatching(matchingRuleTableId, 'five_star')}
              />
              5-Star
            </label>
          </div>
        </section>
      )}

      {table && matchingMethod === 'standard' && (
        <section className="matching-panel__section">
          <label>Offsets (comma-separated, up to 3 per axis)</label>
          <input placeholder="horizontal" value={offsetsH} onChange={(e) => setOffsetsH(e.target.value)} />
          <input placeholder="vertical" value={offsetsV} onChange={(e) => setOffsetsV(e.target.value)} />
          <button onClick={saveOffsets}>Save Offsets</button>
        </section>
      )}

      {table && (
        <section className="matching-panel__section">
          <label>Stripe definitions</label>
          <ul className="matching-panel__list">
            {table.stripe_definitions.map((def) => (
              <li key={def.id}>
                <span>{def.name} (h={def.h_distance}, v={def.v_distance})</span>
                <button onClick={() => deleteStripeDefinition(def)}>Delete</button>
              </li>
            ))}
          </ul>
          <div className="matching-panel__inline-form">
            <input placeholder="Name" value={defForm.name} onChange={(e) => setDefForm({ ...defForm, name: e.target.value })} />
            <input placeholder="Origin X" value={defForm.origin_x} onChange={(e) => setDefForm({ ...defForm, origin_x: e.target.value })} />
            <input placeholder="Origin Y" value={defForm.origin_y} onChange={(e) => setDefForm({ ...defForm, origin_y: e.target.value })} />
            <input placeholder="H distance" value={defForm.h_distance} onChange={(e) => setDefForm({ ...defForm, h_distance: e.target.value })} />
            <input placeholder="V distance" value={defForm.v_distance} onChange={(e) => setDefForm({ ...defForm, v_distance: e.target.value })} />
            <button onClick={addStripeDefinition}>Add Stripe</button>
          </div>
        </section>
      )}

      {table && (
        <section className="matching-panel__section">
          <label>Stripe marks</label>
          <ul className="matching-panel__mark-list">
            {sortedMarks.map((mark) => (
              <li key={mark.id} className="matching-panel__mark-item">
                <span>#{mark.sequence} {mark.name}</span>
                <div className="matching-panel__mark-actions">
                  <button onClick={() => stepMark(mark.id, 'prev')}>Prev</button>
                  <button onClick={() => stepMark(mark.id, 'next')}>Next</button>
                  <button
                    disabled={!selectedPieceId}
                    onClick={() => selectedPieceId && onAssignMark(selectedPieceId, mark.id)}
                  >
                    Assign
                  </button>
                  <button onClick={() => deleteStripeMark(mark.id)}>Delete</button>
                </div>
              </li>
            ))}
          </ul>
          <div className="matching-panel__inline-form">
            <input placeholder="Name" value={markForm.name} onChange={(e) => setMarkForm({ ...markForm, name: e.target.value })} />
            <select
              value={markForm.stripe_definition_id}
              onChange={(e) => setMarkForm({ ...markForm, stripe_definition_id: e.target.value })}
            >
              <option value="">(no stripe)</option>
              {table.stripe_definitions.map((def) => (
                <option key={def.id} value={def.id}>{def.name}</option>
              ))}
            </select>
            <button onClick={addStripeMark}>Add Mark</button>
          </div>
        </section>
      )}

      <section className="matching-panel__section">
        <label>Validate bite</label>
        <div className="matching-panel__inline-form">
          <input placeholder="Bite length" value={biteLength} onChange={(e) => setBiteLength(e.target.value)} />
          <button onClick={runValidateBite}>Validate</button>
        </div>
        {biteResult && (
          biteResult.ok ? (
            <p className="matching-panel__ok">No bite-boundary violations.</p>
          ) : (
            <ul className="matching-panel__list">
              {biteResult.violations.map((v, i) => (
                <li key={i}>
                  Pieces cross a bite boundary at bite {v.bite_index_a} vs {v.bite_index_b} (mark {v.stripe_mark_id}).
                </li>
              ))}
            </ul>
          )
        )}
      </section>
    </div>
  )
}
