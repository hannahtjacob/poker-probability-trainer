def calculate_pot_odds(pot_size: float, call_amount: float) -> dict:
    if pot_size < 0:
        raise ValueError("Pot size must be greater than or equal to 0")

    if call_amount <= 0:
        raise ValueError("Call amount must be greater than 0")

    required_equity = call_amount / (pot_size + call_amount) * 100

    return {
        "pot_size": pot_size,
        "call_amount": call_amount,
        "required_equity": round(required_equity, 2),
    }


def evaluate_call_decision(equity: float, required_equity: float) -> dict:
    if not 0 <= equity <= 100:
        raise ValueError("Equity must be between 0 and 100")

    if not 0 <= required_equity <= 100:
        raise ValueError("Required equity must be between 0 and 100")

    margin = equity - required_equity

    if equity >= required_equity + 3:
        decision = "Profitable call"
    elif equity < required_equity - 3:
        decision = "Likely fold"
    else:
        decision = "Close decision"

    return {
        "decision": decision,
        "margin": round(margin, 2),
    }
