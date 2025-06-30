# 📦 FastAPI App

A backend project built with **FastAPI**, using **SQLAlchemy**, **JWT Authentication**, and **SQLite** for storage. Asynchronous operations are handled via aiosqlite and Telethon for Telegram API
interactions.

---

## Getting Started

1. Make sure you have Python 3.10+ installed on your machine. Run `python --version` in your terminal. If it shows a version (e.g., v3.10), Python is installed.
   [Download and install Python](https://www.python.org/downloads/) if needed.
2. Clone this repository.
3. Create and activate a virtual environment: `python -m venv venv`. Run `venv\Scripts\activate` (for Windows),`source venv/bin/activate` (for macOS/Linux)
4. Install project dependencies by running `pip install -r requirements.txt`.
5. Fill in the .env file based on .env.example.
6. Start the development server with `python main.py`.
7. Open your browser and go to [http://localhost:8000](http://localhost:8000). Docs [http://localhost:8000/docs](http://localhost:8000/docs)

## 🚀 Technologies

- **FastAPI** — modern Python web framework
- **Uvicorn** — ASGI server for FastAPI
- **SQLAlchemy** — ORM for database operations
- **aiosqlite** — async SQLite adapter
- **RPyJWT** — JSON Web Token auth
- **PassLib / bcrypt** — secure password hashing
- **python-dotenv** — load environment variables from .env
- **Pydantic** — data validation and settings management
- **Telethon** — Telegram API client

---

## 📁 Project Structure

- fastapi-app/
- ├── app/
- │ ├── api/ # Route definitions
- │ ├── core/ # Settings and configuration
- │ ├── db/ # Database models and session
- │ ├── schemas/ # Pydantic models
- │ ├── services/ # Business logic and utilities
- │ ├── auth/ # JWT logic and password hashing
- │ └── telegram/ # Telethon session management
- ├── .env # Environment variables
- ├── main.py # Entry point
- ├── requirements.txt # Dependencies
- └── README.md

## 🔐 Authentication

- JWT (HS256)
- Passwords are securely hashed using bcrypt and passlib
- Include the JWT token in the Authorization header as Bearer <token> for protected endpoints

## 📬 Telegram Integration

- Uses Telethon to manage Telegram sessions and communicate with Telegram API
- Telegram clients are stored per user and reused from session
