#!/usr/bin/env python3
"""
Check existing data in database
"""
import sys
import os
sys.path.append('.')
sys.path.append('./app')

from app.core.database import SessionLocal
from app.models.user import User
from app.models.lawyer import Lawyer
from app.models.client import Client
from app.models.case import Case

def check_existing_data():
    print("🔍 Checking existing database data...")
    
    db = SessionLocal()
    try:
        # Check users
        users = db.query(User).all()
        print(f"\n👥 Users ({len(users)}):")
        for user in users:
            print(f"  - {user.email} ({user.user_type}): {user.first_name} {user.last_name}")
        
        # Check lawyers
        lawyers = db.query(Lawyer).all()
        print(f"\n👩‍💼 Lawyers ({len(lawyers)}):")
        for lawyer in lawyers:
            print(f"  - ID: {lawyer.lawyer_id}, User ID: {lawyer.user_id}, Bar: {lawyer.bar_number}")
        
        # Check clients
        clients = db.query(Client).all()
        print(f"\n👤 Clients ({len(clients)}):")
        for client in clients:
            print(f"  - ID: {client.client_id}, User ID: {client.user_id}, Number: {client.client_number}")
        
        # Check cases
        cases = db.query(Case).all()
        print(f"\n📋 Cases ({len(cases)}):")
        for case in cases:
            print(f"  - {case.case_number}: {case.case_type} ({case.case_status})")
        
        if len(users) > 0:
            print("\n🎯 Test Login Credentials:")
            print("━" * 40)
            for user in users:
                if user.user_type == "admin":
                    print(f"🔐 Admin: {user.email} / admin123")
                elif user.user_type == "lawyer":
                    print(f"👩‍💼 Lawyer: {user.email} / lawyer123") 
                elif user.user_type == "client":
                    print(f"👤 Client: {user.email} / client123")
        
    except Exception as e:
        print(f"❌ Error checking data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_existing_data()
