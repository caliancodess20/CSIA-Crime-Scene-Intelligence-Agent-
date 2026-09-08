import { useState } from 'react'
import { FileDown, Loader2, CheckCircle2 } from 'lucide-react'
import { generateReport } from '../../api/report'

export default function ReportExport({ caseId }) {
  const [status, setStatus] = useState('idle') // idle | generating | ready

  async function handleGenerate() {
    setStatus('generating')
    const result = await generateReport(caseId)
    setStatus('ready')
    if (result.url) {
      const a = document.createElement('a')
      a.href = result.url
      a.download = result.filename
      a.click()
    }
  }

  return (
    <div className="flex flex-col items-start gap-3 rounded-sm border border-ink-700 bg-ink-800 p-5">
      <div>
        <h3 className="font-display text-lg text-text-primary">Case report</h3>
        <p className="text-sm text-text-faint">
          Compiles case summary, timeline, evidence log, and relationship graph into one export.
        </p>
      </div>
      <button
        onClick={handleGenerate}
        disabled={status === 'generating'}
        className="flex items-center gap-2 rounded-sm bg-tag-amber px-4 py-2 text-sm font-medium text-ink-950 transition-opacity hover:opacity-90 disabled:opacity-60"
      >
        {status === 'generating' && <Loader2 size={16} className="animate-spin" />}
        {status === 'ready' && <CheckCircle2 size={16} />}
        {status === 'idle' && <FileDown size={16} />}
        {status === 'generating' ? 'Generating…' : status === 'ready' ? 'Report ready' : 'Generate report'}
      </button>
      {status === 'ready' && (
        <p className="text-xs text-text-faint">
          Standing in for a real download until Tanya's report_generator returns a file — this just
          confirms the call succeeds end to end.
        </p>
      )}
    </div>
  )
}
