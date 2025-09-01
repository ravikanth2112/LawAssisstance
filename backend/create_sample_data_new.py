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
from app.models.user import User
from app.models.lawyer import Lawyer
from app.models.client import Client
from app.models.case import Case
from datetime import datetime, timedelta, date
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
        print("👥 Creating sample users...")
        
        # Admin user
        admin_user = User(
            email="admin@lawfirm.com",
            password_hash=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            phone="+1 (555) 000-0001",
            user_type="admin",
            is_active=True
        )
        db.add(admin_user)
        
        # Lawyer users
        lawyer_user1 = User(
            email="john.smith@lawfirm.com",
            password_hash=get_password_hash("lawyer123"),
            first_name="John",
            last_name="Smith",
            phone="+1 (555) 123-4567",
            user_type="lawyer",
            is_active=True
        )
        db.add(lawyer_user1)
        
        lawyer_user2 = User(
            email="sarah.johnson@lawfirm.com",
            password_hash=get_password_hash("lawyer123"),
            first_name="Sarah",
            last_name="Johnson",
            phone="+1 (555) 234-5678",
            user_type="lawyer",
            is_active=True
        )
        db.add(lawyer_user2)
        
        # Client users
        client_user1 = User(
            email="maria.rodriguez@email.com",
            password_hash=get_password_hash("client123"),
            first_name="Maria",
            last_name="Rodriguez",
            phone="+1 (555) 345-6789",
            user_type="client",
            is_active=True
        )
        db.add(client_user1)
        
        client_user2 = User(
            email="john.chen@email.com",
            password_hash=get_password_hash("client123"),
            first_name="John",
            last_name="Chen",
            phone="+1 (555) 456-7890",
            user_type="client",
            is_active=True
        )
        db.add(client_user2)
        
        db.commit()
        
        # Create lawyer profiles
        print("👩‍💼 Creating lawyer profiles...")
        
        lawyer1 = Lawyer(
            user_id=lawyer_user1.user_id,
            bar_number="BAR123456",
            license_state="California",
            specialization="Immigration Law, Family Law",
            hourly_rate=350.00,
            bio="Experienced immigration attorney with 15 years of practice.",
            admitted_date=datetime(2008, 6, 15),
            is_partner=True
        )
        db.add(lawyer1)
        
        lawyer2 = Lawyer(
            user_id=lawyer_user2.user_id,
            bar_number="BAR789012",
            license_state="New York",
            specialization="Immigration Law, Business Law",
            hourly_rate=275.00,
            bio="Specialized in business immigration and visa applications.",
            admitted_date=datetime(2015, 8, 20),
            is_partner=False
        )
        db.add(lawyer2)
        
        db.commit()
        
        # Create client profiles
        print("👤 Creating client profiles...")
        
        client1 = Client(
            user_id=client_user1.user_id,
            client_number="CLT-2024-001",
            country_of_origin="Mexico",
            current_status="H-1B Holder",
            preferred_language="Spanish",
            date_of_birth=date(1990, 5, 15),
            emergency_contact="Carlos Rodriguez (Brother)",
            emergency_phone="+1 (555) 999-0001",
            notes="Fluent in English and Spanish. Prefers evening appointments."
        )
        db.add(client1)
        
        client2 = Client(
            user_id=client_user2.user_id,
            client_number="CLT-2024-002",
            country_of_origin="China",
            current_status="F-1 Student",
            preferred_language="English",
            date_of_birth=date(1988, 11, 22),
            emergency_contact="Li Chen (Sister)",
            emergency_phone="+1 (555) 999-0002",
            notes="PhD student at UC Berkeley. Available weekdays after 3 PM."
        )
        db.add(client2)
        
        # Additional client without user account
        client3 = Client(
            client_number="CLT-2024-003",
            country_of_origin="Egypt",
            current_status="Tourist Visa",
            preferred_language="Arabic",
            date_of_birth=date(1985, 3, 10),
            emergency_contact="Fatima Hassan (Wife)",
            emergency_phone="+1 (555) 999-0003",
            notes="Requires Arabic translation services."
        )
        db.add(client3)
        
        db.commit()
        
        # Create sample cases
        print("📋 Creating sample cases...")
        
        case1 = Case(
            client_id=client1.client_id,
            primary_lawyer_id=lawyer1.lawyer_id,
            case_number="CASE-2024-0001",
            case_type="I-485 Adjustment of Status",
            case_status="progress",
            priority_level="high",
            filing_date=date.today() - timedelta(days=45),
            expected_completion=date.today() + timedelta(days=30),
            estimated_cost=5000.00,
            case_summary="Client applying for permanent residence through employment-based petition."
        )
        db.add(case1)
        
        case2 = Case(
            client_id=client2.client_id,
            primary_lawyer_id=lawyer1.lawyer_id,
            case_number="CASE-2024-0002",
            case_type="H-1B Visa Application",
            case_status="pending",
            priority_level="medium",
            filing_date=date.today() - timedelta(days=30),
            expected_completion=date.today() + timedelta(days=60),
            estimated_cost=3500.00,
            case_summary="Initial H-1B application for software engineer position at tech startup."
        )
        db.add(case2)
        
        case3 = Case(
            client_id=client3.client_id,
            primary_lawyer_id=lawyer2.lawyer_id,
            case_number="CASE-2024-0003",
            case_type="Family-Based Green Card",
            case_status="review",
            priority_level="medium",
            filing_date=date.today() - timedelta(days=60),
            expected_completion=date.today() + timedelta(days=90),
            estimated_cost=4000.00,
            case_summary="I-130 petition for alien relative - spouse-based immigration case."
        )
        db.add(case3)
        
        case4 = Case(
            client_id=client1.client_id,
            primary_lawyer_id=lawyer2.lawyer_id,
            case_number="CASE-2024-0004",
            case_type="Citizenship Application",
            case_status="filed",
            priority_level="low",
            filing_date=date.today() - timedelta(days=15),
            expected_completion=date.today() + timedelta(days=180),
            estimated_cost=1500.00,
            case_summary="N-400 Application for Naturalization - US Citizenship."
        )
        db.add(case4)
        
        db.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📝 Test Accounts:")
        print("━" * 50)
        print("🔐 Admin Portal:")
        print("   Email: admin@lawfirm.com")
        print("   Password: admin123")
        print("\n👩‍💼 Lawyer Portal:")
        print("   Email: john.smith@lawfirm.com")
        print("   Password: lawyer123")
        print("   Email: sarah.johnson@lawfirm.com")
        print("   Password: lawyer123")
        print("\n👤 Client Portal:")
        print("   Email: maria.rodriguez@email.com")
        print("   Password: client123")
        print("   Email: john.chen@email.com")
        print("   Password: client123")
        print("\n📊 Database Summary:")
        print(f"   👥 Users: {db.query(User).count()}")
        print(f"   👩‍💼 Lawyers: {db.query(Lawyer).count()}")
        print(f"   👤 Clients: {db.query(Client).count()}")
        print(f"   📋 Cases: {db.query(Case).count()}")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
