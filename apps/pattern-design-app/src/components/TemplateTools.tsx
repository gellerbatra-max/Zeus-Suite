import { useState } from 'react'
import type { ShapeTemplate } from '../templates'

interface Props {
  templates: ShapeTemplate[]
  canSave: boolean
  onSave: (name: string) => void
  onApply: (template: ShapeTemplate) => void
  onDelete: (name: string) => void
}

// Richpeace's Motif Library / Custom curve save & reuse (Sec 4 Automation): save the current
// perimeter as a named, reusable shape, then drop it onto any piece later -- see templates.ts for
// why this is scoped to perimeter shapes rather than a general macro-record system.
export function TemplateTools({ templates, canSave, onSave, onApply, onDelete }: Props) {
  const [name, setName] = useState('')
  const [selected, setSelected] = useState('')

  const save = () => {
    if (!name.trim()) return
    onSave(name.trim())
    setName('')
  }

  return (
    <div className="shape-tools">
      <span className="shape-tools__label">Templates:</span>
      <div className="shape-tools__group">
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Template name" style={{ width: 120 }} />
        <button onClick={save} disabled={!canSave || !name.trim()}>
          Save Current Shape
        </button>
      </div>
      <div className="shape-tools__group">
        <select value={selected} onChange={(e) => setSelected(e.target.value)}>
          <option value="">Select…</option>
          {templates.map((t) => (
            <option key={t.name} value={t.name}>
              {t.name} ({t.points.length} pt)
            </option>
          ))}
        </select>
        <button
          disabled={!selected}
          onClick={() => {
            const t = templates.find((tpl) => tpl.name === selected)
            if (t) onApply(t)
          }}
        >
          Apply
        </button>
        <button
          disabled={!selected}
          onClick={() => {
            onDelete(selected)
            setSelected('')
          }}
        >
          Delete
        </button>
      </div>
    </div>
  )
}
