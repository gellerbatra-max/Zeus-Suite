import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import { loadIdentity, saveIdentity } from '../identity'
import type { MeOut } from '../api/types'

export function IdentityBar() {
  const [identity, setIdentity] = useState(loadIdentity())
  const [me, setMe] = useState<MeOut | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [editing, setEditing] = useState(false)

  const refresh = () => {
    api
      .get<MeOut>('/me')
      .then((result) => {
        setMe(result)
        setError(null)
      })
      .catch((err) => {
        setMe(null)
        setError(err instanceof ApiError ? err.message : 'Could not reach the API.')
      })
  }

  useEffect(refresh, [])

  const apply = () => {
    saveIdentity(identity)
    setEditing(false)
    refresh()
  }

  return (
    <div className="identity-bar">
      <div className="identity-bar__badge" title="Local-dev identity stand-in for real Entra ID SSO">
        DEV AUTH
      </div>
      {editing ? (
        <>
          <label>
            User
            <input
              value={identity.username}
              onChange={(e) => setIdentity({ ...identity, username: e.target.value })}
            />
          </label>
          <label>
            Org
            <input value={identity.org} onChange={(e) => setIdentity({ ...identity, org: e.target.value })} />
          </label>
          <button onClick={apply}>Apply</button>
        </>
      ) : (
        <>
          <span>
            <strong>{me?.full_name ?? identity.username}</strong> @ {identity.org}
          </span>
          <button onClick={() => setEditing(true)}>Switch identity</button>
        </>
      )}
      {me && <span className="identity-bar__permissions">{me.permissions.length} permissions</span>}
      {error && <span className="identity-bar__error">{error}</span>}
    </div>
  )
}
