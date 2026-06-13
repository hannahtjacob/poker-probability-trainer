import type { DecisionResult, PotOddsResult } from '../types/poker'


interface PotOddsPanelProps {
  potOdds?: PotOddsResult | null
  decision?: DecisionResult | null
}

function PotOddsPanel({ potOdds, decision }: PotOddsPanelProps) {
  if (!potOdds) {
    return null
  }

  return (
    <section className="pot-odds-panel" aria-labelledby="pot-odds-title">
      <h2 id="pot-odds-title">Pot Odds</h2>

      <dl className="pot-odds-list">
        <div className="pot-odds-item">
          <dt>Pot size</dt>
          <dd>{potOdds.pot_size}</dd>
        </div>

        <div className="pot-odds-item">
          <dt>Call amount</dt>
          <dd>{potOdds.call_amount}</dd>
        </div>

        <div className="pot-odds-item">
          <dt>Required equity</dt>
          <dd>{potOdds.required_equity.toFixed(2)}%</dd>
        </div>

        {decision && (
          <>
            <div className="pot-odds-item">
              <dt>Decision</dt>
              <dd>{decision.decision}</dd>
            </div>

            <div className="pot-odds-item">
              <dt>Margin</dt>
              <dd>{decision.margin.toFixed(2)} percentage points</dd>
            </div>
          </>
        )}
      </dl>

      <p className="pot-odds-explanation">
        Required equity is the minimum equity needed for a call to break even.
      </p>
    </section>
  )
}

export default PotOddsPanel
