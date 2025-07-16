from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase

router = APIRouter(prefix="/student/finance", tags=["student-finance"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/dashboard")
def get_finance_dashboard(token: str = Depends(oauth2)):
    """Return finance overview stats and savings goals."""
    return {"balance":0, "income":0, "expenses":0, "savings":[]}  

@router.get("/transactions", response_model=List[dict])
def list_transactions(token: str = Depends(oauth2)):
    """List all finance transactions for the student."""
    return []

@router.post("/transactions", response_model=dict)
def add_transaction(tx: dict, token: str = Depends(oauth2)):
    """Record a new income or expense transaction."""
    return tx