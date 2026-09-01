import { useEffect, useRef, useState } from 'react'
import { api, ApiError } from '../api/client'
import type { NestingJobOut } from '../api/types'

interface Props {
  markerId: string
  orderId: string | null
}

const TERMINAL_STATUSES = new Set(['succeeded', 'failed', 'cancelled'])

export function NestingJobPanel({ markerId, orderId }: Props) {
  const [job, setJob] = useState<NestingJobOut | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [polling, setPolling] = useState(false)
  const intervalRef = useRef<number | null>(null)

  useEffect(() => {
    return () => {
      if (intervalRef.current !== null) window.clearInterval(intervalRef.current)
    }
  }, [])

  const poll = (jobId: string) => {
    setPolling(true)
    intervalRef.current = window.setInterval(async () => {
      try {
        const updated = await api.get<NestingJobOut>(`/nesting-jobs/${jobId}`)
        setJob(updated)
        if (TERMINAL_STATUSES.has(updated.status)) {
          if (intervalRef.current !== null) window.clearInterval(intervalRef.current)
          setPolling(false)
        }
      } catch (err) {
        if (intervalRef.current !== null) window.clearInterval(intervalRef.current)
        setPolling(false)
        setError(err instanceof ApiError ? err.message : String(err))
      }
    }, 1500)
  }

  const submit = async () => {
    if (!orderId) {
      setError('This marker has no linked order -- cannot submit a nesting job.')
      return
    }
    setError(null)
    try {
      const submitted = await api.post<NestingJobOut>('/nesting-jobs', { marker_id: markerId, order_id: orderId })
      setJob(submitted)
      poll(submitted.id)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    }
  }

  return (
    <div className="nesting-job-panel">
      <h3>Auto-Nest (Engine B)</h3>
      <p className="hint">
        Submits to the platform's async job queue and polls to completion. This slice proves the
        plumbing end-to-end; the result is still the platform's stub placeholder, not a real
        placement-producing solver.
      </p>
      <button onClick={submit} disabled={polling}>
        {polling ? 'Running…' : 'Submit Auto-Nest Job'}
      </button>
      {error && <p className="error-text">{error}</p>}
      {job && (
        <div className="nesting-job-panel__status">
          <p>
            Status: <span className={`badge badge--${job.status}`}>{job.status}</span>
          </p>
          {job.result_ref && <pre>{JSON.stringify(job.result_ref, null, 2)}</pre>}
          {job.error_detail && <p className="error-text">{job.error_detail}</p>}
        </div>
      )}
    </div>
  )
}
