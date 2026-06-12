from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.database import Base


class SimulationHistory(Base):
    __tablename__ = "simulation_history"

    id = Column(Integer, primary_key=True, index=True)
    hero_cards = Column(String, nullable=False)
    community_cards = Column(String, nullable=True)
    num_opponents = Column(Integer, nullable=False)
    simulations = Column(Integer, nullable=False)
    win_probability = Column(Float, nullable=False)
    tie_probability = Column(Float, nullable=False)
    loss_probability = Column(Float, nullable=False)
    equity = Column(Float, nullable=False)
    pot_size = Column(Float, nullable=True)
    call_amount = Column(Float, nullable=True)
    required_equity = Column(Float, nullable=True)
    decision = Column(String, nullable=True)
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
