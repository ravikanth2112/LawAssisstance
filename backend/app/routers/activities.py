"""
Activities router - Activity tracking and billable hours management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date, datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.activity import Activity
from app.schemas.activity import ActivityResponse, ActivityCreate, ActivityUpdate

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    case_id: Optional[int] = Query(None),
    activity_type: Optional[str] = Query(None),
    is_billable: Optional[bool] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get activities with filtering (Date range, case, type, billable status)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Activity)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Activity.lawyer_id == current_user.id)
    elif current_user.role == "client":
        # Clients can only see activities for their cases
        from app.models.case import Case
        user_cases = db.query(Case.case_id).filter(Case.client_id == current_user.id).subquery()
        query = query.filter(Activity.case_id.in_(user_cases))
    
    # Apply filters
    if case_id:
        query = query.filter(Activity.case_id == case_id)
    if activity_type:
        query = query.filter(Activity.activity_type == activity_type)
    if is_billable is not None:
        query = query.filter(Activity.is_billable == is_billable)
    if date_from:
        query = query.filter(Activity.activity_date >= date_from)
    if date_to:
        query = query.filter(Activity.activity_date <= date_to)
    
    activities = query.order_by(Activity.activity_date.desc()).all()
    
    # Add computed properties
    for activity in activities:
        activity.billable_amount = activity.billable_amount
    
    return [ActivityResponse.model_validate(activity) for activity in activities]

@router.get("/summary", response_model=dict)
async def get_activities_summary(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    case_id: Optional[int] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get activity summary (Total hours, billable vs non-billable, amounts)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Activity)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Activity.lawyer_id == current_user.id)
    elif current_user.role == "client":
        # Clients can only see activities for their cases
        from app.models.case import Case
        user_cases = db.query(Case.case_id).filter(Case.client_id == current_user.id).subquery()
        query = query.filter(Activity.case_id.in_(user_cases))
    
    # Apply date filters
    if date_from:
        query = query.filter(Activity.activity_date >= date_from)
    if date_to:
        query = query.filter(Activity.activity_date <= date_to)
    if case_id:
        query = query.filter(Activity.case_id == case_id)
    
    activities = query.all()
    
    # Calculate summary statistics
    total_hours = sum(activity.duration_hours for activity in activities)
    billable_hours = sum(activity.duration_hours for activity in activities if activity.is_billable)
    non_billable_hours = total_hours - billable_hours
    
    total_billable_amount = sum(activity.billable_amount for activity in activities if activity.is_billable)
    
    # Activity type breakdown
    type_breakdown = {}
    for activity in activities:
        activity_type = activity.activity_type
        if activity_type not in type_breakdown:
            type_breakdown[activity_type] = {
                "total_hours": 0,
                "billable_hours": 0,
                "billable_amount": 0
            }
        
        type_breakdown[activity_type]["total_hours"] += activity.duration_hours
        if activity.is_billable:
            type_breakdown[activity_type]["billable_hours"] += activity.duration_hours
            type_breakdown[activity_type]["billable_amount"] += activity.billable_amount
    
    return {
        "total_hours": total_hours,
        "billable_hours": billable_hours,
        "non_billable_hours": non_billable_hours,
        "total_billable_amount": total_billable_amount,
        "activity_types": type_breakdown,
        "total_activities": len(activities)
    }

@router.post("/", response_model=ActivityResponse)
async def create_activity(
    activity_data: ActivityCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create activity record (Time tracking, case association)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can create activities
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can create activities"
        )
    
    # Verify case access if case_id provided
    if activity_data.case_id:
        from app.models.case import Case
        case = db.query(Case).filter(Case.case_id == activity_data.case_id).first()
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        # Check if lawyer has access to the case
        if current_user.role == "lawyer" and case.primary_lawyer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this case"
            )
    
    # Create activity record
    activity_dict = activity_data.model_dump()
    activity_dict['lawyer_id'] = current_user.id
    
    activity = Activity(**activity_dict)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    # Add computed properties
    activity.billable_amount = activity.billable_amount
    
    return ActivityResponse.model_validate(activity)

@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity_by_id(
    activity_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get activity by ID"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    activity = db.query(Activity).filter(Activity.activity_id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check access permissions
    if current_user.role == "lawyer" and activity.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    elif current_user.role == "client":
        # Check if client has access through case
        from app.models.case import Case
        case = db.query(Case).filter(Case.case_id == activity.case_id).first()
        if not case or case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    # Add computed properties
    activity.billable_amount = activity.billable_amount
    
    return ActivityResponse.model_validate(activity)

@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update activity record"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    activity = db.query(Activity).filter(Activity.activity_id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions - only the lawyer who created it or admin can edit
    if current_user.role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot update activities"
        )
    
    if current_user.role == "lawyer" and activity.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update activity fields
    update_data = activity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    # Add computed properties
    activity.billable_amount = activity.billable_amount
    
    return ActivityResponse.model_validate(activity)

@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete activity record"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    activity = db.query(Activity).filter(Activity.activity_id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions - only the lawyer who created it or admin can delete
    if current_user.role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot delete activities"
        )
    
    if current_user.role == "lawyer" and activity.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(activity)
    db.commit()
    
    return {"message": "Activity deleted successfully"}

@router.get("/billable/pending")
async def get_pending_billable_activities(
    case_id: Optional[int] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get pending billable activities (Not yet billed)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can see billable activities
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can view billable activities"
        )
    
    query = db.query(Activity).filter(
        and_(
            Activity.is_billable == True,
            Activity.billed == False
        )
    )
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Activity.lawyer_id == current_user.id)
    
    if case_id:
        query = query.filter(Activity.case_id == case_id)
    
    activities = query.order_by(Activity.activity_date.desc()).all()
    
    # Calculate totals
    total_hours = sum(activity.duration_hours for activity in activities)
    total_amount = sum(activity.billable_amount for activity in activities)
    
    # Add computed properties
    for activity in activities:
        activity.billable_amount = activity.billable_amount
    
    return {
        "activities": [ActivityResponse.model_validate(activity) for activity in activities],
        "total_pending_hours": total_hours,
        "total_pending_amount": total_amount,
        "count": len(activities)
    }
