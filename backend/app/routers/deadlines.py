"""
Deadlines router - Deadline management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.deadline import Deadline
from app.schemas.deadline import DeadlineResponse, DeadlineCreate, DeadlineUpdate, DeadlineComplete

router = APIRouter()
security = HTTPBearer()

@router.get("/upcoming", response_model=List[DeadlineResponse])
async def get_upcoming_deadlines(
    days: int = Query(7, description="Number of days to look ahead"),
    priority: Optional[str] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get upcoming deadlines (?days=7, priority filtering)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Calculate date range
    today = date.today()
    end_date = today + timedelta(days=days)
    
    query = db.query(Deadline).filter(
        Deadline.due_date >= today,
        Deadline.due_date <= end_date,
        Deadline.status == "pending"
    )
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Deadline.lawyer_id == current_user.id)
    elif current_user.role == "client":
        # Clients see deadlines for their cases
        from app.models.case import Case
        query = query.join(Case).filter(Case.client_id == current_user.id)
    
    # Priority filtering
    if priority:
        query = query.filter(Deadline.priority_level == priority)
    
    deadlines = query.order_by(Deadline.due_date).all()
    
    # Add computed properties
    for deadline in deadlines:
        deadline.is_overdue = deadline.is_overdue
        deadline.days_remaining = deadline.days_remaining
    
    return [DeadlineResponse.model_validate(deadline) for deadline in deadlines]

@router.get("/overdue", response_model=List[DeadlineResponse])
async def get_overdue_deadlines(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get overdue deadlines (Automatic status tracking)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    today = date.today()
    query = db.query(Deadline).filter(
        Deadline.due_date < today,
        Deadline.status == "pending"
    )
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Deadline.lawyer_id == current_user.id)
    elif current_user.role == "client":
        from app.models.case import Case
        query = query.join(Case).filter(Case.client_id == current_user.id)
    
    # Auto-update status to overdue
    overdue_deadlines = query.all()
    for deadline in overdue_deadlines:
        deadline.status = "overdue"
        deadline.is_overdue = True
        deadline.days_remaining = deadline.days_remaining
    
    db.commit()
    
    return [DeadlineResponse.model_validate(deadline) for deadline in overdue_deadlines]

@router.get("/", response_model=List[DeadlineResponse])
async def get_deadlines(
    case_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all deadlines with filtering"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Deadline)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Deadline.lawyer_id == current_user.id)
    elif current_user.role == "client":
        from app.models.case import Case
        query = query.join(Case).filter(Case.client_id == current_user.id)
    
    # Apply filters
    if case_id:
        query = query.filter(Deadline.case_id == case_id)
    if status:
        query = query.filter(Deadline.status == status)
    if priority:
        query = query.filter(Deadline.priority_level == priority)
    
    deadlines = query.order_by(Deadline.due_date).all()
    
    # Add computed properties
    for deadline in deadlines:
        deadline.is_overdue = deadline.is_overdue
        deadline.days_remaining = deadline.days_remaining
    
    return [DeadlineResponse.model_validate(deadline) for deadline in deadlines]

@router.post("/", response_model=DeadlineResponse)
async def create_deadline(
    deadline_data: DeadlineCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create deadline (Court deadline flag, priority levels)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can create deadlines
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can create deadlines"
        )
    
    # Create deadline
    deadline = Deadline(
        **deadline_data.model_dump(),
        created_by=current_user.id
    )
    db.add(deadline)
    db.commit()
    db.refresh(deadline)
    
    # Add computed properties
    deadline.is_overdue = deadline.is_overdue
    deadline.days_remaining = deadline.days_remaining
    
    return DeadlineResponse.model_validate(deadline)

@router.get("/{deadline_id}", response_model=DeadlineResponse)
async def get_deadline_by_id(
    deadline_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get deadline by ID"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    deadline = db.query(Deadline).filter(Deadline.deadline_id == deadline_id).first()
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    
    # Check access permissions
    if current_user.role == "lawyer" and deadline.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    elif current_user.role == "client":
        from app.models.case import Case
        case = db.query(Case).filter(Case.case_id == deadline.case_id).first()
        if not case or case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    # Add computed properties
    deadline.is_overdue = deadline.is_overdue
    deadline.days_remaining = deadline.days_remaining
    
    return DeadlineResponse.model_validate(deadline)

@router.put("/{deadline_id}", response_model=DeadlineResponse)
async def update_deadline(
    deadline_id: int,
    deadline_update: DeadlineUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update deadline"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    deadline = db.query(Deadline).filter(Deadline.deadline_id == deadline_id).first()
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    
    # Check permissions
    if current_user.role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot update deadlines"
        )
    
    if current_user.role == "lawyer" and deadline.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update deadline fields
    update_data = deadline_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(deadline, field, value)
    
    db.commit()
    db.refresh(deadline)
    
    # Add computed properties
    deadline.is_overdue = deadline.is_overdue
    deadline.days_remaining = deadline.days_remaining
    
    return DeadlineResponse.model_validate(deadline)

@router.put("/{deadline_id}/complete", response_model=DeadlineResponse)
async def mark_deadline_complete(
    deadline_id: int,
    completion_data: DeadlineComplete,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Mark deadline as completed (Timestamp tracking)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    deadline = db.query(Deadline).filter(Deadline.deadline_id == deadline_id).first()
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    
    # Check permissions
    if current_user.role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot complete deadlines"
        )
    
    if current_user.role == "lawyer" and deadline.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Mark as completed
    deadline.status = "completed"
    deadline.completed_date = date.today()
    if completion_data.completion_notes:
        deadline.completion_notes = completion_data.completion_notes
    
    db.commit()
    db.refresh(deadline)
    
    # Add computed properties
    deadline.is_overdue = deadline.is_overdue
    deadline.days_remaining = deadline.days_remaining
    
    return DeadlineResponse.model_validate(deadline)

@router.delete("/{deadline_id}")
async def delete_deadline(
    deadline_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete deadline (admin/lawyer only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can delete deadlines
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can delete deadlines"
        )
    
    deadline = db.query(Deadline).filter(Deadline.deadline_id == deadline_id).first()
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    
    # Check permissions
    if current_user.role == "lawyer" and deadline.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(deadline)
    db.commit()
    
    return {"message": "Deadline deleted successfully"}
