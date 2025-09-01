"""
Clients router - Client management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.client import Client
from app.schemas.client import ClientResponse, ClientCreate, ClientUpdate

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get clients (filtered by role)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Client).join(User).filter(User.is_active == True)
    
    # If lawyer, only show their assigned clients
    if current_user.role == "lawyer":
        # For now, show all clients - in full implementation, filter by lawyer assignment
        pass
    elif current_user.role == "client":
        # Clients can only see their own profile
        query = query.filter(Client.user_id == current_user.id)
    # Admin can see all
    
    clients = query.all()
    return [ClientResponse.model_validate(client) for client in clients]

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client_by_id(
    client_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get client by ID"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Check access permissions
    if current_user.role == "client" and client.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    # For lawyer role, in full implementation check if this client is assigned to the lawyer
    
    return ClientResponse.model_validate(client)

@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create new client"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can create client profiles
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can create client profiles"
        )
    
    # Check if user exists and is a client
    user = db.query(User).filter(User.user_id == client_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.user_type != "client":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be of type 'client'"
        )
    
    # Check if client profile already exists
    existing_client = db.query(Client).filter(Client.user_id == client_data.user_id).first()
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client profile already exists for this user"
        )
    
    # Create client profile
    client = Client(**client_data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    
    return ClientResponse.model_validate(client)

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_update: ClientUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update client"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Check access permissions
    if current_user.role == "client" and client.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    # For lawyer role, in full implementation check if this client is assigned to the lawyer
    
    # Update client fields
    update_data = client_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    
    return ClientResponse.model_validate(client)

@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete client (admin only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can delete client profiles
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete client profiles"
        )
    
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    db.delete(client)
    db.commit()
    
    return {"message": "Client profile deleted successfully"}