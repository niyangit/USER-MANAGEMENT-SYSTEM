# FastAPI User Management System

A User Management System built with FastAPI.

## Features

- User Registration
- User Login
- JWT Authentication
- Role-Based Access Control (RBAC)
- Forgot Password (OTP)
- Forgot Password (Email Link)
- Password Reset
- SQLAlchemy ORM
- MySQL Database
- Connection Pooling
- Rate Limiting
- TTL Cache
- Multiprocessing using Uvicorn Workers

## Tech Stack

- FastAPI
- SQLAlchemy
- MySQL
- JWT
- Python
- Uvicorn

## Installation

```bash
git clone <repository-url>

cd Fastapi-mysql

python -m venv env

env\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

## Environment Variables

Create a `.env` file and add:

```env
MYSQL_DATABASE_URL=...
SECRET_KEY=...
EMAIL_ADDRESS=...
EMAIL_PASSWORD=...
```