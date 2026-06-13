import type { RecommendationResult } from '../types/poker'


interface RecommendationCardProps {
  recommendation?: RecommendationResult | null
}

function formatLabel(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1)
}

function RecommendationCard({ recommendation }: RecommendationCardProps) {
  if (!recommendation) {
    return null
  }

  return (
    <article
      className={`recommendation-card recommendation-${recommendation.action}`}
      aria-labelledby="recommendation-title"
    >
      <h2 id="recommendation-title">Recommendation</h2>

      <dl className="recommendation-summary">
        <div className="recommendation-item">
          <dt>Action</dt>
          <dd>{formatLabel(recommendation.action)}</dd>
        </div>

        <div className="recommendation-item">
          <dt>Confidence</dt>
          <dd>{formatLabel(recommendation.confidence)}</dd>
        </div>
      </dl>

      <p className="recommendation-explanation">
        {recommendation.explanation}
      </p>

      <small className="recommendation-note">
        Recommendations are educational estimates, not guaranteed outcomes.
      </small>
    </article>
  )
}

export default RecommendationCard
