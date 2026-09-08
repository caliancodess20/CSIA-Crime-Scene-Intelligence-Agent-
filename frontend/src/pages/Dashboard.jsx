import CaseDashboard from '../components/CaseDashboard/CaseDashboard'

export default function Dashboard({ onOpenCase }) {
  return (
    <div>
      <h2 className="mb-4 font-display text-3xl text-text-primary">Cases</h2>
      <CaseDashboard onOpenCase={onOpenCase} />
    </div>
  )
}
