// Mirrors apps/data-platform-api/app/schemas.py -- keep field names identical to the backend
// response shapes; this file has no logic, just the wire types this app consumes.

export interface WorkflowStatusOut {
  code: string
  label: string
}

export interface Page<T> {
  items: T[]
  page: number
  page_size: number
  total: number
}

export interface MeOut {
  id: string
  username: string
  full_name: string
  organization_id: string
  permissions: string[]
}

export interface FolderOut {
  id: string
  parent_id: string | null
  name: string
  path: string
  folder_type: string
  version: number
  created_at: string
  created_by: string
}

export interface FolderContentItem {
  entity_type: 'piece' | 'style' | 'marker' | 'order' | 'bundle'
  id: string
  code: string
  updated_at: string
}

export interface SearchResultRow {
  id: string
  code: string
  name: string
  folder_path: string | null
  workflow_status: string
  updated_at: string
}

export interface SearchResponse {
  results: Record<string, SearchResultRow[]>
  total_by_type: Record<string, number>
}

export interface SuggestResultRow {
  entity_type: string
  id: string
  code: string
  name: string
}

export interface CrossReferenceOut {
  entity_type: string
  id: string
  related: Record<string, SearchResultRow[]>
}

export interface AuditLogOut {
  id: number
  occurred_at: string
  user_id: string | null
  action: string
  entity_type: string
  entity_id: string | null
  result: 'success' | 'denied' | 'error'
  detail: string | null
  before_state: Record<string, unknown> | null
  after_state: Record<string, unknown> | null
}

export interface ReportDefinitionOut {
  code: string
  name: string
  entity_type: string
  description: string | null
}

export interface ReportRunOut {
  id: string
  report_code: string
  status: string
  result_inline: Record<string, unknown> | null
  requested_at: string
  completed_at: string | null
}

export const SEARCHABLE_ENTITY_TYPES = ['piece', 'style', 'marker', 'order', 'bundle'] as const
export type SearchableEntityType = (typeof SEARCHABLE_ENTITY_TYPES)[number]
