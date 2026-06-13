import type { AiExplanationResult } from '../types/poker'


interface AIExplanationProps {
  ai?: AiExplanationResult | null
}

function AIExplanation({ ai }: AIExplanationProps) {
  if (!ai) {
    return null
  }

  return (
    <article
      className={`ai-explanation ${ai.success ? 'ai-success' : 'ai-fallback'}`}
      aria-labelledby="ai-explanation-title"
    >
      <h2 id="ai-explanation-title">AI Explanation</h2>

      {ai.success ? (
        <p className="ai-model">
          Model: <strong>{ai.model}</strong>
        </p>
      ) : (
        <p className="ai-unavailable" role="status">
          Local AI was unavailable, so this educational fallback explanation is
          shown instead.
        </p>
      )}

      <p className="ai-explanation-text">{ai.ai_explanation}</p>

      <small className="ai-explanation-note">
        Use this explanation to learn how probabilities and pot odds relate; it
        does not guarantee a hand&apos;s outcome.
      </small>
    </article>
  )
}

export default AIExplanation
