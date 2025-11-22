
import pytest
from fastapi.testclient import TestClient
from main import app, fake_users_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db_state():
    """Reset the fake_users_db to its initial state before each test."""
    original_state = {
        "alice": {"pin_number": "1234", "bank_balance": 1000.00},
        "bob": {"pin_number": "5678", "bank_balance": 2500.50},
        "charlie": {"pin_number": "1111", "bank_balance": 500.00},
    }
    for user, data in original_state.items():
        fake_users_db[user] = data.copy()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_read_item():
    response = client.get("/items/1?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": "test"}

def test_read_item_no_query():
    response = client.get("/items/2")
    assert response.status_code == 200
    assert response.json() == {"item_id": 2, "q": None}

def test_authenticate_success():
    response = client.post("/authenticate", json={"name": "alice", "pin_number": "1234"})
    assert response.status_code == 200
    assert response.json() == {"bank_balance": 1000.00}

def test_authenticate_failure_wrong_pin():
    response = client.post("/authenticate", json={"name": "alice", "pin_number": "9999"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_authenticate_failure_wrong_name():
    response = client.post("/authenticate", json={"name": "charlie", "pin_number": "1234"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_bank_transfer_success():
    response = client.post(
        "/bank-transfer",
        json={"sender_name": "alice", "receiver_name": "bob", "pin_number": "1234", "amount": 200.00}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Transfer of 200.0 from alice to bob successful.",
        "sender_new_balance": 800.00,
    }
    assert fake_users_db["alice"]["bank_balance"] == 800.00
    assert fake_users_db["bob"]["bank_balance"] == 2700.50

def test_bank_transfer_invalid_sender_pin():
    response = client.post(
        "/bank-transfer",
        json={"sender_name": "alice", "receiver_name": "bob", "pin_number": "9999", "amount": 200.00}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid sender credentials"}
    assert fake_users_db["alice"]["bank_balance"] == 1000.00
    assert fake_users_db["bob"]["bank_balance"] == 2500.50

def test_bank_transfer_receiver_not_found():
    response = client.post(
        "/bank-transfer",
        json={"sender_name": "alice", "receiver_name": "dave", "pin_number": "1234", "amount": 200.00}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Receiver not found"}
    assert fake_users_db["alice"]["bank_balance"] == 1000.00

def test_bank_transfer_insufficient_funds():
    response = client.post(
        "/bank-transfer",
        json={"sender_name": "alice", "receiver_name": "bob", "pin_number": "1234", "amount": 1200.00}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient funds"}
    assert fake_users_db["alice"]["bank_balance"] == 1000.00
    assert fake_users_db["bob"]["bank_balance"] == 2500.50

def test_deposit_success():
    response = client.post("/deposit", json={"name": "alice", "amount": 500.00})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Deposit of 500.0 for alice successful.",
        "new_balance": 1500.00,
    }
    assert fake_users_db["alice"]["bank_balance"] == 1500.00

def test_deposit_user_not_found():
    response = client.post("/deposit", json={"name": "dave", "amount": 500.00})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_deposit_negative_amount():
    response = client.post("/deposit", json={"name": "alice", "amount": -100.00})
    assert response.status_code == 400
    assert response.json() == {"detail": "Deposit amount must be positive"}
    assert fake_users_db["alice"]["bank_balance"] == 1000.00

def test_deposit_zero_amount():
    response = client.post("/deposit", json={"name": "alice", "amount": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Deposit amount must be positive"}
    assert fake_users_db["alice"]["bank_balance"] == 1000.00

