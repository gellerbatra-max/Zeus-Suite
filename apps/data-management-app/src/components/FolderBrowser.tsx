import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { FolderTreeNode } from './FolderTreeNode'
import type { FolderContentItem, FolderOut, Page } from '../api/types'

interface Props {
  onViewCrossReference: (entityType: string, id: string) => void
}

export function FolderBrowser({ onViewCrossReference }: Props) {
  const [roots, setRoots] = useState<FolderOut[]>([])
  const [selected, setSelected] = useState<FolderOut | null>(null)
  const [contents, setContents] = useState<FolderContentItem[]>([])
  const [newFolderName, setNewFolderName] = useState('')
  const [error, setError] = useState<string | null>(null)

  const loadRoots = () => {
    api
      .get<Page<FolderOut>>('/folders')
      .then((page) => setRoots(page.items))
      .catch((err) => setError(err.message))
  }

  useEffect(loadRoots, [])

  const loadContents = (folder: FolderOut) => {
    setSelected(folder)
    api
      .get<Page<FolderContentItem>>(`/folders/${folder.id}/contents`)
      .then((page) => setContents(page.items))
      .catch((err) => setError(err.message))
  }

  const createFolder = () => {
    if (!newFolderName.trim()) return
    api
      .post<FolderOut>('/folders', { parent_id: selected?.id ?? null, name: newFolderName.trim() })
      .then(() => {
        setNewFolderName('')
        setError(null)
        // A full root-list reload is the simplest correct refresh here -- a new subfolder's
        // parent may be several levels deep inside the tree's own lazily-loaded children, so
        // there's no single already-loaded list to patch in place.
        loadRoots()
      })
      .catch((err) => setError(err.message))
  }

  const breadcrumbs = selected ? selected.path.split('/').filter(Boolean) : []

  return (
    <div className="browser">
      <div className="browser__tree">
        <h3>Folders</h3>
        {roots.map((folder) => (
          <FolderTreeNode key={folder.id} folder={folder} selectedId={selected?.id ?? null} onSelect={loadContents} depth={0} />
        ))}
        <div className="browser__new-folder">
          <input
            placeholder={selected ? `New subfolder of ${selected.name}` : 'New root folder'}
            value={newFolderName}
            onChange={(e) => setNewFolderName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && createFolder()}
          />
          <button onClick={createFolder}>Create folder</button>
        </div>
      </div>

      <div className="browser__contents">
        {selected ? (
          <>
            <div className="browser__breadcrumb">
              {breadcrumbs.map((segment, i) => (
                <span key={i}>
                  {i > 0 && ' / '}
                  {segment}
                </span>
              ))}
            </div>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Code</th>
                  <th>Updated</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {contents.length === 0 && (
                  <tr>
                    <td colSpan={4} className="data-table__empty">
                      This folder is empty.
                    </td>
                  </tr>
                )}
                {contents.map((item) => (
                  <tr key={`${item.entity_type}-${item.id}`}>
                    <td>
                      <span className="badge">{item.entity_type}</span>
                    </td>
                    <td>{item.code}</td>
                    <td>{new Date(item.updated_at).toLocaleString()}</td>
                    <td>
                      <button onClick={() => onViewCrossReference(item.entity_type, item.id)}>Cross-references</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        ) : (
          <p className="browser__hint">Select a folder to browse its contents, or create one to get started.</p>
        )}
      </div>
      {error && <p className="error-text">{error}</p>}
    </div>
  )
}
