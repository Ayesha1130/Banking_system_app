# GEMINI.md

# Project Name: Banking App
# Tech Stack: FastAPI
# CLI: Gemini CLI
# Description: Simple Banking System with Authenticate, Deposit, and Bank Transfer endpoints

---

## 1️⃣ Project Structure

- **Root Folder**
  - `main.py` → Main FastAPI application file
  - `modules/` → Contains modular features
    - `auth.py` → Authentication module
    - `deposit.py` → Deposit module
    - `transfer.py` → Bank transfer module
  - `tests/` → Contains test scripts
    - `test_main.py`
  - `GEMINI.md` → CLI configuration and project rules

---

## 2️⃣ Modules and Endpoints

### 2.1 Auth Module
- Endpoint: `/authenticate`  
- Method: POST  
- Request: `name` & `pin_number`  
- Response: `bank_balance`  
- Rules:
  - Authenticate user
  - Return 401 if credentials invalid

### 2.2 Deposit Module
- Endpoint: `/deposit`  
- Method: POST  
- Request: `name` & `amount`  
- Response: `message`, `new_balance`  
- Rules:
  - Only positive deposit allowed
  - Return 404 if user not found

### 2.3 Bank Transfer Module
- Endpoint: `/bank-transfer`  
- Method: POST  
- Request: `sender_name`, `receiver_name`, `pin_number`, `amount`  
- Response: `message`, `sender_new_balance`  
- Rules:
  - Authenticate sender using `pin_number`
  - Check sufficient balance
  - Return 404 if receiver not found
  - Deduct sender, add to receiver

---

## 3️⃣ Users & Data
- In-memory users dictionary:

```python
fake_users_db = {
    "alice": {"pin_number": "1234", "bank_balance": 1000.00},
    "bob": {"pin_number": "5678", "bank_balance": 2500.50},
    "charlie": {"pin_number": "1111", "bank_balance": 500.00},
}
