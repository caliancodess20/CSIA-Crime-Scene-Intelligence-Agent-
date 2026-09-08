import { useState, useEffect, useRef } from 'react'
import { Search, X } from 'lucide-react'
import { searchAll } from '../../api/search'

export default function SearchBar({ onSelectCase }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(null)
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  useEffect(() => {
    if (!query.trim()) {
      setResults(null)
      return
    }
    const handle = setTimeout(async () => {
      const data = await searchAll(query)
      setResults(data)
      setOpen(true)
    }, 250)
    return () => clearTimeout(handle)
  }, [query])

  useEffect(() => {
    function handleClick(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  return (
    <div ref={containerRef} className="relative w-full max-w-md">
      <div className="flex items-center gap-2 rounded-sm border border-ink-600 bg-ink-800 px-3 py-2 focus-within:border-tag-amber">
        <Search size={16} className="text-text-faint shrink-0" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query && setOpen(true)}
          placeholder="Search cases, evidence, IDs…"
          className="w-full bg-transparent text-sm text-text-primary placeholder:text-text-faint focus:outline-none"
        />
        {query && (
          <button onClick={() => setQuery('')} aria-label="Clear search">
            <X size={14} className="text-text-faint hover:text-text-primary" />
          </button>
        )}
      </div>

      {open && results && (
        <div className="absolute z-20 mt-1 w-full rounded-sm border border-ink-600 bg-ink-800 shadow-lg shadow-black/40">
          {results.cases.length === 0 && results.evidence.length === 0 && (
            <p className="px-3 py-3 text-sm text-text-faint">No matches for "{query}".</p>
          )}
          {results.cases.length > 0 && (
            <div>
              <p className="px-3 pt-2 text-xs uppercase tracking-wide text-text-faint">Cases</p>
              {results.cases.map((c) => (
                <button
                  key={c.id}
                  onClick={() => {
                    onSelectCase?.(c.id)
                    setOpen(false)
                  }}
                  className="flex w-full items-center justify-between px-3 py-2 text-left text-sm hover:bg-ink-700"
                >
                  <span>{c.title}</span>
                  <span className="font-mono text-xs text-text-faint">{c.id}</span>
                </button>
              ))}
            </div>
          )}
          {results.evidence.length > 0 && (
            <div className="border-t border-ink-600">
              <p className="px-3 pt-2 text-xs uppercase tracking-wide text-text-faint">Evidence</p>
              {results.evidence.map((e) => (
                <div key={e.id} className="px-3 py-2 text-sm text-text-muted">
                  {e.filename}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
