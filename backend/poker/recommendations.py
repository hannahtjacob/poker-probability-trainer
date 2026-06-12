DISCLAIMER = (
    "These probabilities are simulated estimates, not guaranteed outcomes."
)


def generate_rule_based_recommendation(
    simulation_result: dict,
    pot_odds_result: dict | None = None,
    decision_result: dict | None = None,
) -> dict:
    """Generate a beginner-friendly poker recommendation from simulation data."""
    equity = simulation_result["equity"]
    win_probability = simulation_result["win_probability"]
    tie_probability = simulation_result["tie_probability"]
    loss_probability = simulation_result["loss_probability"]

    required_equity = None
    if pot_odds_result is not None:
        required_equity = pot_odds_result.get("required_equity")

    decision = None
    if decision_result is not None:
        decision = decision_result.get("decision")

    probability_summary = (
        f"Your estimated equity is {equity:.2f}%, with a "
        f"{win_probability:.2f}% win chance, {tie_probability:.2f}% tie chance, "
        f"and {loss_probability:.2f}% loss chance."
    )

    if required_equity is not None:
        margin = equity - required_equity
        odds_summary = (
            f" The pot odds require about {required_equity:.2f}% equity."
        )

        if equity >= 70 and margin >= 10:
            action = "raise"
            confidence = "high"
            reasoning = (
                "Your hand has very high estimated equity and comfortably clears "
                "the break-even point, so aggressive play may be reasonable."
            )
        elif margin >= 10 or decision == "Profitable call":
            action = "call"
            confidence = "high" if margin >= 10 else "medium"
            reasoning = (
                "Your estimated equity is meaningfully higher than the equity "
                "needed to call, so calling appears profitable over many similar "
                "situations."
            )
        elif margin <= -10 or decision == "Likely fold":
            action = "fold"
            confidence = "high" if margin <= -10 else "medium"
            reasoning = (
                "Your estimated equity is below the break-even point for this "
                "call, so folding avoids paying too much for the chance to win."
            )
        else:
            action = "caution"
            confidence = "low"
            reasoning = (
                "Your equity is close to the amount required by the pot odds. "
                "Small estimation errors or opponent tendencies could change the "
                "best choice."
            )

        explanation = (
            f"{probability_summary}{odds_summary} {reasoning} {DISCLAIMER}"
        )
    elif equity >= 70:
        action = "raise"
        confidence = "high"
        explanation = (
            f"{probability_summary} This is very high estimated equity, so "
            "aggressive play may be reasonable to build the pot. "
            f"{DISCLAIMER}"
        )
    elif equity >= 50:
        action = "call"
        confidence = "medium"
        explanation = (
            f"{probability_summary} Your hand wins often enough to continue in "
            "many situations, but the price of the call should still be checked. "
            f"{DISCLAIMER}"
        )
    elif equity >= 35:
        action = "caution"
        confidence = "low"
        explanation = (
            f"{probability_summary} The result is uncertain without pot odds, so "
            "check the call price and consider how strongly opponents are playing. "
            f"{DISCLAIMER}"
        )
    else:
        action = "fold"
        confidence = "medium"
        explanation = (
            f"{probability_summary} Your estimated chance of winning is low, so "
            "folding is usually the safer choice unless the call is very cheap. "
            f"{DISCLAIMER}"
        )

    return {
        "action": action,
        "confidence": confidence,
        "explanation": explanation,
    }
