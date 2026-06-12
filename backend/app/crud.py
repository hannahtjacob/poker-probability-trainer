from app.models import SimulationHistory


def create_simulation_history(db, analysis: dict) -> SimulationHistory:
    simulation = analysis["simulation"]
    pot_odds = analysis.get("pot_odds") or {}
    decision = analysis.get("decision") or {}
    recommendation = analysis["recommendation"]

    history = SimulationHistory(
        hero_cards=",".join(simulation["hero_cards"]),
        community_cards=",".join(simulation["community_cards"]),
        num_opponents=simulation["num_opponents"],
        simulations=simulation["simulations"],
        win_probability=simulation["win_probability"],
        tie_probability=simulation["tie_probability"],
        loss_probability=simulation["loss_probability"],
        equity=simulation["equity"],
        pot_size=pot_odds.get("pot_size"),
        call_amount=pot_odds.get("call_amount"),
        required_equity=pot_odds.get("required_equity"),
        decision=decision.get("decision"),
        recommendation=recommendation["explanation"],
    )

    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_simulation_history(
    db,
    limit: int = 20,
) -> list[SimulationHistory]:
    return (
        db.query(SimulationHistory)
        .order_by(
            SimulationHistory.created_at.desc(),
            SimulationHistory.id.desc(),
        )
        .limit(limit)
        .all()
    )
