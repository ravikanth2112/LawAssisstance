"""
Cases router - Case management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.case import Case
from app.schemas.case import CaseResponse, CaseCreate, CaseUpdate

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[CaseResponse])
async def get_cases(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    lawyer_id: Optional[int] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all cases (filtered by user role)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Case)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        # For now, show all cases - in full implementation, filter by lawyer assignment
        pass
    elif current_user.role == "client":
        # Clients can only see their own cases
        query = query.filter(Case.client_id == current_user.id)
    # Admin can see all
    
    # Apply filters
    if status_filter:
        query = query.filter(Case.case_status == status_filter)
    if priority:
        query = query.filter(Case.priority_level == priority)
    if lawyer_id:
        query = query.filter(Case.primary_lawyer_id == lawyer_id)
    
    cases = query.all()
    return [CaseResponse.model_validate(case) for case in cases]

@router.get("/statistics")
async def get_case_statistics(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Case statistics for dashboard"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Case)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        # For now, show all cases - in full implementation, filter by lawyer assignment
        pass
    elif current_user.role == "client":
        # Clients can only see their own cases
        query = query.filter(Case.client_id == current_user.id)
    
    total_cases = query.count()
    active_cases = query.filter(Case.case_status.in_(["active", "in_progress"])).count()
    completed_cases = query.filter(Case.case_status == "completed").count()
    pending_cases = query.filter(Case.case_status == "pending").count()
    
    # Case distribution by status
    status_distribution = {
        "active": active_cases,
        "completed": completed_cases,
        "pending": pending_cases,
        "total": total_cases
    }
    
    return {
        "total": total_cases,
        "active": active_cases,
        "completed": completed_cases,
        "pending": pending_cases,
        "by_status": status_distribution
    }

@router.get("/{case_id}", response_model=CaseResponse)
async def get_case_by_id(
    case_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get case details (includes client, lawyers, deadlines)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Check access permissions
    if current_user.role == "client" and case.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    # For lawyer role, in full implementation check if this case is assigned to the lawyer
    
    return CaseResponse.model_validate(case)

@router.post("/", response_model=CaseResponse)
async def create_case(
    case_data: CaseCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create new case"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can create cases
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can create cases"
        )
    
    # Create case
    case = Case(**case_data.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    
    return CaseResponse.model_validate(case)

@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: int,
    case_update: CaseUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update case"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Check access permissions
    if current_user.role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot update cases"
        )
    # For lawyer role, in full implementation check if this case is assigned to the lawyer
    
    # Update case fields
    update_data = case_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)
    
    db.commit()
    db.refresh(case)
    
    return CaseResponse.model_validate(case)

@router.delete("/{case_id}")
async def delete_case(
    case_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete case (admin only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can delete cases
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete cases"
        )
    
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    db.delete(case)
    db.commit()
    
    return {"message": "Case deleted successfully"}

@router.post("/{case_id}/lawyers")
async def assign_lawyer_to_case(
    case_id: int,
    lawyer_assignment: dict,  # Should contain lawyer_id and role (primary/secondary)
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Assign lawyer to case"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can assign lawyers to cases
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can assign lawyers to cases"
        )
    
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    lawyer_id = lawyer_assignment.get("lawyer_id")
    role = lawyer_assignment.get("role", "primary")
    
    if role == "primary":
        case.primary_lawyer_id = lawyer_id
    # In full implementation, handle secondary lawyers via separate table
    
    db.commit()
    db.refresh(case)
    
    return {"message": f"Lawyer {lawyer_id} assigned as {role} lawyer to case {case_id}"}