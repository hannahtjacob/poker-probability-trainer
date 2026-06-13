import { useEffect, useState } from 'react'

import { analyzeHand, getHistory } from './api/client'
import AIExplanation from './components/AIExplanation'
import HistoryTable from './components/HistoryTable'
import PotOddsPanel from './components/PotOddsPanel'
import ProbabilityChart from './components/ProbabilityChart'
import RecommendationCard from './components/RecommendationCard'
import SimulationForm from './components/SimulationForm'
import type {
  AnalyzeRequest,
  AnalyzeResponse,
  HistoryRecord,
} from './types/poker'
import './App.css'


function getErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'An unexpected error occurred'
}

function App() {
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null)
  const [history, setHistory] = useState<HistoryRecord[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    async function loadHistory() {
      try {
        const records = await getHistory()
        if (active) {
          setHistory(records)
        }
      } catch (historyError) {
        if (active) {
          setError(getErrorMessage(historyError))
        }
      }
    }

    void loadHistory()

    return () => {
      active = false
    }
  }, [])

  async function handleAnalyze(request: AnalyzeRequest) {
    setLoading(true)
    setError(null)

    try {
      const result = await analyzeHand(request)
      setAnalysis(result)

      try {
        setHistory(await getHistory())
      } catch (historyError) {
        setError(
          `Analysis completed, but history could not be refreshed: ${getErrorMessage(
            historyError,
          )}`,
        )
      }
    } catch (analysisError) {
      setError(getErrorMessage(analysisError))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-kicker">Texas Hold&apos;em probability trainer</p>
        <h1>PokerSense</h1>
        <p className="app-description">
          Explore simulated hand equity, compare it with pot odds, and learn how
          probability can support better poker decisions.
        </p>
      </header>

      <section className="app-section form-section" aria-labelledby="form-title">
        <div className="section-heading">
          <h2 id="form-title">Analyze a hand</h2>
          <p>Enter the known cards and table conditions to run a simulation.</p>
        </div>
        <SimulationForm onSubmit={handleAnalyze} loading={loading} />
      </section>

      {loading && (
        <p className="loading-message" role="status" aria-live="polite">
          Running simulations and analyzing the hand...
        </p>
      )}

      {error && (
        <p className="error-message" role="alert">
          {error}
        </p>
      )}

      {analysis && (
        <section
          className="app-section results-section"
          aria-labelledby="results-title"
        >
          <div className="section-heading">
            <h2 id="results-title">Analysis results</h2>
            <p>
              Based on {analysis.simulation.simulations.toLocaleString()}{' '}
              simulated deals against {analysis.simulation.num_opponents}{' '}
              opponent
              {analysis.simulation.num_opponents === 1 ? '' : 's'}.
            </p>
          </div>

          <div className="metrics-grid" aria-label="Simulation metrics">
            <article className="metric-card">
              <span>Win</span>
              <strong>{analysis.simulation.win_probability.toFixed(2)}%</strong>
            </article>
            <article className="metric-card">
              <span>Tie</span>
              <strong>{analysis.simulation.tie_probability.toFixed(2)}%</strong>
            </article>
            <article className="metric-card">
              <span>Loss</span>
              <strong>{analysis.simulation.loss_probability.toFixed(2)}%</strong>
            </article>
            <article className="metric-card metric-equity">
              <span>Equity</span>
              <strong>{analysis.simulation.equity.toFixed(2)}%</strong>
            </article>
          </div>

          <ProbabilityChart
            winProbability={analysis.simulation.win_probability}
            tieProbability={analysis.simulation.tie_probability}
            lossProbability={analysis.simulation.loss_probability}
          />

          <div className="results-grid">
            <PotOddsPanel
              potOdds={analysis.pot_odds}
              decision={analysis.decision}
            />
            <RecommendationCard recommendation={analysis.recommendation} />
          </div>

          <AIExplanation ai={analysis.ai} />
        </section>
      )}

      <section
        className="app-section history-section"
        aria-labelledby="history-title"
      >
        <div className="section-heading">
          <h2 id="history-title">Recent simulations</h2>
          <p>Review the latest saved hand analyses.</p>
        </div>
        <HistoryTable history={history} />
      </section>
    </main>
  )
}

export default App
