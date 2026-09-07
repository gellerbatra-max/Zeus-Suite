// Shape templates (pattern_design_plan.md Sec 4 Automation -- Richpeace's "Custom curve save &
// reuse" / "Motif Library: save a user-drawn shape as a named, reusable tool"). Scoped narrowly
// and honestly: a template is the perimeter's point sequence, centered on its own centroid so it
// can be dropped onto any piece regardless of where the original was drawn, saved to localStorage
// (per-operator, like preferences.ts, not per-piece geometry -- the whole point is reusing a shape
// *across* pieces). This is not a general command-recording macro system: Command objects
// (commands.ts) are closures, not serializable data, so "record every action and replay it" isn't
// something localStorage can hold across a page reload. Recording just the drawn point sequence
// sidesteps that entirely -- it's already plain, serializable {x,y} data.

import type { Point } from './api/types'

export interface ShapeTemplate {
  name: string
  points: { x: number; y: number; type: string }[]
}

const STORAGE_KEY = 'zeus.pattern-design.shape-templates'

function centroidOf(points: { x: number; y: number }[]): { x: number; y: number } {
  if (points.length === 0) return { x: 0, y: 0 }
  const sum = points.reduce((acc, p) => ({ x: acc.x + p.x, y: acc.y + p.y }), { x: 0, y: 0 })
  return { x: sum.x / points.length, y: sum.y / points.length }
}

export function loadTemplates(): ShapeTemplate[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function persist(templates: ShapeTemplate[]): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(templates))
  } catch {
    // Same as preferences.ts: a save that silently doesn't persist across reloads is an
    // acceptable degradation for a convenience feature, not worth surfacing as an app error.
  }
}

export function saveTemplate(name: string, perimeter: Point[]): ShapeTemplate[] {
  const center = centroidOf(perimeter)
  const template: ShapeTemplate = {
    name,
    points: perimeter.map((p) => ({ x: p.x - center.x, y: p.y - center.y, type: p.type })),
  }
  const existing = loadTemplates().filter((t) => t.name !== name)
  const updated = [...existing, template]
  persist(updated)
  return updated
}

export function deleteTemplate(name: string): ShapeTemplate[] {
  const updated = loadTemplates().filter((t) => t.name !== name)
  persist(updated)
  return updated
}

export function instantiateTemplate(template: ShapeTemplate): Point[] {
  return template.points.map((p) => ({ point_ref: crypto.randomUUID(), x: p.x, y: p.y, type: p.type }))
}
