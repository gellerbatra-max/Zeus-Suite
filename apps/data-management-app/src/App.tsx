import { useState } from 'react'
import { IdentityBar } from './components/IdentityBar'
import { FolderBrowser } from './components/FolderBrowser'
import { SearchPanel } from './components/SearchPanel'
import { CrossReferenceView } from './components/CrossReferenceView'
import { ActivityLogViewer } from './components/ActivityLogViewer'
import { ReportsPanel } from './components/ReportsPanel'

type Tab = 'browse' | 'search' | 'activity' | 'reports'

export default function App() {
  const [tab, setTab] = useState<Tab>('browse')
  const [crossRef, setCrossRef] = useState<{ entityType: string; id: string } | null>(null)
  const [activityPreset, setActivityPreset] = useState<{ entityType: string; entityId: string } | null>(null)

  const openCrossReference = (entityType: string, id: string) => setCrossRef({ entityType, id })

  const openActivityLog = (entityType: string, entityId: string) => {
    setActivityPreset({ entityType, entityId })
    setCrossRef(null)
    setTab('activity')
  }

  return (
    <div className="app">
      <header className="app__header">
        <h1>Zeus Suite — Data Management</h1>
        <IdentityBar />
      </header>

      <nav className="app__tabs">
        <button className={tab === 'browse' ? 'active' : ''} onClick={() => setTab('browse')}>
          Browse
        </button>
        <button className={tab === 'search' ? 'active' : ''} onClick={() => setTab('search')}>
          Search
        </button>
        <button className={tab === 'activity' ? 'active' : ''} onClick={() => setTab('activity')}>
          Activity Log
        </button>
        <button className={tab === 'reports' ? 'active' : ''} onClick={() => setTab('reports')}>
          Reports
        </button>
      </nav>

      <main className="app__main">
        {tab === 'browse' && <FolderBrowser onViewCrossReference={openCrossReference} />}
        {tab === 'search' && <SearchPanel onViewCrossReference={openCrossReference} />}
        {tab === 'activity' && (
          <ActivityLogViewer presetFilter={activityPreset} onClearPreset={() => setActivityPreset(null)} />
        )}
        {tab === 'reports' && <ReportsPanel />}
      </main>

      {crossRef && (
        <CrossReferenceView
          entityType={crossRef.entityType}
          entityId={crossRef.id}
          onClose={() => setCrossRef(null)}
          onViewActivityLog={openActivityLog}
          onViewCrossReference={openCrossReference}
        />
      )}
    </div>
  )
}
