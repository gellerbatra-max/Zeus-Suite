import { useState } from 'react'
import type { GradeRuleTable } from '../api/types'

interface Props {
  table: GradeRuleTable | null
  activeSizeStep: number | null
  onSetSizeRange: (sizeRange: string[], baseSize: string) => void
  onSetActiveSizeStep: (step: number | null) => void
  showGradeNest: boolean
  onToggleGradeNest: (show: boolean) => void
  disabled: boolean
}

// The parent remounts this component (via a `key` tied to the open piece) whenever a different
// piece is opened, rather than syncing sizeRangeText/baseSize from the `table` prop in an effect
// -- deriving local editable state from a prop belongs in initial state or a key-driven remount,
// not a setState-in-effect, which just triggers an extra render for the same result.
export function GradingTools({
  table,
  activeSizeStep,
  onSetSizeRange,
  onSetActiveSizeStep,
  showGradeNest,
  onToggleGradeNest,
  disabled,
}: Props) {
  const [sizeRangeText, setSizeRangeText] = useState(table ? table.size_range.join(',') : 'S,M,L,XL')
  const [baseSize, setBaseSize] = useState(table?.base_size ?? '')

  const parsedSizes = sizeRangeText
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)

  const applySizeRange = () => {
    if (parsedSizes.length < 2) return
    const resolvedBase = parsedSizes.includes(baseSize) ? baseSize : parsedSizes[0]
    onSetSizeRange(parsedSizes, resolvedBase)
  }

  const steps = table ? table.size_range.slice(0, -1).map((s, i) => `${s} → ${table.size_range[i + 1]}`) : []

  return (
    <div className="grading-tools">
      <span className="shape-tools__label">Grading:</span>
      <div className="shape-tools__group">
        <input
          value={sizeRangeText}
          onChange={(e) => setSizeRangeText(e.target.value)}
          placeholder="S,M,L,XL"
          aria-label="Size range"
          style={{ width: 140 }}
        />
        <select value={baseSize || parsedSizes[0] || ''} onChange={(e) => setBaseSize(e.target.value)}>
          {parsedSizes.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <span className="hint">base</span>
        <button onClick={applySizeRange} disabled={disabled || parsedSizes.length < 2}>
          Set Size Range
        </button>
      </div>
      {table && (
        <div className="shape-tools__group">
          <span className="hint">Step:</span>
          <select
            value={activeSizeStep ?? ''}
            onChange={(e) => onSetActiveSizeStep(e.target.value === '' ? null : Number(e.target.value))}
          >
            <option value="">Select…</option>
            {steps.map((label, i) => (
              <option key={i} value={i}>
                {label}
              </option>
            ))}
          </select>
          <label className="grading-tools__checkbox">
            <input type="checkbox" checked={showGradeNest} onChange={(e) => onToggleGradeNest(e.target.checked)} />
            Show grade nest
          </label>
        </div>
      )}
    </div>
  )
}
