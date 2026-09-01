// Same local-dev auth stand-in as data-management-app (see that app's identity.ts and the
// backend's app/auth.py::dev_login docstring) -- type an identity instead of a real Entra ID
// login. marker-making-service forwards these headers through to data-platform-api untouched.

const STORAGE_KEY = 'zeus.dev-identity'

export interface DevIdentity {
  username: string
  org: string
}

const DEFAULT_IDENTITY: DevIdentity = { username: 'tester', org: 'DEV' }

export function loadIdentity(): DevIdentity {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return DEFAULT_IDENTITY
    const parsed = JSON.parse(raw)
    if (typeof parsed.username === 'string' && typeof parsed.org === 'string') {
      return parsed
    }
  } catch {
    // fall through to default
  }
  return DEFAULT_IDENTITY
}

export function saveIdentity(identity: DevIdentity): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(identity))
}
