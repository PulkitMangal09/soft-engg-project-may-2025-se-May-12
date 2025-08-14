from fastapi import APIRouter, Depends,HTTPException,Query
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase
from ..models import TransactionCreate,TransactionOut,SavingsGoalCreate, SavingsGoalOut
from uuid import uuid4
from fastapi import HTTPException
from datetime import date,datetime
from fastapi import Body

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
# @router.get("/transactions", response_model=List[TransactionOut])
# def list_transactions(token: str = Depends(oauth2)):
#     user_id = get_user_id(token)
    
#     resp = supabase.table("transactions") \
#         .select("*") \
#         .eq("student_id", user_id) \
#         .order("transaction_date", desc=True) \
#         .execute()
    
#     data = getattr(resp, "data", None)
#     if data is None:
#         raise HTTPException(status_code=500, detail="Could not fetch transactions")

#     return data
# Get a single transaction
@router.get("/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: str, token: str = Depends(oauth2)):
    try:
        user_id = get_user_id(token)

        # Query supabase for this transaction belonging to the authenticated user
        result = supabase.table("transactions") \
            .select("*") \
            .eq("transaction_id", transaction_id) \
            .eq("student_id", user_id) \
            .execute()

        data = getattr(result, "data", None)
        if not data or len(data) == 0:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return data[0]

    except HTTPException:
        raise
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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

# Delete a transaction by ID
@router.delete("/transactions/{transaction_id}", response_model=dict)
def delete_transaction(transaction_id: str, token: str = Depends(oauth2)):
    try:
        user_id = get_user_id(token)

        # Fetch the transaction to ensure it belongs to the user
        result = supabase.table("transactions") \
            .select("*") \
            .eq("transaction_id", transaction_id) \
            .eq("student_id", user_id) \
            .execute()
        
        data = getattr(result, "data", [])
        if not data:
            raise HTTPException(status_code=404, detail="Transaction not found")

        # Delete the transaction
        delete_result = supabase.table("transactions") \
            .delete() \
            .eq("transaction_id", transaction_id) \
            .eq("student_id", user_id) \
            .execute()

        deleted_data = getattr(delete_result, "data", [])
        if not deleted_data:
            raise HTTPException(status_code=500, detail="Delete failed")

        return {"message": "Transaction deleted successfully", "transaction_id": transaction_id}

    except HTTPException:
        raise
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/transactions/{transaction_id}", response_model=dict)
def update_transaction(transaction_id: str, tx: TransactionCreate, token: str = Depends(oauth2)):
    user_id = get_user_id(token)

    # Ensure transaction belongs to this user
    existing = supabase.table("transactions").select("*").eq("transaction_id", transaction_id).eq("student_id", user_id).execute()
    data = getattr(existing, "data", [])
    if not data:
        raise HTTPException(status_code=404, detail="Transaction not found")

    payload = tx.dict()
    if isinstance(payload["transaction_date"], date):
        payload["transaction_date"] = payload["transaction_date"].isoformat()

    # Update
    result = supabase.table("transactions").update(payload).eq("transaction_id", transaction_id).execute()
    updated_data = getattr(result, "data", [])
    if not updated_data:
        raise HTTPException(status_code=400, detail="Update failed")
    return updated_data[0]

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

@router.post("/savings-goals/contribute/{goal_id}", response_model=SavingsGoalOut)
def contribute_to_savings_goal(goal_id: str, amount: float, token: str = Depends(oauth2)):
    """Add a contribution to a savings goal's saved_amount."""
    user_id = get_user_id(token)
    print(goal_id,amount)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Contribution amount must be positive")

    # Fetch goal to ensure it exists and belongs to the user
    goal_resp = supabase.table("savings_goals") \
        .select("saved_amount") \
        .eq("goal_id", goal_id) \
        .eq("student_id", user_id) \
        .single() \
        .execute()
    
    goal_data = getattr(goal_resp, "data", None)
    if not goal_data:
        raise HTTPException(status_code=404, detail="Savings goal not found")

    new_saved_amount = float(goal_data["saved_amount"] or 0) + amount

    # Update saved_amount
    update_resp = supabase.table("savings_goals") \
        .update({"saved_amount": new_saved_amount}) \
        .eq("goal_id", goal_id) \
        .eq("student_id", user_id) \
        .execute()
    
    updated_data = getattr(update_resp, "data", None)
    if not updated_data:
        raise HTTPException(status_code=400, detail="Failed to update savings goal")

    return updated_data[0]


@router.delete("/deletegoal/{goal_id}")
def delete_goal(goal_id: str, token: str = Depends(oauth2)):
    user_id = get_user_id(token)

    # Ensure the goal belongs to the logged-in student
    goal = supabase.table("savings_goals").select("*").eq("goal_id", goal_id).eq("student_id", user_id).execute()

    if not goal.data:
        raise HTTPException(status_code=404, detail="Goal not found or you don't have permission to delete it.")

    # Delete the goal
    supabase.table("savings_goals").delete().eq("goal_id", goal_id).execute()

    return {"message": "Goal deleted successfully"}


@router.get("/goal/{goal_id}")
def get_goal(goal_id: str):
    try:
        response = supabase.table("savings_goals").select(
            "goal_id, title, target_amount, saved_amount"
        ).eq("goal_id", goal_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Goal not found")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/editgoal/{goal_id}")
def update_goal(goal_id: str, payload: dict = Body(...)):
    try:
        # Only include provided fields
        update_data = {}
        if payload.get("title") is not None:
            update_data["title"] = payload["title"]
        if payload.get("target_amount") is not None:
            update_data["target_amount"] = payload["target_amount"]
        if payload.get("saved_amount") is not None:
            update_data["saved_amount"] = payload["saved_amount"]

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        # Supabase update
        response = supabase.table("savings_goals").update(update_data).eq("goal_id", goal_id).execute()

        # Debug logging for Supabase errors
        if hasattr(response, "error") and response.error:
            raise HTTPException(status_code=500, detail=response.error.message)

        if not response.data:
            raise HTTPException(status_code=404, detail="Goal not found")

        return {"message": "Goal updated successfully", "goal": response.data[0]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
