from fastapi import APIRouter, Depends

from app.crud import get_simulation_history
from app.database import get_db
from app.schemas import HistoryResponse


router = APIRouter()


@router.get("/history", response_model=list[HistoryResponse])
def history(limit: int = 20, db=Depends(get_db)):
    return get_simulation_history(db, limit=limit)
