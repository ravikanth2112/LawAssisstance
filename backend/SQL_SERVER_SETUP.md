# 🗄️ SQL Server Express Setup Guide

## 📋 Prerequisites

### 1. Install SQL Server Express
Download and install SQL Server Express from Microsoft:
- **Download**: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
- **Choose**: "Express" (free edition)
- **Instance Name**: Use default "SQLEXPRESS" or note your custom name

### 2. Install ODBC Driver 17 for SQL Server
Download from Microsoft:
- **Download**: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- **Required**: For Python pyodbc connectivity

### 3. Verify SQL Server Services
Ensure these services are running:
- **SQL Server (SQLEXPRESS)**
- **SQL Server Browser** (if using named instances)

## ⚡ Quick Setup

### 1. Configure Environment
```bash
# Copy the environment template
cp backend/.env.example backend/.env

# Edit .env file with your SQL Server settings
# For Windows Authentication (recommended):
SQL_SERVER=localhost\SQLEXPRESS
SQL_DATABASE=ImmigrationLawDB
SQL_USERNAME=
SQL_PASSWORD=
```

### 2. Set Up Database
```bash
cd backend
python setup_sqlserver.py
```

### 3. Create Sample Data
```bash
python create_sample_data.py
```

### 4. Start API Server
```bash
python run_server.py
```

## 🔧 Configuration Options

### Windows Authentication (Recommended)
```env
SQL_SERVER=localhost\SQLEXPRESS
SQL_DATABASE=ImmigrationLawDB
SQL_USERNAME=
SQL_PASSWORD=
```

### SQL Server Authentication
```env
SQL_SERVER=localhost\SQLEXPRESS
SQL_DATABASE=ImmigrationLawDB
SQL_USERNAME=your_sql_username
SQL_PASSWORD=your_sql_password
```

### Custom Instance Name
```env
SQL_SERVER=localhost\YOUR_INSTANCE_NAME
SQL_DATABASE=ImmigrationLawDB
```

### Remote SQL Server
```env
SQL_SERVER=your-server-name
SQL_DATABASE=ImmigrationLawDB
SQL_USERNAME=your_username
SQL_PASSWORD=your_password
```

## 🧪 Testing Connection

### Test Database Setup
```bash
python setup_sqlserver.py
```

### Test API Connection
```bash
python -c "from app.core.database import engine; print('✅ Connected!' if engine.connect() else '❌ Failed')"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "SQL Server does not exist or access denied"
**Solutions:**
- Verify SQL Server Express is installed and running
- Check instance name (usually `SQLEXPRESS`)
- Ensure SQL Server Browser service is running

#### 2. "ODBC Driver not found"
**Solutions:**
- Install ODBC Driver 17 for SQL Server
- Verify driver installation: `pyodbc.drivers()`

#### 3. "Login failed for user"
**Solutions:**
- For Windows Auth: Ensure current user has SQL Server access
- For SQL Auth: Verify username/password and enable SQL Server Authentication

#### 4. "Database does not exist"
**Solutions:**
- Run `python setup_sqlserver.py` to create the database
- Verify connection to master database first

### Enable SQL Server Authentication (if needed)
1. Open SQL Server Management Studio (SSMS)
2. Connect to your SQL Server instance
3. Right-click server → Properties → Security
4. Select "SQL Server and Windows Authentication mode"
5. Restart SQL Server service

### Create SQL Server User (if needed)
```sql
-- In SSMS, run this query:
CREATE LOGIN your_username WITH PASSWORD = 'your_password';
CREATE USER your_username FOR LOGIN your_username;
ALTER ROLE db_owner ADD MEMBER your_username;
```

## 📊 Database Structure

The setup will create these tables:
- **users** - Authentication and user profiles
- **lawyers** - Lawyer-specific information
- **clients** - Client details and immigration status
- **cases** - Immigration cases and tracking

## 🔄 Migration from SQLite

If you have existing SQLite data:

1. **Export SQLite data** (custom script needed)
2. **Set up SQL Server** (run setup_sqlserver.py)
3. **Import data** to SQL Server
4. **Update configuration** to use SQL Server

## 📈 Production Considerations

For production deployment:
- Use a dedicated SQL Server instance (not Express)
- Configure proper backup strategies
- Set up connection pooling
- Use environment-specific configuration
- Enable SSL/TLS for remote connections

## 🎯 Next Steps

After successful setup:
1. ✅ Database and tables created
2. ✅ Sample data populated
3. ✅ API server running
4. 🌐 Visit http://127.0.0.1:8000/docs for API documentation
5. 🎨 Switch to DEV branch for UI development

Your Immigration Law Dashboard is now running on SQL Server Express! 🚀
