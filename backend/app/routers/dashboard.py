"""
Dashboard router - Dashboard statistics and analytics endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.lawyer import Lawyer
from app.models.client import Client
from app.models.case import Case

router = APIRouter()
security = HTTPBearer()

@router.get("/stats")
async def get_dashboard_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dashboard statistics - KPIs, recent activities, alerts"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Base queries
    users_query = db.query(User).filter(User.is_active == True)
    lawyers_query = db.query(Lawyer).join(User).filter(User.is_active == True)
    clients_query = db.query(Client).join(User).filter(User.is_active == True)
    cases_query = db.query(Case)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        # For lawyer, show their assigned cases and clients
        # For now, show all - in full implementation, filter by assignments
        pass
    elif current_user.role == "client":
        # For client, show only their data
        cases_query = cases_query.filter(Case.client_id == current_user.id)
        clients_query = clients_query.filter(Client.user_id == current_user.id)
    
    # Calculate statistics
    total_users = users_query.count() if current_user.role == "admin" else 0
    total_lawyers = lawyers_query.count()
    total_clients = clients_query.count()
    total_cases = cases_query.count()
    
    # Case status breakdown
    active_cases = cases_query.filter(Case.case_status.in_(["active", "in_progress"])).count()
    completed_cases = cases_query.filter(Case.case_status == "completed").count()
    pending_cases = cases_query.filter(Case.case_status == "pending").count()
    
    # Priority breakdown
    high_priority_cases = cases_query.filter(Case.priority_level == "high").count()
    urgent_cases = cases_query.filter(Case.priority_level == "urgent").count()
    
    # Recent activity (simplified)
    recent_cases = cases_query.order_by(Case.created_at.desc()).limit(5).all()
    
    return {
        "overview": {
            "total_users": total_users,
            "total_lawyers": total_lawyers,
            "total_clients": total_clients,
            "total_cases": total_cases
        },
        "case_stats": {
            "active": active_cases,
            "completed": completed_cases,
            "pending": pending_cases,
            "high_priority": high_priority_cases,
            "urgent": urgent_cases
        },
        "recent_activity": [
            {
                "id": case.case_id,
                "type": "case_created",
                "title": f"New {case.case_type} case created",
                "case_number": case.case_number,
                "created_at": case.created_at
            } for case in recent_cases
        ]
    }

@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get recent activity"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # For now, return recent cases as activity
    # In full implementation, this would be from an activity log table
    query = db.query(Case)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        # For lawyer, show their assigned cases
        pass
    elif current_user.role == "client":
        query = query.filter(Case.client_id == current_user.id)
    
    recent_cases = query.order_by(Case.created_at.desc()).limit(limit).all()
    
    activities = []
    for case in recent_cases:
        activities.append({
            "id": case.case_id,
            "type": "case_created",
            "title": f"New {case.case_type} case created",
            "subtitle": f"Case #{case.case_number}",
            "timestamp": case.created_at,
            "status": case.case_status
        })
    
    return activities

@router.get("/upcoming-deadlines")
async def get_upcoming_deadlines(
    days: int = 7,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get upcoming deadlines"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # For now, use expected_completion as deadline
    # In full implementation, this would be from a deadlines table
    from datetime import date, timedelta
    
    end_date = date.today() + timedelta(days=days)
    
    query = db.query(Case).filter(
        Case.expected_completion.isnot(None),
        Case.expected_completion <= end_date,
        Case.case_status.in_(["active", "in_progress", "pending"])
    )
    
    # Role-based filtering
    if current_user.role == "lawyer":
        # For lawyer, show their assigned cases
        pass
    elif current_user.role == "client":
        query = query.filter(Case.client_id == current_user.id)
    
    upcoming_cases = query.order_by(Case.expected_completion).all()
    
    deadlines = []
    for case in upcoming_cases:
        days_remaining = (case.expected_completion - date.today()).days
        deadlines.append({
            "id": case.case_id,
            "title": f"{case.case_type} deadline",
            "case_number": case.case_number,
            "due_date": case.expected_completion,
            "days_remaining": days_remaining,
            "priority": case.priority_level,
            "status": "upcoming" if days_remaining > 0 else "overdue"
        })
    
    return deadlines

@router.get("/case-distribution")
async def get_case_distribution(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get case distribution by type and status"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Case)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        # For lawyer, show their assigned cases
        pass
    elif current_user.role == "client":
        query = query.filter(Case.client_id == current_user.id)
    
    # Distribution by case type
    case_types = db.query(
        Case.case_type,
        func.count(Case.case_id).label('count')
    ).group_by(Case.case_type).all()
    
    # Distribution by status
    case_statuses = db.query(
        Case.case_status,
        func.count(Case.case_id).label('count')
    ).group_by(Case.case_status).all()
    
    return {
        "by_type": [{"type": ct.case_type, "count": ct.count} for ct in case_types],
        "by_status": [{"status": cs.case_status, "count": cs.count} for cs in case_statuses]
    }