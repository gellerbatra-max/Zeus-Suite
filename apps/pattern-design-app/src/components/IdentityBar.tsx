import { useState } from 'react'
import { loadIdentity, saveIdentity } from '../identity'

export function IdentityBar() {
  const [identity, setIdentity] = useState(loadIdentity())
  const [editing, setEditing] = useState(false)

  const apply = () => {
    saveIdentity(identity)
    setEditing(false)
  }

  return (
    <div className="identity-bar">
      <div className="identity-bar__badge" title="Local-dev identity stand-in for real Entra ID SSO, forwarded through to data-platform-api">
        DEV AUTH
      </div>
      {editing ? (
        <>
          <label>
            User
            <input value={identity.username} onChange={(e) => setIdentity({ ...identity, username: e.target.value })} />
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
            <strong>{identity.username}</strong> @ {identity.org}
          </span>
          <button onClick={() => setEditing(true)}>Switch identity</button>
        </>
      )}
    </div>
  )
}
