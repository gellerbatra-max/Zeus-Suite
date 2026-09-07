import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { MaterialSummaryOut } from '../api/types'

interface Props {
  markerId: string
  hasOrder: boolean
  onTargetLengthChanged: (targetLength: number | null) => void
}

function errMessage(err: unknown): string {
  return err instanceof ApiError ? err.message : String(err)
}

export function MaterialPanel({ markerId, hasOrder, onTargetLengthChanged }: Props) {
  const [summary, setSummary] = useState<MaterialSummaryOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [plyCount, setPlyCount] = useState('')
  const [weightPerArea, setWeightPerArea] = useState('')
  const [targetLength, setTargetLength] = useState('')
  const [targetUtilization, setTargetUtilization] = useState('')
  const [targetEfficiency, setTargetEfficiency] = useState('')
  const [requiredLength, setRequiredLength] = useState<number | null>(null)
  const [weightResult, setWeightResult] = useState<number | null>(null)

  const refresh = (s: MaterialSummaryOut) => {
    setSummary(s)
    setPlyCount(s.ply_count != null ? String(s.ply_count) : '')
    setWeightPerArea(s.fabric_weight_per_unit_area != null ? String(s.fabric_weight_per_unit_area) : '')
    setTargetLength(s.target_length != null ? String(s.target_length) : '')
    setTargetUtilization(s.target_utilization_pct != null ? String(s.target_utilization_pct) : '')
    onTargetLengthChanged(s.target_length)
  }

  useEffect(() => {
    api
      .get<MaterialSummaryOut>(`/markers/${markerId}/material/summary`)
      .then(refresh)
      .catch((err) => setError(errMessage(err)))
  }, [markerId])

  const savePlyAndWeight = async () => {
    setError(null)
    try {
      const updated = await api.patch<MaterialSummaryOut>(`/markers/${markerId}/material`, {
        ply_count: plyCount === '' ? null : Number(plyCount),
        fabric_weight_per_unit_area: weightPerArea === '' ? null : Number(weightPerArea),
      })
      refresh(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const saveTargets = async () => {
    setError(null)
    try {
      const updated = await api.patch<MaterialSummaryOut>(`/markers/${markerId}/material/target`, {
        target_length: targetLength === '' ? null : Number(targetLength),
        target_utilization_pct: targetUtilization === '' ? null : Number(targetUtilization),
      })
      refresh(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const applyComputed = async () => {
    setError(null)
    try {
      const updated = await api.post<MaterialSummaryOut>(`/markers/${markerId}/material/apply-computed`)
      refresh(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const calculateRequiredLength = async () => {
    if (targetEfficiency === '') return
    setError(null)
    try {
      const result = await api.post<{ required_length: number }>(`/markers/${markerId}/material/required-length`, {
        target_efficiency_pct: Number(targetEfficiency),
      })
      setRequiredLength(result.required_length)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const calculateWeight = async () => {
    setError(null)
    try {
      const result = await api.post<{ weight: number }>(`/markers/${markerId}/material/weight`, {})
      setWeightResult(result.weight)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  if (!summary) {
    return (
      <div className="material-panel">
        <h3>Material</h3>
        {error && <p className="error-text">{error}</p>}
      </div>
    )
  }

  return (
    <div className="material-panel">
      <h3>Material</h3>
      {error && <p className="error-text">{error}</p>}

      <section className="material-panel__section">
        <label>Live (from current placements)</label>
        <ul className="material-panel__readout">
          <li>Total piece area: {summary.computed_total_piece_area ?? '—'}</li>
          <li>Total perimeter: {summary.computed_total_perimeter ?? '—'}</li>
          <li>Marker length needed: {summary.computed_marker_length ?? '—'}</li>
          <li>Utilization: {summary.computed_utilization_pct != null ? `${summary.computed_utilization_pct}%` : '—'}</li>
        </ul>
        <button onClick={applyComputed} disabled={summary.computed_marker_length == null}>
          Apply Computed Length &amp; Utilization
        </button>
      </section>

      <section className="material-panel__section">
        <label>Stored on marker</label>
        <ul className="material-panel__readout">
          <li>Fabric width: {summary.fabric_width ?? '—'}</li>
          <li>Marker length: {summary.marker_length ?? '—'}</li>
          <li>Utilization: {summary.utilization_pct != null ? `${summary.utilization_pct}%` : '—'}</li>
        </ul>
        <div className="material-panel__inline-form">
          <input placeholder="Ply count" value={plyCount} onChange={(e) => setPlyCount(e.target.value)} />
          <input
            placeholder="Weight / unit area"
            value={weightPerArea}
            onChange={(e) => setWeightPerArea(e.target.value)}
          />
          <button onClick={savePlyAndWeight}>Save</button>
        </div>
      </section>

      <section className="material-panel__section">
        <label>Target (order){!hasOrder && ' — no linked order'}</label>
        <div className="material-panel__inline-form">
          <input
            placeholder="Target length"
            value={targetLength}
            onChange={(e) => setTargetLength(e.target.value)}
            disabled={!hasOrder}
          />
          <input
            placeholder="Target utilization %"
            value={targetUtilization}
            onChange={(e) => setTargetUtilization(e.target.value)}
            disabled={!hasOrder}
          />
          <button onClick={saveTargets} disabled={!hasOrder}>
            Save
          </button>
        </div>
      </section>

      <section className="material-panel__section">
        <label>Calculate Efficiency &amp; Marker Length</label>
        <div className="material-panel__inline-form">
          <input
            placeholder="Target efficiency %"
            value={targetEfficiency}
            onChange={(e) => setTargetEfficiency(e.target.value)}
          />
          <button onClick={calculateRequiredLength}>Calculate</button>
        </div>
        {requiredLength != null && <p className="material-panel__result">Required length: {requiredLength}</p>}
      </section>

      <section className="material-panel__section">
        <label>Calculate Material Weight</label>
        <p className="hint">Uses the ply count / weight-per-area / length saved above.</p>
        <button onClick={calculateWeight}>Calculate</button>
        {weightResult != null && <p className="material-panel__result">Weight: {weightResult}</p>}
      </section>
    </div>
  )
}
