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

# Clean leading/trailing whitespace and quotes (common in Docker env configs)
DATABASE_URL = DATABASE_URL.strip().strip("'\"")

# Safe debug log (hides password)
try:
    if "@" in DATABASE_URL:
        db_parts = DATABASE_URL.split("@", 1)
        scheme_user = db_parts[0]
        host_db = db_parts[1]
        if ":" in scheme_user:
            scheme_user_parts = scheme_user.rsplit(":", 1)
            scheme_user = scheme_user_parts[0] + ":***"
        print(f"DATABASE_URL (local check): {scheme_user}@{host_db}", flush=True)
    else:
        print(f"DATABASE_URL (local check): {DATABASE_URL}", flush=True)
except Exception:
    pass

# SQLAlchemy 1.4+ requires 'postgresql://' instead of 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Initialize the SQLAlchemy Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
