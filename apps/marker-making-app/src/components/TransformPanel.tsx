import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { ChangeWidthOut, TransformSettingsOut, WorkspaceOut } from '../api/types'

interface Props {
  markerId: string
  hasOrder: boolean
  onFabricWidthChanged: (fabricWidth: number | null) => void
  onWorkspaceApplied: (workspace: WorkspaceOut) => void
}

function errMessage(err: unknown): string {
  return err instanceof ApiError ? err.message : String(err)
}

export function TransformPanel({ markerId, hasOrder, onFabricWidthChanged, onWorkspaceApplied }: Props) {
  const [settings, setSettings] = useState<TransformSettingsOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [fabricWidthInput, setFabricWidthInput] = useState('')
  const [shrinkX, setShrinkX] = useState('')
  const [shrinkY, setShrinkY] = useState('')

  const refresh = (s: TransformSettingsOut) => {
    setSettings(s)
    setFabricWidthInput(s.fabric_width != null ? String(s.fabric_width) : '')
    setShrinkX(s.shrink_x_pct != null ? String(s.shrink_x_pct) : '')
    setShrinkY(s.shrink_y_pct != null ? String(s.shrink_y_pct) : '')
    onFabricWidthChanged(s.fabric_width)
  }

  useEffect(() => {
    api
      .get<TransformSettingsOut>(`/markers/${markerId}/transform/settings`)
      .then(refresh)
      .catch((err) => setError(errMessage(err)))
  }, [markerId])

  const changeWidth = async () => {
    if (fabricWidthInput === '') return
    setError(null)
    try {
      const result = await api.post<ChangeWidthOut>(`/markers/${markerId}/transform/change-width`, {
        fabric_width: Number(fabricWidthInput),
      })
      onFabricWidthChanged(result.fabric_width)
      setSettings((prev) => (prev ? { ...prev, fabric_width: result.fabric_width } : prev))
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const saveShrinkStretch = async () => {
    setError(null)
    try {
      const updated = await api.patch<TransformSettingsOut>(`/markers/${markerId}/transform/shrink-stretch`, {
        shrink_x_pct: shrinkX === '' ? null : Number(shrinkX),
        shrink_y_pct: shrinkY === '' ? null : Number(shrinkY),
      })
      refresh(updated)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const applyShrinkStretch = async () => {
    setError(null)
    try {
      const workspace = await api.post<WorkspaceOut>(`/markers/${markerId}/transform/apply-shrink-stretch`)
      onWorkspaceApplied(workspace)
    } catch (err) {
      setError(errMessage(err))
    }
  }

  if (!settings) {
    return (
      <div className="transform-panel">
        <h3>Transform</h3>
        {error && <p className="error-text">{error}</p>}
      </div>
    )
  }

  return (
    <div className="transform-panel">
      <h3>Transform</h3>
      {error && <p className="error-text">{error}</p>}

      <section className="transform-panel__section">
        <label>Change Width of Marker</label>
        <p className="hint">Does not auto-rearrange pieces — resize the fabric-width axis only.</p>
        <div className="transform-panel__inline-form">
          <input placeholder="Fabric width" value={fabricWidthInput} onChange={(e) => setFabricWidthInput(e.target.value)} />
          <button onClick={changeWidth}>Change Width</button>
        </div>
      </section>

      <section className="transform-panel__section">
        <label>Shrink / Stretch (order){!hasOrder && ' — no linked order'}</label>
        <div className="transform-panel__inline-form">
          <input placeholder="Shrink X %" value={shrinkX} onChange={(e) => setShrinkX(e.target.value)} disabled={!hasOrder} />
          <input placeholder="Shrink Y %" value={shrinkY} onChange={(e) => setShrinkY(e.target.value)} disabled={!hasOrder} />
          <button onClick={saveShrinkStretch} disabled={!hasOrder}>
            Save
          </button>
        </div>
        <p className="hint">
          Applies once to current placements — clicking Apply twice double-scales, there's no
          "already applied" tracking.
        </p>
        <button onClick={applyShrinkStretch} disabled={!hasOrder || (settings.shrink_x_pct == null && settings.shrink_y_pct == null)}>
          Apply to Placements
        </button>
      </section>
    </div>
  )
}
