
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Dummy user data for demonstration
fake_users_db = {
    "alice": {"pin_number": "1234", "bank_balance": 1000.00},
    "bob": {"pin_number": "5678", "bank_balance": 2500.50},
    "charlie": {"pin_number": "1111", "bank_balance": 500.00},
}

class AuthRequest(BaseModel):
    name: str
    pin_number: str

class TransferRequest(BaseModel):
    sender_name: str
    receiver_name: str
    pin_number: str
    amount: float

class DepositRequest(BaseModel):
    name: str
    amount: float

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/authenticate")
async def authenticate_user(auth_request: AuthRequest):
    user = fake_users_db.get(auth_request.name)
    if not user or user["pin_number"] != auth_request.pin_number:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"bank_balance": user["bank_balance"]}

@app.post("/bank-transfer")
async def bank_transfer(transfer_request: TransferRequest):
    sender = fake_users_db.get(transfer_request.sender_name)
    receiver = fake_users_db.get(transfer_request.receiver_name)

    # Authenticate sender
    if not sender or sender["pin_number"] != transfer_request.pin_number:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid sender credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if receiver exists
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found",
        )

    # Check for sufficient funds
    if sender["bank_balance"] < transfer_request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds",
        )
    
    # Perform the transfer
    sender["bank_balance"] -= transfer_request.amount
    receiver["bank_balance"] += transfer_request.amount

    return {
        "message": f"Transfer of {transfer_request.amount} from {transfer_request.sender_name} to {transfer_request.receiver_name} successful.",
        "sender_new_balance": sender["bank_balance"],
    }

@app.post("/deposit")
async def deposit(deposit_request: DepositRequest):
    user = fake_users_db.get(deposit_request.name)

    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check for positive deposit amount
    if deposit_request.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deposit amount must be positive",
        )

    # Perform the deposit
    user["bank_balance"] += deposit_request.amount

    return {
        "message": f"Deposit of {deposit_request.amount} for {deposit_request.name} successful.",
        "new_balance": user["bank_balance"],
    }

