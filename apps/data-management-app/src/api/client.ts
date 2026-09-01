import { loadIdentity } from '../identity'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export class ApiError extends Error {
  status: number
  code: string

  constructor(status: number, code: string, message: string) {
    super(message)
    this.status = status
    this.code = code
  }
}

interface RequestOptions {
  method?: string
  params?: Record<string, string | number | boolean | undefined | null>
  body?: unknown
  headers?: Record<string, string>
}

function buildQuery(params?: RequestOptions['params']): string {
  if (!params) return ''
  const usable = Object.entries(params).filter(([, v]) => v !== undefined && v !== null)
  if (usable.length === 0) return ''
  const search = new URLSearchParams()
  for (const [key, value] of usable) search.set(key, String(value))
  return `?${search.toString()}`
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const identity = loadIdentity()
  const response = await fetch(`${BASE_URL}${path}${buildQuery(options.params)}`, {
    method: options.method ?? 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Dev-User': identity.username,
      'X-Dev-Org': identity.org,
      ...options.headers,
    },
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  })

  if (response.status === 204) {
    return undefined as T
  }

  const payload = await response.json().catch(() => null)

  if (!response.ok) {
    const error = payload?.error
    throw new ApiError(
      response.status,
      error?.code ?? 'unknown_error',
      error?.message ?? `Request failed with status ${response.status}`,
    )
  }

  return payload as T
}

export const api = {
  get: <T>(path: string, params?: RequestOptions['params']) => request<T>(path, { params }),
  post: <T>(path: string, body?: unknown, headers?: Record<string, string>) =>
    request<T>(path, { method: 'POST', body, headers }),
  patch: <T>(path: string, body?: unknown, headers?: Record<string, string>) =>
    request<T>(path, { method: 'PATCH', body, headers }),
  del: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
}
