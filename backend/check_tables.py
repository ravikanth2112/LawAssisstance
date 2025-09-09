import pyodbc
import sys

def check_database_tables():
    try:
        conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=RAVIKANTH\\MSSQLSERVER01;DATABASE=ImmigrationLawDB;Trusted_Connection=yes'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print(' SQL Server Database Tables Check')
        print('=' * 40)
        print(' Connected to ImmigrationLawDB')
        
        cursor.execute(\"\"\"
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE' 
            ORDER BY TABLE_NAME
        \"\"\")
        
        tables = cursor.fetchall()
        
        if tables:
            print(f' Found {len(tables)} tables:')
            for table in tables:
                print(f'   - {table[0]}')
                
            print('\\n Table Row Counts:')
            for table in tables:
                table_name = table[0]
                try:
                    cursor.execute(f'SELECT COUNT(*) FROM [{table_name}]')
                    count = cursor.fetchone()[0]
                    print(f'   {table_name}: {count} rows')
                except Exception as e:
                    print(f'   {table_name}: Error - {str(e)[:50]}...')
            
            expected_tables = ['users', 'lawyers', 'clients', 'cases', 'deadlines', 'documents', 'billing', 'payments', 'activities']
            found_tables = [table[0].lower() for table in tables]
            
            print('\\n Expected Tables Status:')
            missing_tables = []
            for table in expected_tables:
                if table in found_tables:
                    print(f' {table} - EXISTS')
                else:
                    print(f' {table} - MISSING')
                    missing_tables.append(table)
            
            if missing_tables:
                print(f'\\n Missing {len(missing_tables)} tables: {missing_tables}')
            else:
                print('\\n All expected tables are present!')
                
        else:
            print(' No tables found in ImmigrationLawDB')
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f' Database connection failed: {e}')

if __name__ == \"__main__\":
    check_database_tables()
