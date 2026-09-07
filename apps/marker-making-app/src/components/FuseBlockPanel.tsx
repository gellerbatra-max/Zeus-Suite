import { useEffect, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { BlockBufferRuleTableOut, FuseBlockOut } from '../api/types'
import type { CanvasPlacement } from './MarkerCanvas'

interface Props {
  markerId: string
  placements: CanvasPlacement[]
  selectedPieceId: string | null
  selectedPieceBlockBufferRuleNo: number | null
  onAssignBlockBufferRule: (pieceId: string, ruleNo: number | null) => void
  onFuseBlocksChanged: (blocks: FuseBlockOut[]) => void
  onRuleTablesChanged: (tables: BlockBufferRuleTableOut[]) => void
}

function errMessage(err: unknown): string {
  return err instanceof ApiError ? err.message : String(err)
}

export function FuseBlockPanel({
  markerId,
  placements,
  selectedPieceId,
  selectedPieceBlockBufferRuleNo,
  onAssignBlockBufferRule,
  onFuseBlocksChanged,
  onRuleTablesChanged,
}: Props) {
  const [ruleTables, setRuleTables] = useState<BlockBufferRuleTableOut[]>([])
  const [fuseBlocks, setFuseBlocks] = useState<FuseBlockOut[]>([])
  const [error, setError] = useState<string | null>(null)

  const [ruleForm, setRuleForm] = useState({
    name: '', rule_no: '', rule_type: 'block', mode: 'static',
    left_amt: '0', top_amt: '0', right_amt: '0', bottom_amt: '0',
  })

  const [draftPieceIds, setDraftPieceIds] = useState<string[]>([])
  const [blockAmount, setBlockAmount] = useState('0.5')
  const [reduceAmount, setReduceAmount] = useState('0')

  useEffect(() => {
    api
      .get<{ items: BlockBufferRuleTableOut[] }>('/block-buffer-rule-tables')
      .then((page) => {
        setRuleTables(page.items)
        onRuleTablesChanged(page.items)
      })
      .catch((err) => setError(errMessage(err)))
  }, [])

  useEffect(() => {
    api
      .get<FuseBlockOut[]>(`/markers/${markerId}/fuse-blocks`)
      .then((blocks) => {
        setFuseBlocks(blocks)
        onFuseBlocksChanged(blocks)
      })
      .catch((err) => setError(errMessage(err)))
  }, [markerId])

  const refreshFuseBlocks = (blocks: FuseBlockOut[]) => {
    setFuseBlocks(blocks)
    onFuseBlocksChanged(blocks)
  }

  const pieceCode = (pieceId: string) => placements.find((p) => p.pieceId === pieceId)?.pieceCode ?? pieceId

  const refreshRuleTables = (tables: BlockBufferRuleTableOut[]) => {
    setRuleTables(tables)
    onRuleTablesChanged(tables)
  }

  const createRuleTable = async () => {
    if (!ruleForm.name.trim() || !ruleForm.rule_no.trim()) return
    setError(null)
    try {
      const created = await api.post<BlockBufferRuleTableOut>('/block-buffer-rule-tables', {
        name: ruleForm.name.trim(),
        rule_no: Number(ruleForm.rule_no) || 0,
        rule_type: ruleForm.rule_type,
        mode: ruleForm.mode,
        left_amt: Number(ruleForm.left_amt) || 0,
        top_amt: Number(ruleForm.top_amt) || 0,
        right_amt: Number(ruleForm.right_amt) || 0,
        bottom_amt: Number(ruleForm.bottom_amt) || 0,
      })
      refreshRuleTables([...ruleTables, created])
      setRuleForm({ name: '', rule_no: '', rule_type: 'block', mode: 'static', left_amt: '0', top_amt: '0', right_amt: '0', bottom_amt: '0' })
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteRuleTable = async (id: string) => {
    setError(null)
    try {
      await api.delete(`/block-buffer-rule-tables/${id}`)
      refreshRuleTables(ruleTables.filter((r) => r.id !== id))
      if (selectedPieceId && ruleTables.find((r) => r.id === id)?.rule_no === selectedPieceBlockBufferRuleNo) {
        onAssignBlockBufferRule(selectedPieceId, null)
      }
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const addSelectedToDraft = () => {
    if (!selectedPieceId || draftPieceIds.includes(selectedPieceId)) return
    setDraftPieceIds((prev) => [...prev, selectedPieceId])
  }

  const removeFromDraft = (pieceId: string) => {
    setDraftPieceIds((prev) => prev.filter((id) => id !== pieceId))
  }

  const createFuseBlock = async () => {
    if (draftPieceIds.length === 0) return
    setError(null)
    try {
      const created = await api.post<FuseBlockOut>(`/markers/${markerId}/fuse-blocks`, {
        piece_ids: draftPieceIds, block_amount: Number(blockAmount) || 0, reduce_amount: Number(reduceAmount) || 0,
      })
      refreshFuseBlocks([...fuseBlocks, created])
      setDraftPieceIds([])
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const recomputeBounds = async (block: FuseBlockOut) => {
    setError(null)
    try {
      const updated = await api.patch<FuseBlockOut>(`/markers/${markerId}/fuse-blocks/${block.id}`, {
        piece_ids: block.piece_placement_ids,
      })
      refreshFuseBlocks(fuseBlocks.map((b) => (b.id === updated.id ? updated : b)))
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const updateFuseBlockAmounts = async (block: FuseBlockOut, blockAmt: number, reduceAmt: number) => {
    setError(null)
    try {
      const updated = await api.patch<FuseBlockOut>(`/markers/${markerId}/fuse-blocks/${block.id}`, {
        block_amount: blockAmt, reduce_amount: reduceAmt,
      })
      refreshFuseBlocks(fuseBlocks.map((b) => (b.id === updated.id ? updated : b)))
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteFuseBlock = async (id: string) => {
    setError(null)
    try {
      await api.delete(`/markers/${markerId}/fuse-blocks/${id}`)
      refreshFuseBlocks(fuseBlocks.filter((b) => b.id !== id))
    } catch (err) {
      setError(errMessage(err))
    }
  }

  const deleteAllFuseBlocks = async () => {
    setError(null)
    try {
      await api.delete(`/markers/${markerId}/fuse-blocks`)
      refreshFuseBlocks([])
    } catch (err) {
      setError(errMessage(err))
    }
  }

  return (
    <div className="fuse-block-panel">
      <h3>Fuse Blocking</h3>
      {error && <p className="error-text">{error}</p>}

      <section className="fuse-block-panel__section">
        <label>Block/Buffer rule tables</label>
        <ul className="fuse-block-panel__list">
          {ruleTables.map((r) => (
            <li key={r.id}>
              <span>
                #{r.rule_no} {r.name} ({r.rule_type}/{r.mode})
              </span>
              <button onClick={() => deleteRuleTable(r.id)}>Delete</button>
            </li>
          ))}
        </ul>
        <div className="matching-panel__inline-form">
          <input placeholder="Name" value={ruleForm.name} onChange={(e) => setRuleForm({ ...ruleForm, name: e.target.value })} />
          <input placeholder="Rule #" value={ruleForm.rule_no} onChange={(e) => setRuleForm({ ...ruleForm, rule_no: e.target.value })} />
          <select value={ruleForm.rule_type} onChange={(e) => setRuleForm({ ...ruleForm, rule_type: e.target.value })}>
            <option value="block">Block</option>
            <option value="buffer">Buffer</option>
          </select>
          <select value={ruleForm.mode} onChange={(e) => setRuleForm({ ...ruleForm, mode: e.target.value })}>
            <option value="static">Static</option>
            <option value="dynamic">Dynamic</option>
          </select>
        </div>
        <div className="matching-panel__inline-form">
          <input placeholder="L" value={ruleForm.left_amt} onChange={(e) => setRuleForm({ ...ruleForm, left_amt: e.target.value })} />
          <input placeholder="T" value={ruleForm.top_amt} onChange={(e) => setRuleForm({ ...ruleForm, top_amt: e.target.value })} />
          <input placeholder="R" value={ruleForm.right_amt} onChange={(e) => setRuleForm({ ...ruleForm, right_amt: e.target.value })} />
          <input placeholder="B" value={ruleForm.bottom_amt} onChange={(e) => setRuleForm({ ...ruleForm, bottom_amt: e.target.value })} />
          <button onClick={createRuleTable}>Add Rule</button>
        </div>
      </section>

      <section className="fuse-block-panel__section">
        <label>Selected piece's rule</label>
        <select
          disabled={!selectedPieceId}
          value={selectedPieceBlockBufferRuleNo ?? ''}
          onChange={(e) => {
            if (!selectedPieceId) return
            const value = e.target.value
            onAssignBlockBufferRule(selectedPieceId, value === '' ? null : Number(value))
          }}
        >
          <option value="">(none)</option>
          {ruleTables.map((r) => (
            <option key={r.id} value={r.rule_no}>#{r.rule_no} {r.name} ({r.rule_type})</option>
          ))}
        </select>
      </section>

      <section className="fuse-block-panel__section">
        <label>Fuse block draft</label>
        <ul className="fuse-block-panel__list">
          {draftPieceIds.map((id) => (
            <li key={id}>
              <span>{pieceCode(id)}</span>
              <button onClick={() => removeFromDraft(id)}>Remove</button>
            </li>
          ))}
        </ul>
        <div className="matching-panel__inline-form">
          <button disabled={!selectedPieceId || draftPieceIds.includes(selectedPieceId)} onClick={addSelectedToDraft}>
            Add Selected Piece
          </button>
          <input placeholder="Block amount" value={blockAmount} onChange={(e) => setBlockAmount(e.target.value)} />
          <input placeholder="Reduce amount" value={reduceAmount} onChange={(e) => setReduceAmount(e.target.value)} />
        </div>
        <button disabled={draftPieceIds.length === 0} onClick={createFuseBlock}>
          Create Fuse Block
        </button>
      </section>

      <section className="fuse-block-panel__section">
        <label>Fuse blocks</label>
        <ul className="fuse-block-panel__list fuse-block-panel__list--stacked">
          {fuseBlocks.map((block) => (
            <li key={block.id} className="fuse-block-panel__block-item">
              <span>{block.piece_placement_ids.map(pieceCode).join(', ')}</span>
              <span className="hint">
                block={block.block_amount} reduce={block.reduce_amount} notch={block.notch_depth.toFixed(2)}
              </span>
              <div className="fuse-block-panel__block-actions">
                <button onClick={() => recomputeBounds(block)}>Recompute Bounds</button>
                <button onClick={() => updateFuseBlockAmounts(block, Math.max(0, block.block_amount - 0.1), block.reduce_amount)}>
                  Block −
                </button>
                <button onClick={() => updateFuseBlockAmounts(block, block.block_amount + 0.1, block.reduce_amount)}>
                  Block +
                </button>
                <button onClick={() => updateFuseBlockAmounts(block, block.block_amount, Math.max(0, block.reduce_amount - 0.1))}>
                  Reduce −
                </button>
                <button onClick={() => updateFuseBlockAmounts(block, block.block_amount, block.reduce_amount + 0.1)}>
                  Reduce +
                </button>
                <button onClick={() => deleteFuseBlock(block.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
        <button disabled={fuseBlocks.length === 0} onClick={deleteAllFuseBlocks}>
          Delete All
        </button>
      </section>
    </div>
  )
}
