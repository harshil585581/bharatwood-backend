# FastAPI Backend

This is a production-ready FastAPI backend using PostgreSQL and Alembic for migrations.

## Setup Instructions

1. **Environment Setup**
   Ensure you have Python installed. The project uses a virtual environment located in `backend/venv`.
   If the `venv` does not exist or you need to recreate it:

   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate # Linux/Mac
   pip install -r requirements.txt
   ```

2. **Database Configuration**
   Copy `.env.example` to `.env` if it doesn't exist, and configure your PostgreSQL connection string:

   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/postgres
   ```

   Ensure your PostgreSQL server is running and the database specified in the URL exists.

3. **Database Migrations**
   The project uses Alembic to handle database schema changes.
   To generate an initial migration (after models are created/modified):

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

   To apply migrations to your database:

   ```bash
   alembic upgrade head
   ```

4. **Running the Server**
   You can run the application using `fastapi dev`:
   ```bash
   fastapi dev main.py
   ```
   Alternatively, using Uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```
   The API documentation will be available at `http://localhost:8000/docs`.

## Project Structure

- `main.py`: The entry point of the FastAPI application.
- `database.py`: Core SQLAlchemy engine and session management.
- `models/`: SQLAlchemy models representing database tables.
- `schemas/`: Pydantic models for data validation and API payloads.
- `routers/`: API route definitions by feature/resource.
- `alembic/`: Database migration configuration and versions.
