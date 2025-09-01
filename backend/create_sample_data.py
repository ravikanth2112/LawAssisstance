"""
Database seeder script - Create sample data for development
"""

import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.lawyer import Lawyer
from app.models.client import Client, ClientStatus
from app.models.case import Case, CaseStatus, CasePriority
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for development"""
    
    # Test database connection first
    try:
        print("🧪 Testing database connection...")
        with engine.connect() as conn:
            conn.execute("SELECT 1").fetchone()
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Please run 'python setup_sqlserver.py' first to set up the database.")
        return
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"ℹ️ Found {existing_users} existing users. Skipping data creation.")
            print("💡 To recreate data, please clear the database first.")
            return
        
        # Create sample users
        print("Creating sample users...")
        
        # Admin user
        admin_user = User(
            email="admin@lawfirm.com",
            password_hash=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        db.add(admin_user)
        
        # Lawyer users
        lawyer_users = [
            User(
                email="john.smith@lawfirm.com",
                password_hash=get_password_hash("lawyer123"),
                first_name="John",
                last_name="Smith",
                role=UserRole.LAWYER,
                is_active=True,
                is_verified=True
            ),
            User(
                email="sarah.johnson@lawfirm.com",
                password_hash=get_password_hash("lawyer123"),
                first_name="Sarah",
                last_name="Johnson",
                role=UserRole.LAWYER,
                is_active=True,
                is_verified=True
            )
        ]
        
        for user in lawyer_users:
            db.add(user)
        
        # Client users
        client_users = [
            User(
                email="maria.rodriguez@email.com",
                password_hash=get_password_hash("client123"),
                first_name="Maria",
                last_name="Rodriguez",
                role=UserRole.CLIENT,
                is_active=True,
                is_verified=True
            ),
            User(
                email="john.chen@email.com",
                password_hash=get_password_hash("client123"),
                first_name="John",
                last_name="Chen",
                role=UserRole.CLIENT,
                is_active=True,
                is_verified=True
            )
        ]
        
        for user in client_users:
            db.add(user)
        
        db.commit()
        
        # Create lawyer profiles
        print("Creating lawyer profiles...")
        
        lawyers_data = [
            {
                "user_id": lawyer_users[0].id,
                "bar_number": "BAR123456",
                "practice_areas": "Immigration Law, Family Law",
                "experience_years": 15,
                "phone": "+1 (555) 123-4567",
                "office_address": "123 Law Street, Legal City, LC 12345",
                "bio": "Experienced immigration attorney with 15 years of practice."
            },
            {
                "user_id": lawyer_users[1].id,
                "bar_number": "BAR789012",
                "practice_areas": "Immigration Law, Business Law",
                "experience_years": 8,
                "phone": "+1 (555) 234-5678",
                "office_address": "456 Attorney Ave, Legal City, LC 12345",
                "bio": "Specialized in business immigration and visa applications."
            }
        ]
        
        lawyers = []
        for data in lawyers_data:
            lawyer = Lawyer(**data)
            db.add(lawyer)
            lawyers.append(lawyer)
        
        db.commit()
        
        # Create client profiles
        print("Creating client profiles...")
        
        clients_data = [
            {
                "user_id": client_users[0].id,
                "lawyer_id": lawyers[0].id,
                "first_name": "Maria",
                "last_name": "Rodriguez",
                "email": "maria.rodriguez@email.com",
                "phone": "+1 (555) 345-6789",
                "address": "789 Client St, Client City, CC 12345",
                "country_of_birth": "Mexico",
                "current_status": "H-1B Holder",
                "case_type": "I-485 Adjustment of Status",
                "status": ClientStatus.ACTIVE,
                "last_contact": datetime.now() - timedelta(days=2)
            },
            {
                "user_id": client_users[1].id,
                "lawyer_id": lawyers[0].id,
                "first_name": "John",
                "last_name": "Chen",
                "email": "john.chen@email.com",
                "phone": "+1 (555) 456-7890",
                "address": "321 Resident Rd, Client City, CC 12345",
                "country_of_birth": "China",
                "current_status": "F-1 Student",
                "case_type": "H-1B Visa Application",
                "status": ClientStatus.PENDING,
                "last_contact": datetime.now() - timedelta(days=7)
            },
            {
                "lawyer_id": lawyers[1].id,
                "first_name": "Ahmed",
                "last_name": "Hassan",
                "email": "ahmed.hassan@email.com",
                "phone": "+1 (555) 567-8901",
                "address": "654 Immigration Blvd, Client City, CC 12345",
                "country_of_birth": "Egypt",
                "current_status": "Tourist Visa",
                "case_type": "Family-Based Green Card",
                "status": ClientStatus.ACTIVE,
                "last_contact": datetime.now() - timedelta(days=3)
            },
            {
                "lawyer_id": lawyers[1].id,
                "first_name": "Lisa",
                "last_name": "Thompson",
                "email": "lisa.thompson@email.com",
                "phone": "+1 (555) 678-9012",
                "address": "987 Visa Way, Client City, CC 12345",
                "country_of_birth": "Canada",
                "current_status": "L-1 Visa",
                "case_type": "L-1 Visa Transfer",
                "status": ClientStatus.COMPLETED,
                "last_contact": datetime.now() - timedelta(days=14)
            }
        ]
        
        clients = []
        for data in clients_data:
            client = Client(**data)
            db.add(client)
            clients.append(client)
        
        db.commit()
        
        # Create sample cases
        print("Creating sample cases...")
        
        cases_data = [
            {
                "client_id": clients[0].id,
                "lawyer_id": lawyers[0].id,
                "case_number": "CASE-2024-0001",
                "case_type": "I-485 Adjustment of Status",
                "title": "Adjustment of Status Application",
                "description": "Client applying for permanent residence through employment",
                "status": CaseStatus.IN_PROGRESS,
                "priority": CasePriority.HIGH,
                "filed_date": datetime.now() - timedelta(days=45),
                "deadline": datetime.now() + timedelta(days=30),
                "estimated_cost": 5000.00,
                "progress_percentage": 65
            },
            {
                "client_id": clients[1].id,
                "lawyer_id": lawyers[0].id,
                "case_number": "CASE-2024-0002",
                "case_type": "H-1B Visa Application",
                "title": "H-1B Specialty Occupation Visa",
                "description": "Initial H-1B application for software engineer position",
                "status": CaseStatus.PENDING,
                "priority": CasePriority.MEDIUM,
                "filed_date": datetime.now() - timedelta(days=30),
                "deadline": datetime.now() + timedelta(days=60),
                "estimated_cost": 3500.00,
                "progress_percentage": 25
            },
            {
                "client_id": clients[2].id,
                "lawyer_id": lawyers[1].id,
                "case_number": "CASE-2024-0003",
                "case_type": "Family-Based Green Card",
                "title": "I-130 Petition for Alien Relative",
                "description": "Family-based immigration petition",
                "status": CaseStatus.WAITING_RESPONSE,
                "priority": CasePriority.MEDIUM,
                "filed_date": datetime.now() - timedelta(days=60),
                "deadline": datetime.now() + timedelta(days=90),
                "estimated_cost": 4000.00,
                "progress_percentage": 80
            },
            {
                "client_id": clients[3].id,
                "lawyer_id": lawyers[1].id,
                "case_number": "CASE-2024-0004",
                "case_type": "L-1 Visa Transfer",
                "title": "L-1A Intracompany Transfer",
                "description": "Executive transfer from Canadian office",
                "status": CaseStatus.COMPLETED,
                "priority": CasePriority.LOW,
                "filed_date": datetime.now() - timedelta(days=120),
                "deadline": datetime.now() - timedelta(days=30),
                "completed_date": datetime.now() - timedelta(days=15),
                "estimated_cost": 2500.00,
                "actual_cost": 2500.00,
                "progress_percentage": 100
            }
        ]
        
        for data in cases_data:
            case = Case(**data)
            db.add(case)
        
        db.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📝 Test Accounts:")
        print("Admin: admin@lawfirm.com / admin123")
        print("Lawyer 1: john.smith@lawfirm.com / lawyer123")
        print("Lawyer 2: sarah.johnson@lawfirm.com / lawyer123")
        print("Client 1: maria.rodriguez@email.com / client123")
        print("Client 2: john.chen@email.com / client123")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
