import { useEffect, useState } from 'react'
import { ArrowRight } from 'lucide-react'
import { getTimelineAndNextSteps } from '../../api/timeline'
import { mockTimeline } from '../../mockData'

// Wired to Sanskruti's timeline_suggestions/routes.py:
//   POST /timeline/suggestions { events } -> { timeline, next_steps }
// `events` below is a placeholder list; swap it for whatever the case's
// real evidence-derived event log looks like once that shape is settled.
export default function Timeline({ events = mockTimeline }) {
  const [timeline, setTimeline] = useState([])
  const [nextSteps, setNextSteps] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getTimelineAndNextSteps(events).then(({ timeline, next_steps }) => {
      setTimeline(timeline)
      setNextSteps(next_steps)
      setLoading(false)
    })
  }, [events])

  if (loading) {
    return <div className="h-40 animate-pulse rounded-sm border border-ink-700 bg-ink-800" />
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
      <div>
        <h3 className="mb-3 font-display text-lg text-text-primary">Timeline</h3>
        <ol className="relative border-l border-ink-600 pl-5">
          {timeline.map((event, i) => (
            <li key={i} className="mb-5 last:mb-0">
              <span className="absolute -left-[5px] mt-1.5 h-2.5 w-2.5 rounded-full border-2 border-ink-950 bg-tag-amber" />
              <p className="font-mono text-xs text-text-faint">{event.timestamp}</p>
              <p className="text-sm text-text-primary">{event.event}</p>
            </li>
          ))}
        </ol>
      </div>

      <div>
        <h3 className="mb-3 font-display text-lg text-text-primary">Suggested next steps</h3>
        {nextSteps.length === 0 ? (
          <p className="text-sm text-text-faint">No rule-based suggestions for the current timeline.</p>
        ) : (
          <ul className="space-y-2">
            {nextSteps.map((step, i) => (
              <li
                key={i}
                className="flex items-start gap-2 rounded-sm border border-ink-700 bg-ink-800 px-3 py-2 text-sm text-text-muted"
              >
                <ArrowRight size={14} className="mt-0.5 shrink-0 text-tag-amber" />
                {step}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
