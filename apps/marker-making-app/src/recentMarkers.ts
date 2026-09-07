// File metadata / recent files (Sec 1.11): "quick-reopen list of the 5 most recently opened
// files." No server-side concept of this exists (or should -- it's a per-browser convenience,
// not shared state), so it's local-only, same localStorage convention as identity.ts.

const STORAGE_KEY = 'zeus.marker-picker.recent'
const MAX_RECENT = 5

export interface RecentMarker {
  id: string
  markerCode: string
}

export function loadRecentMarkers(): RecentMarker[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    if (Array.isArray(parsed)) return parsed
  } catch {
    // fall through to empty
  }
  return []
}

export function pushRecentMarker(marker: RecentMarker): void {
  try {
    const existing = loadRecentMarkers().filter((m) => m.id !== marker.id)
    const updated = [marker, ...existing].slice(0, MAX_RECENT)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
  } catch {
    // best-effort only -- a full/blocked localStorage shouldn't break opening a marker
  }
}
