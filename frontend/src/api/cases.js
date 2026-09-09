// Talks to Yojit's case_management module.
// Base URL: http://127.0.0.1:8000  (proxied via vite as /api)
// All routes prefixed: /api/v1
// UPDATED to match Yojit's confirmed API_REFERENCE.md exactly.
//
// To go live: set MOCK_MODE = false in src/api/client.js

import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockCases } from '../mockData'

// GET /api/v1/cases — List all cases (paginated)
export async function listCases(page = 1, pageSize = 20) {
  if (MOCK_MODE) {
    await fakeDelay()
    return mockCases
  }
  const res = await apiClient.get('/v1/cases', {
    params: { page, page_size: pageSize }
  })
  return res.data
}

// GET /api/v1/cases/{case_id} — Get one case + its evidence
export async function getCase(caseId) {
  if (MOCK_MODE) {
    await fakeDelay()
    return mockCases.find((c) => c.id === caseId) ?? null
  }
  const res = await apiClient.get(`/v1/cases/${caseId}`)
  return res.data
}

// POST /api/v1/cases — Create a new case
export async function createCase(payload) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { id: `CSIA-2026-${Math.floor(Math.random() * 9000 + 1000)}`, ...payload }
  }
  const res = await apiClient.post('/v1/cases', payload)
  return res.data
}

// PUT /api/v1/cases/{case_id} — Update a case
export async function updateCase(caseId, payload) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { id: caseId, ...payload }
  }
  const res = await apiClient.put(`/v1/cases/${caseId}`, payload)
  return res.data
}

// DELETE /api/v1/cases/{case_id} — Delete a case and its evidence
export async function deleteCase(caseId) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { deleted: true }
  }
  const res = await apiClient.delete(`/v1/cases/${caseId}`)
  return res.data
}

// POST /api/v1/cases/{case_id}/evidence — Attach evidence to a case
export async function attachEvidence(caseId, payload) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { case_id: caseId, ...payload }
  }
  const res = await apiClient.post(`/v1/cases/${caseId}/evidence`, payload)
  return res.data
}

// GET /api/v1/evidence/{evidence_id} — Get a single evidence item
export async function getEvidence(evidenceId) {
  if (MOCK_MODE) {
    await fakeDelay()
    return null
  }
  const res = await apiClient.get(`/v1/evidence/${evidenceId}`)
  return res.data
}

// GET /api/v1/health — Health check
export async function healthCheck() {
  const res = await apiClient.get('/v1/health')
  return res.data
}
