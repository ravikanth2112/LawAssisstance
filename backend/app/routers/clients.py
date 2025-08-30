from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import User, Client, UserType
from app.schemas import ClientCreate, ClientUpdate, ClientResponse, ClientWithUser
from app.routers.auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter()

def generate_client_number():
    """Generate a unique client number."""
    return f"CL{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"

@router.get("/", response_model=dict)
async def get_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all clients with pagination and filtering."""
    query = db.query(Client).join(User).filter(User.is_active == True)
    
    # Apply filters
    if search:
        query = query.filter(
            (User.first_name.ilike(f"%{search}%")) |
            (User.last_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%")) |
            (Client.client_number.ilike(f"%{search}%"))
        )
    
    if country:
        query = query.filter(Client.country_of_origin.ilike(f"%{country}%"))
    
    if status:
        query = query.filter(Client.current_status.ilike(f"%{status}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    clients = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": [
            {
                "client_id": client.client_id,
                "user_id": client.user_id,
                "client_number": client.client_number,
                "country_of_origin": client.country_of_origin,
                "current_status": client.current_status,
                "preferred_language": client.preferred_language,
                "date_of_birth": client.date_of_birth.isoformat() if client.date_of_birth else None,
                "emergency_contact": client.emergency_contact,
                "emergency_phone": client.emergency_phone,
                "notes": client.notes,
                "created_at": client.created_at.isoformat(),
                "updated_at": client.updated_at.isoformat(),
                "user": {
                    "email": client.user.email,
                    "first_name": client.user.first_name,
                    "last_name": client.user.last_name,
                    "phone": client.user.phone
                } if client.user else None
            } for client in clients
        ],
        "pagination": {
            "page": (skip // limit) + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        },
        "message": "Clients retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/", response_model=dict)
async def create_client(
    client_data: ClientCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new client profile."""
    # Check if user exists and is not already a client
    user = db.query(User).filter(User.user_id == client_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.user_type != UserType.CLIENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have client user type"
        )
    
    # Check if client profile already exists
    existing_client = db.query(Client).filter(Client.user_id == client_data.user_id).first()
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client profile already exists for this user"
        )
    
    # Generate unique client number
    client_number = client_data.client_number or generate_client_number()
    
    # Check if client number is unique
    existing_number = db.query(Client).filter(Client.client_number == client_number).first()
    if existing_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client number already exists"
        )
    
    # Create client profile
    db_client = Client(
        user_id=client_data.user_id,
        client_number=client_number,
        country_of_origin=client_data.country_of_origin,
        current_status=client_data.current_status,
        preferred_language=client_data.preferred_language,
        date_of_birth=client_data.date_of_birth,
        emergency_contact=client_data.emergency_contact,
        emergency_phone=client_data.emergency_phone,
        notes=client_data.notes
    )
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return {
        "success": True,
        "data": {
            "client_id": db_client.client_id,
            "user_id": db_client.user_id,
            "client_number": db_client.client_number,
            "country_of_origin": db_client.country_of_origin,
            "current_status": db_client.current_status,
            "preferred_language": db_client.preferred_language,
            "date_of_birth": db_client.date_of_birth.isoformat() if db_client.date_of_birth else None,
            "emergency_contact": db_client.emergency_contact,
            "emergency_phone": db_client.emergency_phone,
            "notes": db_client.notes,
            "created_at": db_client.created_at.isoformat(),
            "updated_at": db_client.updated_at.isoformat()
        },
        "message": "Client profile created successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/{client_id}", response_model=dict)
async def get_client(
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get client by ID."""
    client = db.query(Client).join(User).filter(
        Client.client_id == client_id,
        User.is_active == True
    ).first()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Check permissions (admin, lawyer, or self)
    if (current_user.user_type not in [UserType.ADMIN, UserType.LAWYER] and 
        current_user.user_id != client.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {
        "success": True,
        "data": {
            "client_id": client.client_id,
            "user_id": client.user_id,
            "client_number": client.client_number,
            "country_of_origin": client.country_of_origin,
            "current_status": client.current_status,
            "preferred_language": client.preferred_language,
            "date_of_birth": client.date_of_birth.isoformat() if client.date_of_birth else None,
            "emergency_contact": client.emergency_contact,
            "emergency_phone": client.emergency_phone,
            "notes": client.notes,
            "created_at": client.created_at.isoformat(),
            "updated_at": client.updated_at.isoformat(),
            "user": {
                "email": client.user.email,
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "phone": client.user.phone
            } if client.user else None
        },
        "message": "Client retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.put("/{client_id}", response_model=dict)
async def update_client(
    client_id: int,
    client_update: ClientUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update client profile."""
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Check permissions (admin, lawyer, or self)
    if (current_user.user_type not in [UserType.ADMIN, UserType.LAWYER] and 
        current_user.user_id != client.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = client_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    
    return {
        "success": True,
        "data": {
            "client_id": client.client_id,
            "user_id": client.user_id,
            "client_number": client.client_number,
            "country_of_origin": client.country_of_origin,
            "current_status": client.current_status,
            "preferred_language": client.preferred_language,
            "date_of_birth": client.date_of_birth.isoformat() if client.date_of_birth else None,
            "emergency_contact": client.emergency_contact,
            "emergency_phone": client.emergency_phone,
            "notes": client.notes,
            "created_at": client.created_at.isoformat(),
            "updated_at": client.updated_at.isoformat()
        },
        "message": "Client profile updated successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.delete("/{client_id}", response_model=dict)
async def delete_client(
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete client profile (Admin only)."""
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Soft delete by deactivating the user
    user = db.query(User).filter(User.user_id == client.user_id).first()
    if user:
        user.is_active = False
    
    db.commit()
    
    return {
        "success": True,
        "data": {},
        "message": "Client deleted successfully",
        "timestamp": datetime.utcnow().isoformat()
    }
