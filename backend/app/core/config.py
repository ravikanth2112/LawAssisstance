"""
Configuration settings for Immigration Law Dashboard API
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Immigration Law Dashboard API"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=True, env="DEBUG")
    HOST: str = Field(default="127.0.0.1", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./immigration_law.db",
        env="DATABASE_URL"
    )
    
    # For SQL Server (uncomment when ready)
    # SQL_SERVER: str = Field(default="localhost", env="SQL_SERVER")
    # SQL_DATABASE: str = Field(default="ImmigrationLawDB", env="SQL_DATABASE")
    # SQL_USERNAME: str = Field(default="", env="SQL_USERNAME")
    # SQL_PASSWORD: str = Field(default="", env="SQL_PASSWORD")
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-here-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()
