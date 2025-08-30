from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Dict, Any
from app.database import get_db
from app.models import User, Case, Client, Lawyer, UserType, CaseStatus, CasePriority
from app.routers.auth import get_current_user
from datetime import datetime, timedelta
import calendar

router = APIRouter()

@router.get("/", response_model=dict)
async def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard data for the current user."""
    dashboard_data = {}
    
    if current_user.user_type == UserType.ADMIN:
        dashboard_data = await get_admin_dashboard(db)
    elif current_user.user_type == UserType.LAWYER:
        dashboard_data = await get_lawyer_dashboard(current_user, db)
    elif current_user.user_type == UserType.CLIENT:
        dashboard_data = await get_client_dashboard(current_user, db)
    
    return {
        "success": True,
        "data": dashboard_data,
        "message": "Dashboard data retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

async def get_admin_dashboard(db: Session) -> Dict[str, Any]:
    """Get admin dashboard with system-wide statistics."""
    # User statistics
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_lawyers = db.query(Lawyer).count()
    total_clients = db.query(Client).count()
    
    # Case statistics
    total_cases = db.query(Case).count()
    active_cases = db.query(Case).filter(Case.case_status == CaseStatus.ACTIVE).count()
    pending_cases = db.query(Case).filter(Case.case_status == CaseStatus.PENDING).count()
    completed_cases = db.query(Case).filter(Case.case_status == CaseStatus.COMPLETED).count()
    
    # Priority cases
    urgent_cases = db.query(Case).filter(Case.priority_level == CasePriority.URGENT).count()
    high_priority_cases = db.query(Case).filter(Case.priority_level == CasePriority.HIGH).count()
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_cases_last_30_days = db.query(Case).filter(Case.created_at >= thirty_days_ago).count()
    new_users_last_30_days = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    
    # Cases by status breakdown
    cases_by_status = {}
    for status in CaseStatus:
        count = db.query(Case).filter(Case.case_status == status).count()
        cases_by_status[status.value] = count
    
    # Cases by priority breakdown
    cases_by_priority = {}
    for priority in CasePriority:
        count = db.query(Case).filter(Case.priority_level == priority).count()
        cases_by_priority[priority.value] = count
    
    # Monthly case trends (last 6 months)
    monthly_trends = []
    for i in range(6):
        start_date = datetime.utcnow().replace(day=1) - timedelta(days=i*30)
        end_date = start_date + timedelta(days=31)
        
        cases_count = db.query(Case).filter(
            and_(Case.created_at >= start_date, Case.created_at < end_date)
        ).count()
        
        monthly_trends.append({
            "month": calendar.month_name[start_date.month],
            "year": start_date.year,
            "cases": cases_count
        })
    
    return {
        "user_statistics": {
            "total_users": total_users,
            "active_users": active_users,
            "total_lawyers": total_lawyers,
            "total_clients": total_clients,
            "new_users_last_30_days": new_users_last_30_days
        },
        "case_statistics": {
            "total_cases": total_cases,
            "active_cases": active_cases,
            "pending_cases": pending_cases,
            "completed_cases": completed_cases,
            "urgent_cases": urgent_cases,
            "high_priority_cases": high_priority_cases,
            "new_cases_last_30_days": new_cases_last_30_days,
            "cases_by_status": cases_by_status,
            "cases_by_priority": cases_by_priority
        },
        "trends": {
            "monthly_case_trends": monthly_trends
        },
        "quick_stats": {
            "completion_rate": round((completed_cases / total_cases * 100) if total_cases > 0 else 0, 2),
            "urgent_case_percentage": round((urgent_cases / total_cases * 100) if total_cases > 0 else 0, 2),
            "active_user_percentage": round((active_users / total_users * 100) if total_users > 0 else 0, 2)
        }
    }

async def get_lawyer_dashboard(current_user: User, db: Session) -> Dict[str, Any]:
    """Get lawyer dashboard with their case statistics."""
    # Get lawyer profile
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.user_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer profile not found"
        )
    
    # Case statistics for this lawyer
    lawyer_cases = db.query(Case).filter(Case.primary_lawyer_id == lawyer.lawyer_id)
    total_cases = lawyer_cases.count()
    active_cases = lawyer_cases.filter(Case.case_status == CaseStatus.ACTIVE).count()
    pending_cases = lawyer_cases.filter(Case.case_status == CaseStatus.PENDING).count()
    completed_cases = lawyer_cases.filter(Case.case_status == CaseStatus.COMPLETED).count()
    
    # Priority cases
    urgent_cases = lawyer_cases.filter(Case.priority_level == CasePriority.URGENT).count()
    high_priority_cases = lawyer_cases.filter(Case.priority_level == CasePriority.HIGH).count()
    
    # Upcoming deadlines (next 30 days)
    thirty_days_ahead = datetime.utcnow() + timedelta(days=30)
    upcoming_deadlines = lawyer_cases.filter(
        and_(
            Case.expected_completion.isnot(None),
            Case.expected_completion <= thirty_days_ahead,
            Case.case_status.in_([CaseStatus.ACTIVE, CaseStatus.PENDING])
        )
    ).count()
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_cases_last_30_days = lawyer_cases.filter(Case.created_at >= thirty_days_ago).count()
    
    # Cases by status breakdown
    cases_by_status = {}
    for status in CaseStatus:
        count = lawyer_cases.filter(Case.case_status == status).count()
        cases_by_status[status.value] = count
    
    # Cases by priority breakdown
    cases_by_priority = {}
    for priority in CasePriority:
        count = lawyer_cases.filter(Case.priority_level == priority).count()
        cases_by_priority[priority.value] = count
    
    # Recent cases (last 5)
    recent_cases = lawyer_cases.order_by(Case.created_at.desc()).limit(5).all()
    recent_cases_data = []
    for case in recent_cases:
        client_name = f"{case.client.user.first_name} {case.client.user.last_name}" if case.client and case.client.user else "Unknown"
        recent_cases_data.append({
            "case_id": case.case_id,
            "case_number": case.case_number,
            "case_type": case.case_type,
            "client_name": client_name,
            "status": case.case_status.value,
            "priority": case.priority_level.value,
            "created_at": case.created_at.isoformat()
        })
    
    return {
        "profile": {
            "lawyer_id": lawyer.lawyer_id,
            "bar_number": lawyer.bar_number,
            "specialization": lawyer.specialization,
            "years_of_experience": lawyer.years_of_experience,
            "hourly_rate": float(lawyer.hourly_rate) if lawyer.hourly_rate else None
        },
        "case_statistics": {
            "total_cases": total_cases,
            "active_cases": active_cases,
            "pending_cases": pending_cases,
            "completed_cases": completed_cases,
            "urgent_cases": urgent_cases,
            "high_priority_cases": high_priority_cases,
            "upcoming_deadlines": upcoming_deadlines,
            "new_cases_last_30_days": new_cases_last_30_days,
            "cases_by_status": cases_by_status,
            "cases_by_priority": cases_by_priority
        },
        "recent_activity": {
            "recent_cases": recent_cases_data
        },
        "quick_stats": {
            "completion_rate": round((completed_cases / total_cases * 100) if total_cases > 0 else 0, 2),
            "urgent_case_percentage": round((urgent_cases / total_cases * 100) if total_cases > 0 else 0, 2),
            "active_case_percentage": round((active_cases / total_cases * 100) if total_cases > 0 else 0, 2)
        }
    }

async def get_client_dashboard(current_user: User, db: Session) -> Dict[str, Any]:
    """Get client dashboard with their case information."""
    # Get client profile
    client = db.query(Client).filter(Client.user_id == current_user.user_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client profile not found"
        )
    
    # Case statistics for this client
    client_cases = db.query(Case).filter(Case.client_id == client.client_id)
    total_cases = client_cases.count()
    active_cases = client_cases.filter(Case.case_status == CaseStatus.ACTIVE).count()
    pending_cases = client_cases.filter(Case.case_status == CaseStatus.PENDING).count()
    completed_cases = client_cases.filter(Case.case_status == CaseStatus.COMPLETED).count()
    
    # Priority cases
    urgent_cases = client_cases.filter(Case.priority_level == CasePriority.URGENT).count()
    high_priority_cases = client_cases.filter(Case.priority_level == CasePriority.HIGH).count()
    
    # Upcoming deadlines (next 30 days)
    thirty_days_ahead = datetime.utcnow() + timedelta(days=30)
    upcoming_deadlines = client_cases.filter(
        and_(
            Case.expected_completion.isnot(None),
            Case.expected_completion <= thirty_days_ahead,
            Case.case_status.in_([CaseStatus.ACTIVE, CaseStatus.PENDING])
        )
    ).count()
    
    # Cases by status breakdown
    cases_by_status = {}
    for status in CaseStatus:
        count = client_cases.filter(Case.case_status == status).count()
        cases_by_status[status.value] = count
    
    # All client cases with details
    all_cases = client_cases.order_by(Case.created_at.desc()).all()
    cases_data = []
    for case in all_cases:
        lawyer_name = f"{case.primary_lawyer.user.first_name} {case.primary_lawyer.user.last_name}" if case.primary_lawyer and case.primary_lawyer.user else "Unknown"
        cases_data.append({
            "case_id": case.case_id,
            "case_number": case.case_number,
            "case_type": case.case_type,
            "status": case.case_status.value,
            "priority": case.priority_level.value,
            "lawyer_name": lawyer_name,
            "filing_date": case.filing_date.isoformat() if case.filing_date else None,
            "expected_completion": case.expected_completion.isoformat() if case.expected_completion else None,
            "created_at": case.created_at.isoformat()
        })
    
    return {
        "profile": {
            "client_id": client.client_id,
            "client_number": client.client_number,
            "country_of_origin": client.country_of_origin,
            "current_status": client.current_status
        },
        "case_statistics": {
            "total_cases": total_cases,
            "active_cases": active_cases,
            "pending_cases": pending_cases,
            "completed_cases": completed_cases,
            "urgent_cases": urgent_cases,
            "high_priority_cases": high_priority_cases,
            "upcoming_deadlines": upcoming_deadlines,
            "cases_by_status": cases_by_status
        },
        "cases": {
            "all_cases": cases_data
        },
        "quick_stats": {
            "completion_rate": round((completed_cases / total_cases * 100) if total_cases > 0 else 0, 2),
            "urgent_case_percentage": round((urgent_cases / total_cases * 100) if total_cases > 0 else 0, 2),
            "active_case_percentage": round((active_cases / total_cases * 100) if total_cases > 0 else 0, 2)
        }
    }

@router.get("/summary", response_model=dict)
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a quick summary for the dashboard header."""
    if current_user.user_type == UserType.ADMIN:
        total_cases = db.query(Case).count()
        total_users = db.query(User).filter(User.is_active == True).count()
        urgent_cases = db.query(Case).filter(Case.priority_level == CasePriority.URGENT).count()
        
        return {
            "success": True,
            "data": {
                "total_cases": total_cases,
                "total_users": total_users,
                "urgent_cases": urgent_cases,
                "role": "admin"
            },
            "message": "Admin summary retrieved successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    elif current_user.user_type == UserType.LAWYER:
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.user_id).first()
        if lawyer:
            my_cases = db.query(Case).filter(Case.primary_lawyer_id == lawyer.lawyer_id).count()
            active_cases = db.query(Case).filter(
                and_(Case.primary_lawyer_id == lawyer.lawyer_id, Case.case_status == CaseStatus.ACTIVE)
            ).count()
            urgent_cases = db.query(Case).filter(
                and_(Case.primary_lawyer_id == lawyer.lawyer_id, Case.priority_level == CasePriority.URGENT)
            ).count()
        else:
            my_cases = active_cases = urgent_cases = 0
        
        return {
            "success": True,
            "data": {
                "my_cases": my_cases,
                "active_cases": active_cases,
                "urgent_cases": urgent_cases,
                "role": "lawyer"
            },
            "message": "Lawyer summary retrieved successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    elif current_user.user_type == UserType.CLIENT:
        client = db.query(Client).filter(Client.user_id == current_user.user_id).first()
        if client:
            my_cases = db.query(Case).filter(Case.client_id == client.client_id).count()
            active_cases = db.query(Case).filter(
                and_(Case.client_id == client.client_id, Case.case_status == CaseStatus.ACTIVE)
            ).count()
            pending_cases = db.query(Case).filter(
                and_(Case.client_id == client.client_id, Case.case_status == CaseStatus.PENDING)
            ).count()
        else:
            my_cases = active_cases = pending_cases = 0
        
        return {
            "success": True,
            "data": {
                "my_cases": my_cases,
                "active_cases": active_cases,
                "pending_cases": pending_cases,
                "role": "client"
            },
            "message": "Client summary retrieved successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
