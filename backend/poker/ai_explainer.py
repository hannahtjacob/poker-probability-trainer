import json


def _fallback_explanation(analysis: dict) -> str:
    simulation = analysis.get("simulation") or {}
    pot_odds = analysis.get("pot_odds") or {}
    decision = analysis.get("decision") or {}

    win_probability = simulation.get("win_probability")
    tie_probability = simulation.get("tie_probability")
    loss_probability = simulation.get("loss_probability")
    equity = simulation.get("equity")
    required_equity = pot_odds.get("required_equity")

    parts = [
        "The simulation estimates how often this hand wins, ties, or loses "
        "across many possible deals; these are estimates, not guarantees."
    ]

    if None not in (win_probability, tie_probability, loss_probability):
        parts.append(
            f"It estimated a {win_probability}% chance to win, a "
            f"{tie_probability}% chance to tie, and a {loss_probability}% "
            "chance to lose."
        )

    if equity is not None:
        parts.append(
            f"Equity is {equity}%, which combines wins with a share of tied pots."
        )

    if required_equity is not None and equity is not None:
        comparison = "above" if equity >= required_equity else "below"
        parts.append(
            f"The call requires about {required_equity}% equity, so the estimated "
            f"equity is {comparison} the break-even point."
        )
    elif decision.get("decision"):
        parts.append(f"The rule-based assessment is: {decision['decision']}.")
    else:
        parts.append(
            "Without pot size and call amount, the simulation cannot determine "
            "whether calling offers a good price."
        )

    parts.append(
        "A beginner should compare equity with the break-even equity from pot "
        "odds, while remembering that opponent ranges and uncertain information "
        "can change the result. Use this as an educational exercise, not as "
        "encouragement to gamble."
    )
    return " ".join(parts)


def explain_analysis_with_ai(
    analysis: dict,
    model: str = "llama3.2",
) -> dict:
    """Explain poker analysis with a local Ollama model or a safe fallback."""
    fallback = _fallback_explanation(analysis)
    prompt = (
        "You are a poker probability tutor. Explain the following Texas Hold'em "
        "analysis in clear, beginner-friendly language. Explain what the win, "
        "tie, and loss probabilities mean; what equity means; whether the pot "
        "odds justify calling when pot-odds data is available; and what a "
        "beginner should learn from the hand. Keep the explanation educational, "
        "mention that simulations are estimates rather than guarantees, and do "
        "not encourage gambling.\n\n"
        f"Analysis:\n{json.dumps(analysis, indent=2, default=str)}"
    )

    try:
        import ollama

        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        if isinstance(response, dict):
            explanation = response.get("message", {}).get("content")
        else:
            message = getattr(response, "message", None)
            explanation = getattr(message, "content", None)

        if not explanation or not explanation.strip():
            raise ValueError("Ollama returned an empty explanation")

        return {
            "success": True,
            "model": model,
            "ai_explanation": explanation.strip(),
        }
    except Exception:
        return {
            "success": False,
            "model": model,
            "ai_explanation": fallback,
        }
