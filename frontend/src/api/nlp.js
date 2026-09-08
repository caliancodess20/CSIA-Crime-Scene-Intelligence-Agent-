// Talks to Anmol's nlp_engine module (summarizer + relationship_graph).
import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockGraph } from '../mockData'

export async function getRelationshipGraph(caseId) {
  if (MOCK_MODE) {
    await fakeDelay()
    return mockGraph
  }
  const res = await apiClient.get(`/nlp/relationship-graph/${caseId}`)
  return res.data
}

export async function summarizeStatement(text) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { summary: text.slice(0, 140) + (text.length > 140 ? '…' : '') }
  }
  const res = await apiClient.post('/nlp/summarize', { text })
  return res.data
}
