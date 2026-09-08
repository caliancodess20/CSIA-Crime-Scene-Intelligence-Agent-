// Talks to Yojit's case_management module (backend/app/case_management/routes.py).
// Endpoints below are guesses based on "CRUD: create, update, retrieve a case" +
// "search + filter" in the file structure doc — confirm exact paths with Yojit
// and adjust this file only. Nothing else in the app should import axios directly.

import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockCases } from '../mockData'

export async function listCases() {
  if (MOCK_MODE) {
    await fakeDelay()
    return mockCases
  }
  const res = await apiClient.get('/cases')
  return res.data
}

export async function getCase(caseId) {
  if (MOCK_MODE) {
    await fakeDelay()
    return mockCases.find((c) => c.id === caseId) ?? null
  }
  const res = await apiClient.get(`/cases/${caseId}`)
  return res.data
}

export async function createCase(payload) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { id: `CSIA-2026-${Math.floor(Math.random() * 9000 + 1000)}`, ...payload }
  }
  const res = await apiClient.post('/cases', payload)
  return res.data
}

export async function updateCase(caseId, payload) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { id: caseId, ...payload }
  }
  const res = await apiClient.patch(`/cases/${caseId}`, payload)
  return res.data
}
