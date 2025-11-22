# 🏦 Banking App with FastAPI + Gemini CLI

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Enabled-orange)

This project is a simple banking system using FastAPI and Gemini CLI.  
Users can:
- Authenticate and check bank balance
- Deposit money
- Transfer money to other users

## Features
1. `/authenticate` → Login & view bank balance
2. `/deposit` → Add money to user account
3. `/bank-transfer` → Transfer money from sender to receiver

## Gemini CLI Workflow
1. Start CLI: `gemini start` → create new project
2. Choose tech stack: `FastAPI`
3. Optional: Create/Activate virtual environment
4. Generate modules: `auth`, `deposit`, `transfer`
5. Generate endpoints via prompts:
   - `/authenticate`
   - `/deposit`
   - `/bank-transfer`

## Demo Users
```python
users = {
    "Ali": {"pin": "1234", "bank_balance": 5000},
    "Sara": {"pin": "4321", "bank_balance": 2000},
}



