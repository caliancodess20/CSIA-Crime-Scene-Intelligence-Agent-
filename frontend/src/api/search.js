// Talks to Yojit's search.py (search + filter across cases/evidence).
import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockCases, mockEvidence } from '../mockData'

export async function searchAll(query) {
  if (MOCK_MODE) {
    await fakeDelay(300)
    const q = query.trim().toLowerCase()
    if (!q) return { cases: [], evidence: [] }
    return {
      cases: mockCases.filter(
        (c) => c.title.toLowerCase().includes(q) || c.id.toLowerCase().includes(q)
      ),
      evidence: mockEvidence.filter((e) => e.filename.toLowerCase().includes(q))
    }
  }
  const res = await apiClient.get('/search', { params: { q: query } })
  return res.data
}
