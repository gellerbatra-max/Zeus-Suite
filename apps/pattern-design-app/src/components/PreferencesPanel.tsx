import type { Preferences } from '../preferences'
import { mmToDisplay, displayToMm } from '../preferences'

interface Props {
  preferences: Preferences
  onChange: (next: Preferences) => void
}

export function PreferencesPanel({ preferences, onChange }: Props) {
  const set = <K extends keyof Preferences>(key: K, value: Preferences[K]) =>
    onChange({ ...preferences, [key]: value })

  const gridSpacingDisplay = mmToDisplay(preferences.gridSpacingMm, preferences.displayUnit)

  return (
    <div className="preferences-panel">
      <div className="shape-tools__group">
        <span className="hint">Units:</span>
        <select value={preferences.displayUnit} onChange={(e) => set('displayUnit', e.target.value as Preferences['displayUnit'])}>
          <option value="mm">mm</option>
          <option value="cm">cm</option>
          <option value="in">in</option>
        </select>
      </div>
      <div className="shape-tools__group">
        <span className="hint">Grid spacing:</span>
        <input
          type="number"
          min="1"
          value={Math.round(gridSpacingDisplay * 100) / 100}
          onChange={(e) => set('gridSpacingMm', displayToMm(Number(e.target.value), preferences.displayUnit))}
          style={{ width: 64 }}
        />
        <span className="hint">{preferences.displayUnit}</span>
      </div>
      <label className="grading-tools__checkbox">
        <input type="checkbox" checked={preferences.snapToGrid} onChange={(e) => set('snapToGrid', e.target.checked)} />
        Snap to grid
      </label>
      <label className="grading-tools__checkbox">
        <input
          type="checkbox"
          checked={preferences.autosaveEnabled}
          onChange={(e) => set('autosaveEnabled', e.target.checked)}
        />
        Autosave every
      </label>
      <input
        type="number"
        min="10"
        value={preferences.autosaveIntervalSec}
        onChange={(e) => set('autosaveIntervalSec', Number(e.target.value))}
        disabled={!preferences.autosaveEnabled}
        style={{ width: 56 }}
      />
      <span className="hint">sec</span>
      <div className="shape-tools__group">
        <span className="hint">Piece color:</span>
        <input type="color" value={preferences.pieceStrokeColor} onChange={(e) => set('pieceStrokeColor', e.target.value)} />
      </div>
      <div className="shape-tools__group">
        <span className="hint">Background:</span>
        <input type="color" value={preferences.backgroundColor} onChange={(e) => set('backgroundColor', e.target.value)} />
      </div>
    </div>
  )
}
