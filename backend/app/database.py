# Database configuration and session management for Agent Reality Map Backend
# Uses SQLite with SQLAlchemy ORM for production-grade data persistence

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
import os

# Database file location (project root for easy access)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = BASE_DIR / "agent-reality-map-backend.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine with check_same_thread=False for FastAPI async compatibility
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL query debugging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

# Dependency for FastAPI endpoints to get database session
def get_db():
    """
    FastAPI dependency that provides a database session.
    Automatically handles session lifecycle (commit/rollback/close).

    Usage:
        @app.get("/agents/")
        def get_agents(db: Session = Depends(get_db)):
            return db.query(Agent).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database (create all tables)
def init_db():
    """
    Create all database tables defined in models.
    Call this on application startup.
    """
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DATABASE_PATH}")
