import { useState } from 'react'
import { api, ApiError } from '../api/client'
import type { MigrationBatchOut, MigrationItemOut } from '../api/types'
import { MigrationCanvas } from './MigrationCanvas'

// The Legacy Migration batch pipeline + Migration Viewer (format_interchange_plan.md Sec 2,
// Steps 3-4 of Sec 7). Unlike Export/Import above, this is a multi-step workflow (create batch ->
// run -> triage each item -> commit), so it gets its own component rather than living inline in
// App.tsx.

async function refreshBatch(batchId: string): Promise<MigrationBatchOut> {
  return api.get<MigrationBatchOut>(`/migration/batches/${batchId}`)
}

async function refreshItems(batchId: string): Promise<MigrationItemOut[]> {
  return api.get<MigrationItemOut[]>(`/migration/batches/${batchId}/items`)
}

export function MigrationPanel() {
  const [files, setFiles] = useState<FileList | null>(null)
  const [sourceSystem, setSourceSystem] = useState('Legacy AccuMark Library')
  const [targetCollection, setTargetCollection] = useState('')
  const [autoSortFlagged, setAutoSortFlagged] = useState(true)
  const [metadataByFilename, setMetadataByFilename] = useState('{}')
  const [creating, setCreating] = useState(false)
  const [running, setRunning] = useState(false)
  const [committing, setCommitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [batch, setBatch] = useState<MigrationBatchOut | null>(null)
  const [items, setItems] = useState<MigrationItemOut[]>([])
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null)

  const [resolveMetadata, setResolveMetadata] = useState('{}')
  const [resolveFile, setResolveFile] = useState<File | null>(null)
  const [blockNote, setBlockNote] = useState('')
  const [itemActionBusy, setItemActionBusy] = useState(false)

  const selectedItem = items.find((i) => i.id === selectedItemId) ?? null

  const createBatch = async () => {
    if (!files || files.length === 0) return
    setCreating(true)
    setError(null)
    try {
      const form = new FormData()
      for (const file of Array.from(files)) form.append('files', file)
      form.append(
        'options',
        JSON.stringify({
          source_system: sourceSystem,
          auto_sort_flagged: autoSortFlagged,
          target_collection: targetCollection.trim() || null,
        }),
      )
      const created = await api.postForm<MigrationBatchOut>('/migration/batches', form)
      setBatch(created)
      setItems(await refreshItems(created.id))
      setSelectedItemId(null)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setCreating(false)
    }
  }

  const runBatch = async () => {
    if (!batch) return
    setRunning(true)
    setError(null)
    try {
      let parsed: unknown = {}
      try {
        parsed = JSON.parse(metadataByFilename || '{}')
      } catch {
        throw new ApiError(400, 'metadata_by_filename must be valid JSON.')
      }
      const form = new FormData()
      form.append('metadata_by_filename', JSON.stringify(parsed))
      const updated = await api.postForm<MigrationBatchOut>(`/migration/batches/${batch.id}/run`, form)
      setBatch(updated)
      setItems(await refreshItems(batch.id))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setRunning(false)
    }
  }

  const commitBatch = async () => {
    if (!batch) return
    setCommitting(true)
    setError(null)
    try {
      const updated = await api.post<MigrationBatchOut>(`/migration/batches/${batch.id}/commit`)
      setBatch(updated)
      setItems(await refreshItems(batch.id))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setCommitting(false)
    }
  }

  const selectItem = (itemId: string) => {
    setSelectedItemId(itemId)
    setResolveMetadata('{}')
    setResolveFile(null)
    setBlockNote('')
  }

  const doResolve = async () => {
    if (!batch || !selectedItem) return
    setItemActionBusy(true)
    setError(null)
    try {
      let parsed: unknown = {}
      try {
        parsed = JSON.parse(resolveMetadata || '{}')
      } catch {
        throw new ApiError(400, 'legacy_metadata must be valid JSON.')
      }
      const form = new FormData()
      form.append('legacy_metadata', JSON.stringify(parsed))
      if (resolveFile) form.append('file', resolveFile)
      const updatedItem = await api.postForm<MigrationItemOut>(
        `/migration/batches/${batch.id}/items/${selectedItem.id}/resolve`,
        form,
      )
      setItems((prev) => prev.map((i) => (i.id === updatedItem.id ? updatedItem : i)))
      setBatch(await refreshBatch(batch.id))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setItemActionBusy(false)
    }
  }

  const doBlock = async () => {
    if (!batch || !selectedItem || !blockNote.trim()) return
    setItemActionBusy(true)
    setError(null)
    try {
      const form = new FormData()
      form.append('note', blockNote.trim())
      const updatedItem = await api.postForm<MigrationItemOut>(
        `/migration/batches/${batch.id}/items/${selectedItem.id}/block`,
        form,
      )
      setItems((prev) => prev.map((i) => (i.id === updatedItem.id ? updatedItem : i)))
      setBatch(await refreshBatch(batch.id))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setItemActionBusy(false)
    }
  }

  const doAcceptWarning = async () => {
    if (!batch || !selectedItem) return
    setItemActionBusy(true)
    setError(null)
    try {
      const updatedItem = await api.post<MigrationItemOut>(
        `/migration/batches/${batch.id}/items/${selectedItem.id}/accept-warning`,
      )
      setItems((prev) => prev.map((i) => (i.id === updatedItem.id ? updatedItem : i)))
      setBatch(await refreshBatch(batch.id))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setItemActionBusy(false)
    }
  }

  return (
    <section className="panel">
      <h2>Legacy Migration Batch</h2>

      <div className="field">
        <label htmlFor="mig-files">Source files (IGES)</label>
        <input id="mig-files" type="file" multiple accept=".igs,.iges" onChange={(e) => setFiles(e.target.files)} />
      </div>
      <div className="field">
        <label htmlFor="mig-source-system">Source system</label>
        <input id="mig-source-system" value={sourceSystem} onChange={(e) => setSourceSystem(e.target.value)} />
      </div>
      <div className="field">
        <label htmlFor="mig-target-collection">Target folder ID (target_collection)</label>
        <input
          id="mig-target-collection"
          value={targetCollection}
          onChange={(e) => setTargetCollection(e.target.value)}
          placeholder="uuid -- required to commit"
        />
      </div>
      <div className="checkbox-row">
        <label>
          <input type="checkbox" checked={autoSortFlagged} onChange={(e) => setAutoSortFlagged(e.target.checked)} />
          Auto-sort flagged items into Needs Review
        </label>
      </div>
      <button onClick={createBatch} disabled={creating || !files || files.length === 0}>
        {creating ? 'Creating…' : 'Create Batch'}
      </button>

      {batch && (
        <>
          <div className="field" style={{ marginTop: 16 }}>
            <label htmlFor="mig-metadata">Per-item legacy metadata (JSON: {'{'}"&lt;filename&gt;": {'{'}...{'}'}{'}'})</label>
            <textarea
              id="mig-metadata"
              rows={3}
              value={metadataByFilename}
              onChange={(e) => setMetadataByFilename(e.target.value)}
            />
          </div>
          <button onClick={runBatch} disabled={running}>
            {running ? 'Running…' : 'Run Batch'}
          </button>

          <div className="result" style={{ marginTop: 16 }}>
            <p>
              <span className="hint">Batch:</span> {batch.id}
            </p>
            <p>
              <span className={`badge badge--${batch.status}`}>{batch.status}</span> · {batch.item_count} item(s), chunk_count{' '}
              {batch.chunk_count}
            </p>
            <p>
              <span className="hint">Counts:</span>{' '}
              {Object.entries(batch.counts).map(([k, v]) => `${k}: ${v}`).join(', ') || 'none yet'}
            </p>
            <button onClick={commitBatch} disabled={committing || batch.commit_blocked_by.length > 0 || batch.item_count === 0}>
              {committing ? 'Committing…' : 'Commit Batch'}
            </button>
            {batch.commit_blocked_by.length > 0 && (
              <p className="hint">Blocked by: {batch.commit_blocked_by.join(', ')}</p>
            )}
          </div>
        </>
      )}

      {error && <p className="error-text">{error}</p>}

      {items.length > 0 && (
        <div style={{ marginTop: 16, overflowX: 'auto' }}>
          <table style={{ borderCollapse: 'collapse', width: '100%' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>File</th>
                <th style={{ textAlign: 'left' }}>Status</th>
                <th style={{ textAlign: 'left' }}>Needs review</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} style={{ borderTop: '1px solid #d8d8dc' }}>
                  <td>{item.source_style_ref}</td>
                  <td>
                    <span className={`badge badge--${item.status}`}>{item.status}</span>
                  </td>
                  <td>{item.needs_review ? 'Yes' : 'No'}</td>
                  <td>
                    <button onClick={() => selectItem(item.id)}>View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedItem && (
        <div className="panel" style={{ marginTop: 16 }}>
          <h3>{selectedItem.source_style_ref}</h3>
          <p>
            <span className={`badge badge--${selectedItem.status}`}>{selectedItem.status}</span>
            {selectedItem.block_note && <span className="hint"> — {selectedItem.block_note}</span>}
          </p>

          <MigrationCanvas converted={selectedItem.converted_geometry} sourceSummary={selectedItem.source_summary} diff={selectedItem.diff} />

          {selectedItem.findings.length > 0 && (
            <div>
              <span className="hint">Findings:</span>
              <ul>
                {selectedItem.findings.map((f) => (
                  <li key={f.id}>
                    <strong>[{f.severity}]</strong> {f.code}: {f.message} {f.resolved && '(resolved)'}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {selectedItem.diff?.perimeter_offset && (
            <p className="hint">
              Perimeter offset: {selectedItem.diff.perimeter_offset.magnitude_mm.toFixed(1)}mm @{' '}
              {selectedItem.diff.perimeter_offset.direction_deg.toFixed(0)}°
            </p>
          )}

          {selectedItem.status === 'converted_with_warning' && (
            <button onClick={doAcceptWarning} disabled={itemActionBusy}>
              Accept Warning
            </button>
          )}

          {(selectedItem.status === 'error' || selectedItem.status === 'blocked') && (
            <>
              <div className="field">
                <label htmlFor="resolve-metadata">Corrected legacy metadata (JSON, merged into existing)</label>
                <textarea id="resolve-metadata" rows={3} value={resolveMetadata} onChange={(e) => setResolveMetadata(e.target.value)} />
              </div>
              <div className="field">
                <label htmlFor="resolve-file">Replacement source file (optional)</label>
                <input id="resolve-file" type="file" accept=".igs,.iges" onChange={(e) => setResolveFile(e.target.files?.[0] ?? null)} />
              </div>
              <button onClick={doResolve} disabled={itemActionBusy}>
                Resolve & Re-run
              </button>

              <div className="field" style={{ marginTop: 8 }}>
                <label htmlFor="block-note">Block with correction note</label>
                <input id="block-note" value={blockNote} onChange={(e) => setBlockNote(e.target.value)} />
              </div>
              <button onClick={doBlock} disabled={itemActionBusy || !blockNote.trim()}>
                Block
              </button>
            </>
          )}
        </div>
      )}
    </section>
  )
}
