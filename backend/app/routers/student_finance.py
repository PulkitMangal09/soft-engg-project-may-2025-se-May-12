from fastapi import APIRouter, Depends,HTTPException,Query
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase
from ..models import TransactionCreate,TransactionOut,SavingsGoalCreate, SavingsGoalOut
from uuid import uuid4
from fastapi import HTTPException
from datetime import date,datetime

router = APIRouter(prefix="/student/finance", tags=["student-finance"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_user_id(token: str):
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, 'error', None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth_res.user.id

# @router.post("/transactions", response_model=dict)
# def add_transaction(tx: dict, token: str = Depends(oauth2)):
#     """Record a new income or expense transaction."""
#     return tx
#Add New Transaction
@router.post("/transactions", response_model=dict)
def add_transaction(tx: TransactionCreate, token: str = Depends(oauth2)):
    try:
        print("DEBUG: Incoming transaction object:", tx)
        print("DEBUG: Transaction as dict:", tx.dict())

        # Get user ID from token
        user_id = get_user_id(token)
        print("DEBUG: Authenticated user ID:", user_id)

        # Prepare payload
        payload = tx.dict()
        payload["transaction_id"] = str(uuid4())
        payload["student_id"] = user_id
        
        if isinstance(payload["transaction_date"], date):
            payload["transaction_date"] = payload["transaction_date"].isoformat()
        payload["created_at"] = payload["transaction_date"]
        # payload["type"] = payload["type"].lower()
        print("DEBUG: Final payload before insert:", payload)

        # Insert into database
        result = supabase.table("transactions").insert(payload).execute()
        print("DEBUG: Supabase insert result:", result)

        data = getattr(result, "data", None)
        if not data:
            raise HTTPException(status_code=400, detail="Insert failed")

        return data[0]

    except HTTPException:
        raise  # re-raise HTTP exceptions unchanged

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
#Display All Transactions
# @router.get("/transactions", response_model=List[dict])
# def list_transactions(token: str = Depends(oauth2)):
#     """List all finance transactions for the student."""
#     return []
@router.get("/transactions", response_model=List[TransactionOut])
def list_transactions(token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    
    resp = supabase.table("transactions") \
        .select("*") \
        .eq("student_id", user_id) \
        .order("transaction_date", desc=True) \
        .execute()
    
    data = getattr(resp, "data", None)
    if data is None:
        raise HTTPException(status_code=500, detail="Could not fetch transactions")

    return data

# @router.get("/dashboard")
# def get_finance_dashboard(token: str = Depends(oauth2)):
#     """Return finance overview stats and savings goals."""
#     return {"balance":0, "income":0, "expenses":0, "savings":[]}  
@router.get("/dashboard")
def get_finance_dashboard(
    token: str = Depends(oauth2),
    from_date: str | None = Query(None, description="Start date in YYYY-MM-DD format"),
    to_date: str | None = Query(None, description="End date in YYYY-MM-DD format")):
    user_id = get_user_id(token)

    # --- Get first and last day of current month ---
  # Assume these come from frontend (could be None if not provided)
    # from_date_str = None  # e.g., "2025-08-01"
    # to_date_str = None    # e.g., "2025-08-13"
    print(from_date)
    if from_date and to_date:
        # Convert strings to date objects
        first_day = datetime.strptime(from_date, "%Y-%m-%d").date()
        last_day = datetime.strptime(to_date, "%Y-%m-%d").date()
    else:
        # Default: first and last day of current month till today
        today = date.today()
        first_day = today.replace(day=1)
        last_day = today

    print(first_day, last_day)
 # Or dynamically if you need end of month

    # --- Fetch all transactions ---
    tx_resp = supabase.table("transactions") \
        .select("amount, type, transaction_date") \
        .eq("student_id", user_id) \
        .execute()
    
    tx_data = getattr(tx_resp, "data", [])
    if tx_data is None:
        raise HTTPException(status_code=500, detail="Could not fetch transactions")

    # --- Calculate totals ---
    total_income = sum(tx["amount"] for tx in tx_data if tx["type"] == "Income")
    total_expenses = sum(tx["amount"] for tx in tx_data if tx["type"] == "Expense")
   

    # --- Filter for current month ---
    month_income = sum(
        tx["amount"] for tx in tx_data
        if tx["type"] == "Income" and first_day <= date.fromisoformat(tx["transaction_date"]) <= last_day
    )
    month_expenses = sum(
        tx["amount"] for tx in tx_data
        if tx["type"] == "Expense" and first_day <= date.fromisoformat(tx["transaction_date"]) <= last_day
    )
    balance = month_income - month_expenses
    # --- Fetch savings goals ---
    sg_resp = supabase.table("savings_goals") \
        .select("goal_id, title, target_amount, saved_amount") \
        .eq("student_id", user_id) \
        .execute()

    savings_goals = getattr(sg_resp, "data", [])

    tx_resp = supabase.table("transactions") \
    .select("transaction_id, type, amount, type, transaction_date, category, note") \
    .eq("student_id", user_id) \
    .gte("transaction_date", str(first_day)) \
    .lte("transaction_date", str(last_day)) \
    .execute()

    tx_data = getattr(tx_resp, "data", []) or []
    return {
        "balance": balance,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "month_income": month_income,
        "month_expenses": month_expenses,
        "savings": savings_goals,
        "transactions": tx_data
    }


# -------------------------------
# -------------------------------
         # CRUD Goals
# -------------------------------
# -------------------------------


@router.post("/savings-goals", response_model=SavingsGoalOut)
def create_savings_goal(goal: SavingsGoalCreate, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    payload = goal.dict()
    payload["goal_id"] = str(uuid4())
    payload["student_id"] = user_id

    resp = supabase.table("savings_goals").insert(payload).execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]

@router.get("/savings-goals", response_model=List[SavingsGoalOut])
def list_savings_goals(token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("savings_goals").select("*").eq("student_id", user_id).order("created_at", desc=True).execute()
    return getattr(resp, "data", [])

@router.get("/savings-goals/{goal_id}", response_model=SavingsGoalOut)
def get_savings_goal(goal_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    resp = supabase.table("savings_goals").select("*").eq("goal_id", goal_id).eq("student_id", user_id).single().execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=404, detail="Goal not found")
    return data

@router.patch("/savings-goals/{goal_id}", response_model=SavingsGoalOut)
def update_savings_goal(goal_id: str, goal: SavingsGoalCreate, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    payload = goal.dict(exclude_unset=True)
    resp = supabase.table("savings_goals").update(payload).eq("goal_id", goal_id).eq("student_id", user_id).execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]

@router.delete("/savings-goals/{goal_id}", response_model=dict)
def delete_savings_goal(goal_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)
    supabase.table("savings_goals").delete().eq("goal_id", goal_id).eq("student_id", user_id).execute()
    return {"deleted": True}
