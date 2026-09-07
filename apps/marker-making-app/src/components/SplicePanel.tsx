import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { SpliceMarkOut, SpliceSettingsOut } from '../api/types'

interface Props {
  markerId: string
  onSpliceMarksChanged: (marks: SpliceMarkOut[]) => void
}

function errMessage(err: unknown): string {
  return err instanceof ApiError ? err.message : String(err)
}

export function SplicePanel({ markerId, onSpliceMarksChanged }: Props) {
  const [settings, setSettings] = useState<SpliceSettingsOut | null>(null)
  const [marks, setMarks] = useState<SpliceMarkOut[]>([])
  const [error, setError] = useState<string | null>(null)

  const [minLength, setMinLength] = useState('')
  const [maxLength, setMaxLength] = useState('')
  const [margin, setMargin] = useState('')
  const [separation, setSeparation] = useState('')
  const [rollLength, setRollLength] = useState('')

  const [manualStart, setManualStart] = useState('')
  const [manualEnd, setManualEnd] = useState('')
  const [manualRollId, setManualRollId] = useState('')

  const refreshMarks = (m: SpliceMarkOut[]) => {
    setMarks(m)
    onSpliceMarksChanged(m)
  }

  useEffect(() => {
    api
      .get<SpliceSettingsOut>(`/markers/${markerId}/splice/settings`)
      .then((s) => {
        setSettings(s)
        setMinLength(s.min_length != null ? String(s.min_length) : '')
        setMaxLength(s.max_length != null ? String(s.max_length) : '')
        setMargin(s.margin != null ? String(s.margin) : '')
        setSeparation(s.separation != null ? String(s.separation) : '')
      })
      .catch((err) => setError(errMessage(err)))
    api
      .get<SpliceMarkOut[]>(`/markers/${markerId}/splice-marks`)
      .then(refreshMarks)
      .catch((err) => setError(errMessage(err)))
  }, [markerId])

  const saveSettings = async () => {
    setError(null)
    try {
      const updated = await api.patch<SpliceSettingsOut>(`/markers/${markerId}/splice/settings`, {
        min_length: minLength === '' ? null : Number(minLength),
        max_length: maxLength === '' ? null : Number(maxLength),
        margin: margin === '' ? null : Number(margin),
        separation: separation === '' ? null : Number(separation),
      })
      setSettings(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const regenerateAuto = async () => {
    if (rollLength === '') return
    setError(null)
    try {
      const updated = await api.post<SpliceMarkOut[]>(`/markers/${markerId}/splice/auto`, {
        roll_length: Number(rollLength),
      })
      refreshMarks(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const addManualMark = async () => {
    if (manualStart === '' || manualEnd === '') return
    setError(null)
    try {
      const created = await api.post<SpliceMarkOut>(`/markers/${markerId}/splice-marks`, {
        start_x: Number(manualStart), end_x: Number(manualEnd), roll_id: manualRollId || null,
      })
      refreshMarks([...marks, created])
      setManualStart('')
      setManualEnd('')
      setManualRollId('')
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteMark = async (id: string) => {
    setError(null)
    try {
      await api.delete(`/splice-marks/${id}`)
      refreshMarks(marks.filter((m) => m.id !== id))
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteAll = async () => {
    setError(null)
    try {
      await api.delete(`/markers/${markerId}/splice-marks`)
      refreshMarks([])
    } catch (err) {
      setError(errMessage(err))
    }
  }

  if (!settings) {
    return (
      <div className="splice-panel">
        <h3>Splice Marks</h3>
        {error && <p className="error-text">{error}</p>}
      </div>
    )
  }

  return (
    <div className="splice-panel">
      <h3>Splice Marks</h3>
      {error && <p className="error-text">{error}</p>}

      <section className="splice-panel__section">
        <label>Splice settings</label>
        <div className="splice-panel__inline-form">
          <input placeholder="Min length" value={minLength} onChange={(e) => setMinLength(e.target.value)} />
          <input placeholder="Max length" value={maxLength} onChange={(e) => setMaxLength(e.target.value)} />
        </div>
        <div className="splice-panel__inline-form">
          <input placeholder="Margin" value={margin} onChange={(e) => setMargin(e.target.value)} />
          <input placeholder="Separation" value={separation} onChange={(e) => setSeparation(e.target.value)} />
          <button onClick={saveSettings}>Save</button>
        </div>
      </section>

      <section className="splice-panel__section">
        <label>Splice / Automatic</label>
        <p className="hint">No real fabric-roll data exists yet — enter the roll length by hand.</p>
        <div className="splice-panel__inline-form">
          <input placeholder="Roll length" value={rollLength} onChange={(e) => setRollLength(e.target.value)} />
          <button onClick={regenerateAuto}>Regenerate Auto Splices</button>
        </div>
      </section>

      <section className="splice-panel__section">
        <label>Add manual splice</label>
        <div className="splice-panel__inline-form">
          <input placeholder="Start" value={manualStart} onChange={(e) => setManualStart(e.target.value)} />
          <input placeholder="End" value={manualEnd} onChange={(e) => setManualEnd(e.target.value)} />
          <input placeholder="Roll id" value={manualRollId} onChange={(e) => setManualRollId(e.target.value)} />
        </div>
        <button onClick={addManualMark}>Add</button>
      </section>

      <section className="splice-panel__section">
        <label>Marks ({marks.length})</label>
        <ul className="splice-panel__list">
          {marks
            .slice()
            .sort((a, b) => a.start_x - b.start_x)
            .map((m) => (
              <li key={m.id}>
                <span>
                  {m.start_x.toFixed(2)}–{m.end_x.toFixed(2)} ({m.source}
                  {m.roll_id ? `, ${m.roll_id}` : ''})
                </span>
                <button onClick={() => deleteMark(m.id)}>Delete</button>
              </li>
            ))}
        </ul>
        <button disabled={marks.length === 0} onClick={deleteAll}>
          Delete All
        </button>
      </section>
    </div>
  )
}
