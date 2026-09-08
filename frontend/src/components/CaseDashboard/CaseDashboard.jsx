import { useEffect, useState } from 'react'
import { listCases } from '../../api/cases'

const statusStyles = {
  active: 'bg-tag-amber/15 text-tag-amber border-tag-amber/40',
  closed: 'bg-text-faint/10 text-text-faint border-text-faint/30'
}

export default function CaseDashboard({ onOpenCase }) {
  const [cases, setCases] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listCases().then((data) => {
      setCases(data)
      setLoading(false)
    })
  }, [])

  if (loading) {
    return (
      <div className="space-y-2">
        {[0, 1, 2].map((i) => (
          <div key={i} className="h-20 animate-pulse rounded-sm border border-ink-700 bg-ink-800" />
        ))}
      </div>
    )
  }

  if (cases.length === 0) {
    return (
      <div className="rounded-sm border border-dashed border-ink-600 p-8 text-center">
        <p className="font-display text-xl text-text-primary">No open cases</p>
        <p className="mt-1 text-sm text-text-faint">New cases created by the team will appear here.</p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {cases.map((c) => (
        <button
          key={c.id}
          onClick={() => onOpenCase(c.id)}
          className="flex w-full flex-col gap-2 rounded-sm border border-ink-700 bg-ink-800 p-4 text-left transition-colors hover:border-ink-500 sm:flex-row sm:items-center sm:justify-between"
        >
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs text-text-faint">{c.id}</span>
              <span className={`rounded-sm border px-1.5 py-0.5 text-[10px] font-medium ${statusStyles[c.status]}`}>
                {c.status}
              </span>
            </div>
            <h3 className="mt-1 font-display text-xl leading-tight text-text-primary">{c.title}</h3>
            <p className="mt-1 max-w-xl text-sm text-text-muted">{c.summary}</p>
          </div>
          <div className="flex shrink-0 gap-6 text-sm text-text-faint sm:text-right">
            <div>
              <p className="text-text-muted">{c.lead}</p>
              <p className="font-mono text-xs">opened {c.opened}</p>
            </div>
            <div className="text-center">
              <p className="font-display text-2xl text-text-primary">{c.evidenceCount}</p>
              <p className="text-xs">items</p>
            </div>
          </div>
        </button>
      ))}
    </div>
  )
}
