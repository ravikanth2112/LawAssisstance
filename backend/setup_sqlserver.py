"""
SQL Server Express Database Setup Script
Creates the database and tables for Immigration Law Dashboard
"""

import sys
from pathlib import Path
import pyodbc

# Add the app directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from app.core.config import settings
from app.core.database import engine, Base
from app.models import user, lawyer, client, case

def create_database():
    """Create the database if it doesn't exist"""
    
    try:
        # Extract server and database from settings
        server = settings.SQL_SERVER
        database = settings.SQL_DATABASE
        
        print(f"🔧 Setting up SQL Server Express database...")
        print(f"📍 Server: {server}")
        print(f"🗄️ Database: {database}")
        
        # Connection string for master database to create our database
        if settings.SQL_USERNAME and settings.SQL_PASSWORD:
            # SQL Server Authentication
            master_conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;UID={settings.SQL_USERNAME};PWD={settings.SQL_PASSWORD}"
        else:
            # Windows Authentication
            master_conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes"
        
        # Connect to master database
        print("🔗 Connecting to SQL Server...")
        conn = pyodbc.connect(master_conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{database}'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print(f"📁 Creating database '{database}'...")
            cursor.execute(f"CREATE DATABASE [{database}]")
            print("✅ Database created successfully!")
        else:
            print("ℹ️ Database already exists.")
        
        cursor.close()
        conn.close()
        
        # Now create tables using SQLAlchemy
        print("🏗️ Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        print("\n🎉 SQL Server Express setup complete!")
        print(f"📊 Database URL: {settings.database_url}")
        
        return True
        
    except pyodbc.Error as e:
        print(f"❌ SQL Server Error: {e}")
        print("\n💡 Common solutions:")
        print("1. Ensure SQL Server Express is installed and running")
        print("2. Check if 'SQLEXPRESS' instance is correct")
        print("3. Verify ODBC Driver 17 for SQL Server is installed")
        print("4. For Windows Auth, ensure current user has SQL Server access")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_connection():
    """Test the database connection"""
    
    try:
        print("🧪 Testing database connection...")
        
        # Test SQLAlchemy connection
        with engine.connect() as conn:
            result = conn.execute("SELECT @@VERSION").fetchone()
            print(f"✅ Connection successful!")
            print(f"📝 SQL Server Version: {result[0][:50]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🚀 Immigration Law Dashboard - SQL Server Express Setup")
    print("=" * 60)
    
    # Show current configuration
    print("📋 Current Configuration:")
    print(f"   Server: {settings.SQL_SERVER}")
    print(f"   Database: {settings.SQL_DATABASE}")
    print(f"   Auth Type: {'SQL Server' if settings.SQL_USERNAME else 'Windows'}")
    print("-" * 60)
    
    # Create database and tables
    if create_database():
        # Test connection
        test_connection()
        
        print("\n🎯 Next Steps:")
        print("1. Run: python create_sample_data.py")
        print("2. Run: python run_server.py")
        print("3. Visit: http://127.0.0.1:8000/docs")
    else:
        print("\n🔧 Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
