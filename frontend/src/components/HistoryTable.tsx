import type { HistoryRecord } from '../types/poker'


interface HistoryTableProps {
  history: HistoryRecord[]
}

function formatDate(value: string): string {
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString()
}

function HistoryTable({ history }: HistoryTableProps) {
  if (history.length === 0) {
    return <p className="history-empty">No saved simulations yet.</p>
  }

  return (
    <div className="history-table-wrapper">
      <table className="history-table">
        <caption>Recent simulations</caption>
        <thead>
          <tr>
            <th scope="col">Created</th>
            <th scope="col">Hero cards</th>
            <th scope="col">Community cards</th>
            <th scope="col">Opponents</th>
            <th scope="col">Simulations</th>
            <th scope="col">Win probability</th>
            <th scope="col">Equity</th>
            <th scope="col">Decision</th>
          </tr>
        </thead>
        <tbody>
          {history.map((record) => (
            <tr key={record.id}>
              <td>{formatDate(record.created_at)}</td>
              <td>{record.hero_cards}</td>
              <td>{record.community_cards || 'None'}</td>
              <td>{record.num_opponents}</td>
              <td>{record.simulations.toLocaleString()}</td>
              <td>{record.win_probability.toFixed(2)}%</td>
              <td>{record.equity.toFixed(2)}%</td>
              <td>{record.decision || 'Not calculated'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default HistoryTable
