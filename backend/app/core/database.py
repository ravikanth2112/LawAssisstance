"""
Database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
database_url = settings.DATABASE_URL if settings.DATABASE_URL else settings.database_url

# SQL Server specific engine configuration
if "mssql" in database_url:
    engine = create_engine(
        database_url,
        # SQL Server specific options
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG  # Log SQL queries in debug mode
    )
else:
    # Fallback for other databases (like SQLite for development)
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
