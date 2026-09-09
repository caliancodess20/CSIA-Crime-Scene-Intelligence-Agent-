import { useState } from 'react'
import { ShieldHalf } from 'lucide-react'
import SearchBar from './components/SearchBar/SearchBar'
import Dashboard from './pages/Dashboard'
import CaseDetail from './pages/CaseDetail'
import { MOCK_MODE } from './api/client'

export default function App() {
  const [activeCase, setActiveCase] = useState(null)

  return (
    <div className="min-h-screen bg-ink-950">
      <header className="border-b border-ink-700 bg-ink-900">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-2">
            <ShieldHalf size={20} className="text-tag-amber" />
            <span className="font-display text-xl tracking-wide text-text-primary">CSIA</span>
            <span className="hidden text-sm text-text-faint sm:inline">Case Intelligence</span>
          </div>
          <SearchBar onSelectCase={setActiveCase} />
        </div>
      </header>

      {MOCK_MODE && (
        <div className="border-b border-tag-amber/30 bg-tag-amber/10 px-4 py-1.5 text-center text-xs text-tag-amber">
          Running on mock data — flip MOCK_MODE in src/api/client.js once a backend route is live.
        </div>
      )}

      <main className="mx-auto max-w-6xl px-4 py-6">
        {activeCase ? (
          <CaseDetail caseId={activeCase} onBack={() => setActiveCase(null)} />
        ) : (
          <Dashboard onOpenCase={setActiveCase} />
        )}
      </main>
    </div>
  )
}
