from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserLogin, Token, UserCreate, UserResponse
from app.utils.auth import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        user_type=user_data.user_type
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create tokens
    token_data = {
        "sub": db_user.email,
        "user_id": db_user.user_id,
        "user_type": db_user.user_type.value
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {
        "success": True,
        "data": {
            "user": {
                "user_id": db_user.user_id,
                "email": db_user.email,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "user_type": db_user.user_type.value
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        "message": "User registered successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/login", response_model=dict)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return tokens."""
    # Find user
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    
    # Create tokens
    token_data = {
        "sub": user.email,
        "user_id": user.user_id,
        "user_type": user.user_type.value
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {
        "success": True,
        "data": {
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_type": user.user_type.value
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        "message": "Login successful",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/refresh-token", response_model=dict)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    token = credentials.credentials
    
    # Verify refresh token
    payload = verify_token(token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user
    user = db.query(User).filter(User.email == payload["email"]).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    token_data = {
        "sub": user.email,
        "user_id": user.user_id,
        "user_type": user.user_type.value
    }
    
    access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    
    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        },
        "message": "Token refreshed successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user."""
    token = credentials.credentials
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = db.query(User).filter(User.email == payload["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return {
        "success": True,
        "data": {
            "user_id": current_user.user_id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "phone": current_user.phone,
            "user_type": current_user.user_type.value,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at.isoformat(),
            "updated_at": current_user.updated_at.isoformat()
        },
        "message": "User profile retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }
