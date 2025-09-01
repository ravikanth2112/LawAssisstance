"""
Immigration Law Dashboard - Phase 1 API
FastAPI backend for immigration law practice management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn

from app.routers import authentication, users, lawyers, clients, cases, dashboard
from app.core.database import engine, SessionLocal
from app.core.config import settings
from app.models import user, lawyer, client, case
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Creating database tables...")
    user.Base.metadata.create_all(bind=engine)
    lawyer.Base.metadata.create_all(bind=engine)
    client.Base.metadata.create_all(bind=engine)
    case.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    yield
    logger.info("Application shutdown")

# Create FastAPI application
app = FastAPI(
    title="Immigration Law Dashboard API",
    description="Phase 1 APIs for immigration law practice management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(authentication.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(lawyers.router, prefix="/api/lawyers", tags=["lawyers"])
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(cases.router, prefix="/api/cases", tags=["cases"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Immigration Law Dashboard API - Phase 1",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
