import { useState, type FormEvent } from 'react'

import type { AnalyzeRequest } from '../types/poker'


interface SimulationFormProps {
  onSubmit: (request: AnalyzeRequest) => void
  loading: boolean
}

function SimulationForm({ onSubmit, loading }: SimulationFormProps) {
  const [heroCard1, setHeroCard1] = useState('As')
  const [heroCard2, setHeroCard2] = useState('Kh')
  const [communityCards, setCommunityCards] = useState('Qd,Jc,2h')
  const [numOpponents, setNumOpponents] = useState('2')
  const [simulations, setSimulations] = useState('10000')
  const [potSize, setPotSize] = useState('')
  const [callAmount, setCallAmount] = useState('')
  const [useAI, setUseAI] = useState(false)

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const request: AnalyzeRequest = {
      hero_cards: [heroCard1.trim(), heroCard2.trim()],
      community_cards: communityCards
        .split(',')
        .map((card) => card.trim())
        .filter(Boolean),
      num_opponents: Number(numOpponents),
      simulations: Number(simulations),
      use_ai: useAI,
      save_result: true,
    }

    if (potSize.trim() !== '') {
      request.pot_size = Number(potSize)
    }

    if (callAmount.trim() !== '') {
      request.call_amount = Number(callAmount)
    }

    onSubmit(request)
  }

  return (
    <form className="simulation-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="hero-card-1">Hero card 1</label>
        <input
          id="hero-card-1"
          type="text"
          value={heroCard1}
          onChange={(event) => setHeroCard1(event.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="hero-card-2">Hero card 2</label>
        <input
          id="hero-card-2"
          type="text"
          value={heroCard2}
          onChange={(event) => setHeroCard2(event.target.value)}
          required
        />
      </div>

      <div className="form-group form-group-wide">
        <label htmlFor="community-cards">Community cards</label>
        <input
          id="community-cards"
          type="text"
          value={communityCards}
          onChange={(event) => setCommunityCards(event.target.value)}
          placeholder="Qd,Jc,2h"
        />
        <small className="form-helper">
          Enter comma-separated cards. Valid examples: As, Kh, Td, 2c.
        </small>
      </div>

      <div className="form-group">
        <label htmlFor="num-opponents">Number of opponents</label>
        <input
          id="num-opponents"
          type="number"
          min="1"
          max="8"
          value={numOpponents}
          onChange={(event) => setNumOpponents(event.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="simulations">Simulations</label>
        <input
          id="simulations"
          type="number"
          min="1"
          value={simulations}
          onChange={(event) => setSimulations(event.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="pot-size">Pot size (optional)</label>
        <input
          id="pot-size"
          type="number"
          min="0"
          step="any"
          value={potSize}
          onChange={(event) => setPotSize(event.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="call-amount">Call amount (optional)</label>
        <input
          id="call-amount"
          type="number"
          min="0"
          step="any"
          value={callAmount}
          onChange={(event) => setCallAmount(event.target.value)}
        />
      </div>

      <label className="form-checkbox">
        <input
          type="checkbox"
          checked={useAI}
          onChange={(event) => setUseAI(event.target.checked)}
        />
        Use AI explanation
      </label>

      <button className="form-submit" type="submit" disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze hand'}
      </button>
    </form>
  )
}

export default SimulationForm
