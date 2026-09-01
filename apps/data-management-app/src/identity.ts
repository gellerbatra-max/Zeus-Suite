// Section 5.1's real Entra ID login is not available locally (see the backend's
// app/auth.py::dev_login docstring) -- this stands in for it, letting a tester type an identity
// instead of signing in through a real OIDC redirect. Every API call carries these as
// X-Dev-User / X-Dev-Org headers; the backend's dev-stub auth trusts them outright.

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
