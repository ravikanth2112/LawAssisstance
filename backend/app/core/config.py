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
    
    # Database - SQL Server Express Configuration
    SQL_SERVER: str = Field(default="localhost\\SQLEXPRESS", env="SQL_SERVER")
    SQL_DATABASE: str = Field(default="ImmigrationLawDB", env="SQL_DATABASE")
    SQL_USERNAME: str = Field(default="", env="SQL_USERNAME") 
    SQL_PASSWORD: str = Field(default="", env="SQL_PASSWORD")
    
    # Database URL - Constructed for SQL Server Express
    @property
    def database_url(self) -> str:
        if self.SQL_USERNAME and self.SQL_PASSWORD:
            # SQL Server Authentication
            return f"mssql+pyodbc://{self.SQL_USERNAME}:{self.SQL_PASSWORD}@{self.SQL_SERVER}/{self.SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            # Windows Authentication (Trusted Connection)
            return f"mssql+pyodbc://@{self.SQL_SERVER}/{self.SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    # Fallback DATABASE_URL for manual override
    DATABASE_URL: str = Field(default="", env="DATABASE_URL")
    
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
