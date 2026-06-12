from fastapi import APIRouter, Depends, HTTPException

from app.crud import create_simulation_history
from app.database import get_db
from app.schemas import AnalyzeRequest, EquityRequest
from poker.odds import calculate_pot_odds, evaluate_call_decision
from poker.recommendations import generate_rule_based_recommendation
from poker.simulator import simulate_equity


router = APIRouter()


@router.post("/simulate")
def simulate(request: EquityRequest):
    try:
        return simulate_equity(
            hero_cards=request.hero_cards,
            community_cards=request.community_cards,
            num_opponents=request.num_opponents,
            simulations=request.simulations,
            seed=request.seed,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/analyze")
def analyze(request: AnalyzeRequest, db=Depends(get_db)):
    try:
        simulation = simulate_equity(
            hero_cards=request.hero_cards,
            community_cards=request.community_cards,
            num_opponents=request.num_opponents,
            simulations=request.simulations,
            seed=request.seed,
        )

        pot_odds = None
        decision = None
        if request.pot_size is not None and request.call_amount is not None:
            pot_odds = calculate_pot_odds(
                pot_size=request.pot_size,
                call_amount=request.call_amount,
            )
            decision = evaluate_call_decision(
                equity=simulation["equity"],
                required_equity=pot_odds["required_equity"],
            )

        recommendation = generate_rule_based_recommendation(
            simulation_result=simulation,
            pot_odds_result=pot_odds,
            decision_result=decision,
        )

        analysis = {
            "simulation": simulation,
            "pot_odds": pot_odds,
            "decision": decision,
            "recommendation": recommendation,
        }

        saved_id = None
        if request.save_result:
            saved = create_simulation_history(db, analysis)
            saved_id = saved.id

        return {
            **analysis,
            "saved_id": saved_id,
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
