// Talks to Anmol's nlp_engine module.
// UPDATED to match his confirmed routes.py exactly.
//
// Endpoints (prefixed /api/v1/nlp in main.py):
//   POST /api/v1/nlp/extract
//     body: { case_id: str, statement_text: str }
//     returns: {
//       case_id, summary: [str], entities: [{text,label,start,end}],
//       relationship_graph: { nodes: [{id,type}], edges: [{source,target,context}] }
//     }
//   GET /api/v1/nlp/health

import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockGraph } from '../mockData'

// POST /api/v1/nlp/extract
// Pass a witness statement text — returns summary, entities, and graph
export async function extractStatement(caseId, statementText) {
  if (MOCK_MODE) {
    await fakeDelay(800)
    return {
      case_id: caseId,
      summary: [
        'Witness observed forced entry at 4th Ave storage facility.',
        'Suspect described as male, grey jacket, fled in a grey sedan.'
      ],
      entities: [
        { text: 'W. Castillo', label: 'PERSON', start: 0, end: 11 },
        { text: '4th Ave Storage', label: 'LOC', start: 25, end: 40 },
        { text: 'grey sedan', label: 'ORG', start: 80, end: 90 }
      ],
      relationship_graph: mockGraph
    }
  }
  const res = await apiClient.post('/v1/nlp/extract', {
    case_id: caseId,
    statement_text: statementText
  })
  return res.data
}

// GET /api/v1/nlp/health — health check
export async function nlpHealthCheck() {
  const res = await apiClient.get('/v1/nlp/health')
  return res.data
}

// Helper used by RelationshipGraph component —
// extracts just the graph from a processed statement
export async function getRelationshipGraph(caseId, statementText = '') {
  if (MOCK_MODE) {
    await fakeDelay()
    return mockGraph
  }
  const result = await extractStatement(caseId, statementText)
  return result.relationship_graph
}

// Helper used by the summary panel —
// extracts just the summary sentences
export async function summarizeStatement(caseId, text) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { summary: text.slice(0, 140) + (text.length > 140 ? '…' : '') }
  }
  const result = await extractStatement(caseId, text)
  return { summary: result.summary.join(' ') }
}
