import { useEffect, useState } from 'react'
import { ArrowLeft } from 'lucide-react'
import { getCase } from '../api/cases'
import EvidenceUpload from '../components/EvidenceUpload/EvidenceUpload'
import Timeline from '../components/Timeline/Timeline'
import RelationshipGraph from '../components/RelationshipGraph/RelationshipGraph'
import ReportExport from '../components/ReportExport/ReportExport'

const tabs = ['Overview', 'Evidence', 'Timeline', 'Graph', 'Report']

export default function CaseDetail({ caseId, onBack }) {
  const [caseData, setCaseData] = useState(null)
  const [tab, setTab] = useState('Overview')

  useEffect(() => {
    getCase(caseId).then(setCaseData)
  }, [caseId])

  return (
    <div>
      <button
        onClick={onBack}
        className="mb-4 flex items-center gap-1.5 text-sm text-text-faint hover:text-text-primary"
      >
        <ArrowLeft size={14} /> Back to cases
      </button>

      {caseData && (
        <div className="mb-5">
          <p className="font-mono text-xs text-text-faint">{caseData.id}</p>
          <h2 className="font-display text-3xl text-text-primary">{caseData.title}</h2>
        </div>
      )}

      <div className="mb-5 flex gap-1 border-b border-ink-700">
        {tabs.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-3 py-2 text-sm transition-colors ${
              tab === t
                ? 'border-b-2 border-tag-amber text-text-primary'
                : 'text-text-faint hover:text-text-muted'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === 'Overview' && caseData && (
        <p className="max-w-2xl text-sm text-text-muted">{caseData.summary}</p>
      )}
      {tab === 'Evidence' && <EvidenceUpload caseId={caseId} />}
      {tab === 'Timeline' && <Timeline />}
      {tab === 'Graph' && <RelationshipGraph caseId={caseId} />}
      {tab === 'Report' && <ReportExport caseId={caseId} />}
    </div>
  )
}
