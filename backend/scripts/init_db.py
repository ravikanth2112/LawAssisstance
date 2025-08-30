"""
Database initialization and table creation script
Run this to create all tables and sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
import urllib.parse

# Direct connection string for testing
def get_engine():
    """Create SQLAlchemy engine with proper connection string."""
    # Try different connection string formats
    connection_strings = [
        "mssql+pyodbc://@RAVIKANTH\\MSSQLSERVER01/ImmigrationLawDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes",
        "mssql+pyodbc://RAVIKANTH\\MSSQLSERVER01/ImmigrationLawDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes&charset=utf8",
        "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=RAVIKANTH\\MSSQLSERVER01;DATABASE=ImmigrationLawDB;Trusted_Connection=yes")
    ]
    
    for conn_str in connection_strings:
        try:
            engine = create_engine(conn_str, echo=True)
            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print(f"✅ Successfully connected with: {conn_str[:50]}...")
                return engine
        except Exception as e:
            print(f"❌ Failed with connection string: {e}")
            continue
    
    raise Exception("Could not establish database connection with any connection string")

from app.models import User, Lawyer, Client, Case, UserType, CaseStatus, CasePriority
from app.utils.auth import get_password_hash
import uuid
from datetime import datetime

def create_sample_data():
    """Create sample data for testing."""
    from sqlalchemy.orm import sessionmaker
    
    engine = get_engine()  # Get working engine
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@lawfirm.com").first()
        if admin_user:
            print("Sample data already exists. Skipping creation.")
            return
        
        print("Creating sample data...")
        
        # Create admin user
        admin_user = User(
            email="admin@lawfirm.com",
            password_hash=get_password_hash("admin123"),
            first_name="System",
            last_name="Admin",
            phone="555-0001",
            user_type=UserType.ADMIN
        )
        db.add(admin_user)
        db.flush()
        
        # Create lawyer user
        lawyer_user = User(
            email="lawyer1@lawfirm.com",
            password_hash=get_password_hash("lawyer123"),
            first_name="John",
            last_name="Smith",
            phone="555-0123",
            user_type=UserType.LAWYER
        )
        db.add(lawyer_user)
        db.flush()
        
        # Create lawyer profile
        lawyer = Lawyer(
            user_id=lawyer_user.user_id,
            bar_number="BAR123456",
            license_state="NY",
            specialization="Immigration Law",
            hourly_rate=350.00,
            bio="Experienced immigration attorney specializing in family-based and employment-based cases."
        )
        db.add(lawyer)
        db.flush()
        
        # Create client user
        client_user = User(
            email="client1@email.com",
            password_hash=get_password_hash("client123"),
            first_name="Maria",
            last_name="Garcia",
            phone="555-0456",
            user_type=UserType.CLIENT
        )
        db.add(client_user)
        db.flush()
        
        # Create client profile
        client = Client(
            user_id=client_user.user_id,
            client_number="CL001",
            country_of_origin="Mexico",
            current_status="Pending Green Card",
            emergency_contact="Carlos Garcia",
            emergency_phone="555-0789"
        )
        db.add(client)
        db.flush()
        
        # Create another client for testing
        client_user2 = User(
            email="client2@email.com",
            password_hash=get_password_hash("client123"),
            first_name="Ahmed",
            last_name="Hassan",
            phone="555-0567",
            user_type=UserType.CLIENT
        )
        db.add(client_user2)
        db.flush()
        
        client2 = Client(
            user_id=client_user2.user_id,
            client_number="CL002",
            country_of_origin="Egypt",
            current_status="H1B Visa",
            emergency_contact="Fatima Hassan",
            emergency_phone="555-0890"
        )
        db.add(client2)
        db.flush()
        
        # Create sample cases
        case1 = Case(
            client_id=client.client_id,
            primary_lawyer_id=lawyer.lawyer_id,
            case_number=f"CS{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}",
            case_type="Family-based Green Card",
            case_status=CaseStatus.ACTIVE,
            priority_level=CasePriority.HIGH,
            estimated_cost=5000.00,
            case_summary="Green card application for spouse of US citizen. All initial documents submitted, waiting for interview appointment.",
            filing_date=datetime.now().date()
        )
        db.add(case1)
        
        case2 = Case(
            client_id=client2.client_id,
            primary_lawyer_id=lawyer.lawyer_id,
            case_number=f"CS{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}",
            case_type="H1B to Green Card",
            case_status=CaseStatus.PENDING,
            priority_level=CasePriority.MEDIUM,
            estimated_cost=7500.00,
            case_summary="Employment-based green card application. PERM labor certification in progress."
        )
        db.add(case2)
        
        # Commit all changes
        db.commit()
        
        print("Sample data created successfully!")
        print("\nLogin credentials:")
        print("Admin: admin@lawfirm.com / admin123")
        print("Lawyer: lawyer1@lawfirm.com / lawyer123")
        print("Client 1: client1@email.com / client123")
        print("Client 2: client2@email.com / client123")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def init_database():
    """Initialize the database and create all tables."""
    try:
        print("Creating database tables...")
        
        # Get working engine
        engine = get_engine()
        
        # Import Base from app.database
        from app.database import Base
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("Database tables created successfully!")
        
        # Create sample data
        create_sample_data()
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        print("Make sure SQL Server is running and the database exists.")
        print("You may need to create the database manually first:")
        print("CREATE DATABASE ImmigrationLawDB;")

if __name__ == "__main__":
    init_database()
