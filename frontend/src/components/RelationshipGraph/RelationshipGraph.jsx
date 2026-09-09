import { useEffect, useMemo, useState } from 'react'
import { getRelationshipGraph } from '../../api/nlp'

const typeColor = {
  witness: '#5C8A5A',
  suspect: '#A8455C',
  location: '#E8A33D',
  object: '#8B93A7'
}

// Simple circular layout — swap for d3-force or react-force-graph later if
// graphs get large; fine for the handful of entities a single case produces.
export default function RelationshipGraph({ caseId }) {
  const [graph, setGraph] = useState({ nodes: [], edges: [] })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getRelationshipGraph(caseId).then((data) => {
      setGraph(data)
      setLoading(false)
    })
  }, [caseId])

  const positions = useMemo(() => {
    const cx = 300
    const cy = 200
    const r = 140
    const map = {}
    graph.nodes.forEach((node, i) => {
      const angle = (2 * Math.PI * i) / Math.max(graph.nodes.length, 1) - Math.PI / 2
      map[node.id] = { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) }
    })
    return map
  }, [graph.nodes])

  if (loading) {
    return <div className="h-80 animate-pulse rounded-sm border border-ink-700 bg-ink-800" />
  }

  if (graph.nodes.length === 0) {
    return (
      <div className="rounded-sm border border-dashed border-ink-600 p-8 text-center text-sm text-text-faint">
        No entities extracted yet — the relationship graph populates once Anmol's NLP module processes statements for this case.
      </div>
    )
  }

  return (
    <div>
      <svg viewBox="0 0 600 400" className="w-full rounded-sm border border-ink-700 bg-ink-800">
        {graph.edges.map((edge, i) => {
          const s = positions[edge.source]
          const t = positions[edge.target]
          if (!s || !t) return null
          const mx = (s.x + t.x) / 2
          const my = (s.y + t.y) / 2
          return (
            <g key={i}>
              <line x1={s.x} y1={s.y} x2={t.x} y2={t.y} stroke="#3A4359" strokeWidth={1.5} />
              <text x={mx} y={my - 4} fontSize="10" fill="#8B93A7" textAnchor="middle" fontFamily="IBM Plex Mono, monospace">
                {edge.label}
              </text>
            </g>
          )
        })}
        {graph.nodes.map((node) => {
          const p = positions[node.id]
          return (
            <g key={node.id}>
              <circle cx={p.x} cy={p.y} r={8} fill={typeColor[node.type] ?? '#8B93A7'} />
              <text
                x={p.x}
                y={p.y - 14}
                fontSize="11"
                fill="#E8EAF0"
                textAnchor="middle"
                fontFamily="IBM Plex Sans, sans-serif"
              >
                {node.id}
              </text>
            </g>
          )
        })}
      </svg>
      <div className="mt-3 flex flex-wrap gap-4 text-xs text-text-faint">
        {Object.entries(typeColor).map(([type, color]) => (
          <div key={type} className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full" style={{ backgroundColor: color }} />
            {type}
          </div>
        ))}
      </div>
    </div>
  )
}
