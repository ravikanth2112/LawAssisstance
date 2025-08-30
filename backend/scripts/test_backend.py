#!/usr/bin/env python3
"""
Test script to verify database connection and API functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import httpx
from sqlalchemy.orm import sessionmaker
from app.database import engine, get_db
from app.models import User, Lawyer, Client, Case

def test_database_connection():
    """Test direct database connection."""
    print("Testing database connection...")
    
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test query
        user_count = db.query(User).count()
        case_count = db.query(Case).count()
        lawyer_count = db.query(Lawyer).count()
        client_count = db.query(Client).count()
        
        print(f"✅ Database connection successful!")
        print(f"   Users: {user_count}")
        print(f"   Cases: {case_count}")
        print(f"   Lawyers: {lawyer_count}")
        print(f"   Clients: {client_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoints."""
    print("\nTesting API endpoints...")
    
    base_url = "http://localhost:8000"
    
    try:
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            response = await client.get(f"{base_url}/api/health")
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
            
            # Test authentication
            login_data = {
                "email": "admin@lawfirm.com",
                "password": "admin123"
            }
            
            response = await client.post(f"{base_url}/api/auth/login", json=login_data)
            if response.status_code == 200:
                print("✅ Authentication endpoint working")
                token_data = response.json()
                access_token = token_data["data"]["access_token"]
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {access_token}"}
                response = await client.get(f"{base_url}/api/users/me", headers=headers)
                if response.status_code == 200:
                    print("✅ Protected endpoint working")
                    user_data = response.json()
                    print(f"   Current user: {user_data['data']['first_name']} {user_data['data']['last_name']}")
                else:
                    print(f"❌ Protected endpoint failed: {response.status_code}")
                
                # Test dashboard endpoint
                response = await client.get(f"{base_url}/api/dashboard/", headers=headers)
                if response.status_code == 200:
                    print("✅ Dashboard endpoint working")
                    dashboard_data = response.json()
                    total_cases = dashboard_data["data"]["case_statistics"]["total_cases"]
                    print(f"   Total cases in system: {total_cases}")
                else:
                    print(f"❌ Dashboard endpoint failed: {response.status_code}")
                
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("   Make sure the FastAPI server is running on http://localhost:8000")

def test_sample_data():
    """Test sample data exists."""
    print("\nTesting sample data...")
    
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check admin user
        admin = db.query(User).filter(User.email == "admin@lawfirm.com").first()
        if admin:
            print("✅ Admin user exists")
        else:
            print("❌ Admin user not found")
        
        # Check lawyer
        lawyer = db.query(User).filter(User.email == "lawyer1@lawfirm.com").first()
        if lawyer:
            print("✅ Lawyer user exists")
        else:
            print("❌ Lawyer user not found")
        
        # Check client
        client = db.query(User).filter(User.email == "client1@email.com").first()
        if client:
            print("✅ Client user exists")
        else:
            print("❌ Client user not found")
        
        # Check cases
        cases = db.query(Case).all()
        if cases:
            print(f"✅ {len(cases)} sample cases exist")
            for case in cases:
                print(f"   - {case.case_number}: {case.case_type} ({case.case_status.value})")
        else:
            print("❌ No sample cases found")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")

async def main():
    """Run all tests."""
    print("🧪 Running Immigration Law Dashboard Tests\n")
    print("=" * 50)
    
    # Test 1: Database connection
    db_success = test_database_connection()
    
    # Test 2: Sample data
    if db_success:
        test_sample_data()
    
    # Test 3: API endpoints (only if server is running)
    print("\n" + "=" * 50)
    print("API Testing (requires server to be running)")
    print("Start server with: python -m uvicorn app.main:app --reload")
    
    try:
        await test_api_endpoints()
    except Exception as e:
        print(f"❌ API tests skipped: Server not running")
    
    print("\n" + "=" * 50)
    print("🏁 Test Summary Complete")
    print("\nIf all tests pass, your backend is ready!")
    print("Next steps:")
    print("1. Start the FastAPI server: python -m uvicorn app.main:app --reload")
    print("2. Visit http://localhost:8000/docs for API documentation")
    print("3. Test the React frontend integration")

if __name__ == "__main__":
    asyncio.run(main())
