# ⚖️ Legal Pricing Service

A microservice built with **FastAPI** and **PostgreSQL** for calculating the cost of legal services.  
It provides reliable pricing logic, supports dynamic rules and tariffs, and is designed to integrate seamlessly with other services in a modular e‑commerce or SaaS architecture.

---

## 📦 Features

- Calculate service cost based on type, duration, and complexity  
- Support for dynamic pricing rules and tariff plans  
- API endpoints for price estimation and rule management  
- Integration-ready for order, billing, and user services  
- Alembic-powered migrations for schema evolution  

---

## ⚙️ Deployment

### 1. Environment setup
sudo nano .env
pip install -r requirements.txt
python -m app.main

###2. Database migrations
Generate a new migration:

bash
alembic revision --autogenerate -m "init"
Apply migrations:

bash
alembic upgrade head
🗂 Project Structure
app/db → database models, sessions, and pricing logic

app/api → FastAPI routes for pricing endpoints

app/schemas → Pydantic models for request/response validation

app/main.py → FastAPI app entry point

### 🛠 Tech Stack
Python 3.10+

FastAPI

PostgreSQL

SQLAlchemy

Alembic

Docker (optional)
