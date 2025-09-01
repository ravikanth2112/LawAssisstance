import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import SignIn from './pages/SignIn';
import Dashboard from './pages/Dashboard';
import Clients from './pages/Clients';
import Documents from './pages/Documents';
import Deadlines from './pages/Deadlines';
import Billing from './pages/Billing';
import Branding from './pages/Branding';
import Analytics from './pages/Analytics';

// Protected Layout Component for authenticated pages
const DashboardLayout = ({ children }) => {
  return (
    <div className="d-flex min-vh-100">
      <Sidebar />
      <div className="flex-grow-1 bg-light" style={{ marginLeft: '280px' }}>
        {children}
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<SignIn />} />
        <Route path="/signin" element={<SignIn />} />
        
        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={
          <DashboardLayout>
            <Dashboard />
          </DashboardLayout>
        } />
        <Route path="/clients" element={
          <DashboardLayout>
            <Clients />
          </DashboardLayout>
        } />
        <Route path="/documents" element={
          <DashboardLayout>
            <Documents />
          </DashboardLayout>
        } />
        <Route path="/deadlines" element={
          <DashboardLayout>
            <Deadlines />
          </DashboardLayout>
        } />
        <Route path="/billing" element={
          <DashboardLayout>
            <Billing />
          </DashboardLayout>
        } />
        <Route path="/branding" element={
          <DashboardLayout>
            <Branding />
          </DashboardLayout>
        } />
        <Route path="/analytics" element={
          <DashboardLayout>
            <Analytics />
          </DashboardLayout>
        } />
      </Routes>
    </Router>
  );
}

export default App;
