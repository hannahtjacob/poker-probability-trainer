export interface SimulationResult {
  wins: number
  ties: number
  losses: number
  win_probability: number
  tie_probability: number
  loss_probability: number
  equity: number
  simulations: number
  num_opponents: number
  hero_cards: string[]
  community_cards: string[]
}

export interface PotOddsResult {
  pot_size: number
  call_amount: number
  required_equity: number
}

export interface DecisionResult {
  decision: string
  margin: number
}

export interface RecommendationResult {
  action: 'raise' | 'call' | 'fold' | 'caution'
  confidence: 'high' | 'medium' | 'low'
  explanation: string
}

export interface AnalyzeRequest {
  hero_cards: string[]
  community_cards?: string[]
  num_opponents?: number
  simulations?: number
  seed?: number | null
  pot_size?: number | null
  call_amount?: number | null
  use_ai?: boolean
  save_result?: boolean
}

export interface AiExplanationResult {
  success: boolean
  model: string
  ai_explanation: string
}

export interface AnalyzeResponse {
  simulation: SimulationResult
  pot_odds?: PotOddsResult | null
  decision?: DecisionResult | null
  recommendation: RecommendationResult
  saved_id?: number | null
  ai?: AiExplanationResult | null
}

export interface HistoryRecord {
  id: number
  hero_cards: string
  community_cards: string | null
  num_opponents: number
  simulations: number
  win_probability: number
  tie_probability: number
  loss_probability: number
  equity: number
  pot_size: number | null
  call_amount: number | null
  required_equity: number | null
  decision: string | null
  recommendation: string | null
  created_at: string
}
