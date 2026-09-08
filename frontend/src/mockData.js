// Placeholder data standing in for each backend track until it lands.
// Shape these to match the real response bodies as soon as routes.py /
// schemas.py exist for each module — that's the whole point of this file.

export const mockCases = [
  {
    id: 'CSIA-2026-0142',
    title: 'Warehouse District Break-In',
    status: 'active',
    opened: '2026-08-24',
    lead: 'Det. R. Fontaine',
    evidenceCount: 7,
    summary: 'Forced entry reported at a storage facility on 4th Ave. Two witness statements collected, CCTV pending retrieval.'
  },
  {
    id: 'CSIA-2026-0139',
    title: 'Downtown Vehicle Theft Ring',
    status: 'active',
    opened: '2026-08-19',
    lead: 'Det. M. Okafor',
    evidenceCount: 12,
    summary: 'Pattern of thefts across three parking structures. Suspect vehicle partially identified from traffic cam still.'
  },
  {
    id: 'CSIA-2026-0121',
    title: 'Riverside Fraud Complaint',
    status: 'closed',
    opened: '2026-07-30',
    lead: 'Det. R. Fontaine',
    evidenceCount: 4,
    summary: 'Case closed after forensic document review confirmed complainant account.'
  }
]

export const mockTimeline = [
  { event: 'Case created', timestamp: '2026-08-24 10:00' },
  { event: 'Witness statement', timestamp: '2026-08-24 14:00' },
  { event: 'Evidence collected', timestamp: '2026-08-24 15:30' }
]

export const mockNextSteps = [
  'Perform forensic analysis on the collected evidence.',
  'Conduct a suspect interview based on available witness information.'
]

export const mockEvidence = [
  { id: 'EV-001', type: 'image', filename: 'entry_point_01.jpg', uploadedBy: 'Det. R. Fontaine', timestamp: '2026-08-24 15:30' },
  { id: 'EV-002', type: 'text', filename: 'witness_statement_castillo.txt', uploadedBy: 'Det. R. Fontaine', timestamp: '2026-08-24 14:05' },
  { id: 'EV-003', type: 'video_frame', filename: 'cctv_frame_0087.png', uploadedBy: 'System', timestamp: '2026-08-24 16:12' }
]

export const mockGraph = {
  nodes: [
    { id: 'W. Castillo', type: 'witness' },
    { id: '4th Ave Storage', type: 'location' },
    { id: 'Unknown Suspect A', type: 'suspect' },
    { id: 'Grey Sedan', type: 'object' }
  ],
  edges: [
    { source: 'W. Castillo', target: '4th Ave Storage', label: 'reported at' },
    { source: '4th Ave Storage', target: 'Unknown Suspect A', label: 'seen entering' },
    { source: 'Unknown Suspect A', target: 'Grey Sedan', label: 'drove' }
  ]
}
