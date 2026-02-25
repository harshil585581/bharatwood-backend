import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Explicitly load environment variables from .env file and override any existing terminal cache
load_dotenv(override=True)

# Get the database URL from the environment directly
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Initialize the SQLAlchemy Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
