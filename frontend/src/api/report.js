// Talks to Tanya's report_generator module.
import { apiClient, MOCK_MODE, fakeDelay } from './client'

export async function generateReport(caseId) {
  if (MOCK_MODE) {
    await fakeDelay(600)
    // Stand-in for a downloadable file URL / blob the real endpoint would return.
    return { url: null, filename: `${caseId}_report.pdf`, ready: true }
  }
  const res = await apiClient.post(`/reports/${caseId}/generate`, null, { responseType: 'blob' })
  return res.data
}
