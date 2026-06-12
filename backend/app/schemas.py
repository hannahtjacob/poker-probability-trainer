from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EquityRequest(BaseModel):
    hero_cards: list[str]
    community_cards: list[str] = []
    num_opponents: int = 1
    simulations: int = 10000
    seed: int | None = None


class PotOddsRequest(BaseModel):
    pot_size: float
    call_amount: float
    equity: float | None = None


class AnalyzeRequest(BaseModel):
    hero_cards: list[str]
    community_cards: list[str] = []
    num_opponents: int = 1
    simulations: int = 10000
    seed: int | None = None
    pot_size: float | None = None
    call_amount: float | None = None
    use_ai: bool = False
    save_result: bool = True


class HistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hero_cards: str
    community_cards: str | None
    num_opponents: int
    simulations: int
    win_probability: float
    tie_probability: float
    loss_probability: float
    equity: float
    pot_size: float | None
    call_amount: float | None
    required_equity: float | None
    decision: str | None
    recommendation: str | None
    created_at: datetime
