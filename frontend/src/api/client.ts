// All API calls go through /api, which Vite proxies to http://localhost:8000.
const BASE = '/api'

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init)
  if (res.status === 204) return undefined as T
  if (!res.ok) {
    const text = await res.text()
    throw new ApiError(res.status, text)
  }
  return res.json() as Promise<T>
}

export const get = <T>(path: string) => request<T>(path)

export const post = <T>(path: string, body: unknown) =>
  request<T>(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

export const del = (path: string) => request<void>(path, { method: 'DELETE' })
