import pyodbc
import urllib.parse

# Test different connection approaches
servers = [
    "RAVIKANTH\\MSSQLSERVER01",
    "RAVIKANTH\\RAVIKANTH", 
    "RAVIKANTH",
    "(local)"
]

for server in servers:
    try:
        print(f"Testing connection to: {server}")
        
        # Test direct pyodbc connection first
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"✅ Direct connection successful to {server}")
        print(f"   Version: {version[:50]}...")
        
        # Test if our database exists
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'ImmigrationLawDB'")
        db_exists = cursor.fetchone()
        if db_exists:
            print(f"✅ ImmigrationLawDB database exists on {server}")
        else:
            print(f"ℹ️  ImmigrationLawDB database does not exist on {server}")
            # Try to create it
            cursor.execute("CREATE DATABASE ImmigrationLawDB")
            print(f"✅ Created ImmigrationLawDB database on {server}")
        
        conn.close()
        
        # If successful, create SQLAlchemy URL
        sqlalchemy_url = f"mssql+pyodbc://@{server}/ImmigrationLawDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
        print(f"✅ SQLAlchemy URL: {sqlalchemy_url}")
        break
        
    except Exception as e:
        print(f"❌ Failed to connect to {server}: {e}")
        continue
else:
    print("❌ Could not connect to any SQL Server instance")
