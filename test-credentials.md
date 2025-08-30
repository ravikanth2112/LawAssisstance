# Test Credentials for Immigration Law Dashboard

## Testing Authentication Integration

Your React frontend is now connected to the FastAPI backend! Here are the test credentials from the sample data:

### Lawyer/Admin Login
**Email:** admin@firm.com  
**Password:** admin123  
**Role:** Admin  

**Email:** lawyer@firm.com  
**Password:** lawyer123  
**Role:** Lawyer  

### Client Login
**Email:** client1@email.com  
**Password:** client123  
**Role:** Client  

**Email:** client2@email.com  
**Password:** client123  
**Role:** Client  

## How to Test

1. **Frontend:** http://localhost:3000
2. **Backend API:** http://127.0.0.1:8000
3. **API Documentation:** http://127.0.0.1:8000/docs

### Testing Steps:
1. Open http://localhost:3000 in your browser
2. Choose either "Law Firm Dashboard" or "Client Portal"
3. Use one of the test credentials above
4. Click "Sign In"
5. You should be redirected to the dashboard with real data from the API

### Features Working:
- ✅ User registration and login
- ✅ JWT token authentication
- ✅ Dashboard with real API data
- ✅ User profile information in sidebar
- ✅ Logout functionality
- ✅ Error handling and loading states

### Next Steps:
- Update other components (Clients, Cases, etc.) to use API data
- Implement client dashboard for client portal users
- Add more advanced features like file uploads, notifications, etc.

## Troubleshooting

If you encounter any issues:

1. **CORS Errors:** Make sure the FastAPI server is running on http://127.0.0.1:8000
2. **Authentication Errors:** Check the browser console for detailed error messages
3. **Database Errors:** Ensure SQL Server is running and the database connection is working

## API Endpoints Available

The backend provides 85+ API endpoints covering:
- Authentication (login, register, logout)
- Users management
- Lawyers management
- Clients management
- Cases management
- Dashboard statistics and analytics

Check http://127.0.0.1:8000/docs for the complete API documentation.
