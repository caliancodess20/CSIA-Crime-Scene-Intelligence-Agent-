// Talks to Yojit's search endpoints.
// UPDATED to match Yojit's confirmed API_REFERENCE.md exactly.
//
// GET /api/v1/search/cases   params: q, status, crime_type, priority,
//                                    assigned_investigator, tag, page, page_size
// GET /api/v1/search/evidence  params: q, evidence_type, case_id, page, page_size
//
// status values:   open | under_investigation | closed | archived
// priority values: low | medium | high | critical
// evidence_type:   image | video | document | witness_statement |
//                  cctv_frame | physical | other

import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockCases, mockEvidence } from '../mockData'

// Search cases — pass any combination of filters
export async function searchCases({ q, status, crime_type, priority, assigned_investigator, tag, page = 1, page_size = 20 } = {}) {
  if (MOCK_MODE) {
    await fakeDelay(300)
    if (!q) return { cases: [] }
    const query = q.toLowerCase()
    return {
      cases: mockCases.filter(
        (c) => c.title.toLowerCase().includes(query) || c.id.toLowerCase().includes(query)
      )
    }
  }
  const res = await apiClient.get('/v1/search/cases', {
    params: { q, status, crime_type, priority, assigned_investigator, tag, page, page_size }
  })
  return res.data
}

// Search evidence — pass any combination of filters
export async function searchEvidence({ q, evidence_type, case_id, page = 1, page_size = 20 } = {}) {
  if (MOCK_MODE) {
    await fakeDelay(300)
    if (!q) return { evidence: [] }
    const query = q.toLowerCase()
    return {
      evidence: mockEvidence.filter((e) => e.file_name.toLowerCase().includes(query))
    }
  }
  const res = await apiClient.get('/v1/search/evidence', {
    params: { q, evidence_type, case_id, page, page_size }
  })
  return res.data
}

// Combined search used by the SearchBar component
export async function searchAll(query) {
  if (!query.trim()) return { cases: [], evidence: [] }
  const [casesResult, evidenceResult] = await Promise.all([
    searchCases({ q: query }),
    searchEvidence({ q: query })
  ])
  return {
    cases: casesResult.cases ?? [],
    evidence: evidenceResult.evidence ?? []
  }
}
