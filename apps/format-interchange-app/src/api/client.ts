import { loadIdentity } from '../identity'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8002'

export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

interface RequestOptions {
  method?: string
  body?: unknown
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const identity = loadIdentity()
  const response = await fetch(`${BASE_URL}${path}`, {
    method: options.method ?? 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Dev-User': identity.username,
      'X-Dev-Org': identity.org,
    },
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  })

  const payload = await response.json().catch(() => null)

  if (!response.ok) {
    const message = payload?.error?.message ?? payload?.error?.detail ?? `Request failed with status ${response.status}`
    throw new ApiError(response.status, typeof message === 'string' ? message : JSON.stringify(message))
  }

  return payload as T
}

async function requestForm<T>(path: string, form: FormData): Promise<T> {
  const identity = loadIdentity()
  const response = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    // No Content-Type header here -- the browser sets multipart/form-data with the right
    // boundary itself; setting it manually strips that boundary and the server can't parse it.
    headers: { 'X-Dev-User': identity.username, 'X-Dev-Org': identity.org },
    body: form,
  })

  const payload = await response.json().catch(() => null)

  if (!response.ok) {
    const message = payload?.error?.message ?? payload?.error?.detail ?? `Request failed with status ${response.status}`
    throw new ApiError(response.status, typeof message === 'string' ? message : JSON.stringify(message))
  }

  return payload as T
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: 'POST', body }),
  postForm: <T>(path: string, form: FormData) => requestForm<T>(path, form),
}
