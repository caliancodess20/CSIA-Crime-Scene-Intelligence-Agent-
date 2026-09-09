// Talks to Anwesha's image_analysis module (backend/app/image_analysis/app.py).
// This one is based on real, confirmed code she shared — not a guess:
//   POST /analyze-evidence/   (multipart, field name "file")
//   -> { status, device_used, filename,
//        payload: { detected_objects: [...], extracted_text: [...] } }
import axios from 'axios'
import { MOCK_MODE, fakeDelay } from './client'

const imageAnalysisClient = axios.create({
  baseURL: '/image-api'
})

export async function analyzeEvidenceImage(file) {
  if (MOCK_MODE) {
    await fakeDelay(900)
    return {
      status: 'success',
      device_used: 'cpu',
      filename: file.name,
      payload: {
        detected_objects: [
          { class_name: 'person', confidence: 0.91, bounding_box: [120, 45, 310, 400] },
          { class_name: 'car', confidence: 0.87, bounding_box: [400, 200, 620, 380] },
          { class_name: 'backpack', confidence: 0.72, bounding_box: [150, 250, 220, 390] }
        ],
        extracted_text: [
          { text: 'NO PARKING', confidence: 0.95, bounding_box: [[50, 10], [200, 10], [200, 40], [50, 40]] }
        ]
      }
    }
  }
  const form = new FormData()
  form.append('file', file)
  const res = await imageAnalysisClient.post('/analyze-evidence/', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data
}
