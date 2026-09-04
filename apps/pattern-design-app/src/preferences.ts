// Preferences (pattern_design_plan.md Sec 4 Customization, Preferences & Workspace Setup --
// Gerber depth per the depth guidance). Unlike everything built in Phases 2.1-2.5, none of this
// lives in the geometry document: a preference is a per-operator UI setting, not piece data, so it
// belongs in localStorage (this browser, this person), the same scoping `identity.ts` already uses
// for the dev-auth stand-in. Nothing here is undoable and nothing round-trips through the platform.

export type LengthUnit = 'mm' | 'cm' | 'in'

export interface Preferences {
  displayUnit: LengthUnit
  gridSpacingMm: number
  snapToGrid: boolean
  autosaveEnabled: boolean
  autosaveIntervalSec: number
  pieceFillColor: string
  pieceStrokeColor: string
  backgroundColor: string
}

const STORAGE_KEY = 'zeus.pattern-design.preferences'

export const DEFAULT_PREFERENCES: Preferences = {
  displayUnit: 'mm',
  gridSpacingMm: 50,
  snapToGrid: false,
  autosaveEnabled: false,
  autosaveIntervalSec: 60,
  pieceFillColor: 'rgba(46,90,172,0.08)',
  pieceStrokeColor: '#2e5aac',
  backgroundColor: '#ffffff',
}

export function loadPreferences(): Preferences {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return DEFAULT_PREFERENCES
    return { ...DEFAULT_PREFERENCES, ...JSON.parse(raw) }
  } catch {
    return DEFAULT_PREFERENCES
  }
}

export function savePreferences(prefs: Preferences): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs))
  } catch {
    // Preferences are a convenience, not a correctness requirement -- a private-browsing tab or
    // full storage quota just means defaults are used again next load, not a broken app.
  }
}

// mm is the geometry document's fixed storage unit (Sec 3.3) -- these only affect what's typed
// into / displayed by the UI (Richpeace's "Length unit & precision setup").
const MM_PER_UNIT: Record<LengthUnit, number> = { mm: 1, cm: 10, in: 25.4 }

export function mmToDisplay(mm: number, unit: LengthUnit): number {
  return mm / MM_PER_UNIT[unit]
}

export function displayToMm(value: number, unit: LengthUnit): number {
  return value * MM_PER_UNIT[unit]
}

export function snapValue(mm: number, gridSpacingMm: number): number {
  if (gridSpacingMm <= 0) return mm
  return Math.round(mm / gridSpacingMm) * gridSpacingMm
}
