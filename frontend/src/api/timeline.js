// Talks to Sanskruti's timeline_suggestions module.
// GET/POST shape below matches her routes.py exactly:
//   POST /timeline/suggestions  { events: [...] }  ->  { timeline, next_steps }
import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockTimeline, mockNextSteps } from '../mockData'

export async function getTimelineAndNextSteps(events) {
  if (MOCK_MODE) {
    await fakeDelay()
    return { timeline: mockTimeline, next_steps: mockNextSteps }
  }
  const res = await apiClient.post('/timeline/suggestions', { events })
  return res.data
}
