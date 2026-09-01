import { useState } from 'react'
import { api } from '../api/client'
import type { FolderOut, Page } from '../api/types'

interface Props {
  folder: FolderOut
  selectedId: string | null
  onSelect: (folder: FolderOut) => void
  depth: number
}

export function FolderTreeNode({ folder, selectedId, onSelect, depth }: Props) {
  const [expanded, setExpanded] = useState(false)
  const [children, setChildren] = useState<FolderOut[] | null>(null)
  const [loading, setLoading] = useState(false)

  const toggle = () => {
    if (!expanded && children === null) {
      setLoading(true)
      api
        .get<Page<FolderOut>>(`/folders/${folder.id}/children`)
        .then((page) => setChildren(page.items))
        .finally(() => setLoading(false))
    }
    setExpanded(!expanded)
  }

  return (
    <div>
      <div
        className={`folder-tree__row${selectedId === folder.id ? ' folder-tree__row--selected' : ''}`}
        style={{ paddingLeft: `${depth * 16}px` }}
      >
        <button className="folder-tree__toggle" onClick={toggle} aria-label={expanded ? 'Collapse' : 'Expand'}>
          {loading ? '…' : expanded ? '▾' : '▸'}
        </button>
        <button className="folder-tree__name" onClick={() => onSelect(folder)}>
          {folder.name}
        </button>
      </div>
      {expanded && children && children.length === 0 && (
        <div className="folder-tree__empty" style={{ paddingLeft: `${(depth + 1) * 16}px` }}>
          (no subfolders)
        </div>
      )}
      {expanded &&
        children?.map((child) => (
          <FolderTreeNode key={child.id} folder={child} selectedId={selectedId} onSelect={onSelect} depth={depth + 1} />
        ))}
    </div>
  )
}
