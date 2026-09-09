// Talks to Tanya's evidence_upload module.
import { apiClient, MOCK_MODE, fakeDelay } from './client'
import { mockEvidence } from '../mockData'

export async function listEvidence(caseId) {
  if (MOCK_MODE) {
    await fakeDelay()
    return mockEvidence
  }
  const res = await apiClient.get(`/cases/${caseId}/evidence`)
  return res.data
}

// file: a File object from an <input type="file"> or drop event
export async function uploadEvidence(caseId, file, onProgress) {
  if (MOCK_MODE) {
    // Simulate a progress bar so the UI component works standalone.
    for (let pct = 0; pct <= 100; pct += 20) {
      await fakeDelay(120)
      onProgress?.(pct)
    }
    return {
      id: `EV-${Math.floor(Math.random() * 900 + 100)}`,
      type: file.type.startsWith('image') ? 'image' : file.type.startsWith('video') ? 'video_frame' : 'text',
      filename: file.name,
      uploadedBy: 'You',
      timestamp: new Date().toISOString().slice(0, 16).replace('T', ' ')
    }
  }
  const form = new FormData()
  form.append('file', file)
  form.append('case_id', caseId)
  const res = await apiClient.post('/evidence/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (evt) => onProgress?.(Math.round((evt.loaded / evt.total) * 100))
  })
  return res.data
}
