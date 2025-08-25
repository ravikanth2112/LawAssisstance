import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/', icon: 'bi-house-door', label: 'Dashboard' },
    { path: '/clients', icon: 'bi-people', label: 'Clients' },
    { path: '/documents', icon: 'bi-file-earmark-text', label: 'Documents' },
    { path: '/deadlines', icon: 'bi-calendar-event', label: 'Deadlines' },
    { path: '/billing', icon: 'bi-currency-dollar', label: 'Billing & Invoices' },
    { path: '/branding', icon: 'bi-building', label: 'Firm Branding' },
    { path: '/analytics', icon: 'bi-bar-chart', label: 'Analytics' }
  ];

  return (
    <div className="d-flex flex-column vh-100 bg-dark text-white position-fixed" style={{width: '280px', zIndex: 1000}}>
      {/* Header */}
      <div className="p-4 border-bottom border-secondary">
        <div className="d-flex align-items-center mb-3">
          <i className="bi bi-scales text-primary fs-3 me-3"></i>
          <div>
            <h5 className="mb-0 text-white">Immigration Law Partners</h5>
            <small className="text-muted">AI-Powered Assistant</small>
          </div>
        </div>
      </div>

      {/* User Info Card */}
      <div className="p-4">
        <div className="card bg-secondary border-0">
          <div className="card-body p-3">
            <div className="d-flex align-items-center">
              <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" style={{width: '40px', height: '40px'}}>
                <i className="bi bi-person-circle text-white fs-5"></i>
              </div>
              <div className="flex-grow-1">
                <div className="fw-semibold text-white">Sarah Johnson</div>
                <small className="text-muted">Senior Partner</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-grow-1 px-3">
        <ul className="nav nav-pills flex-column">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path} className="nav-item mb-1">
                <Link
                  to={item.path}
                  className={`nav-link d-flex align-items-center py-3 px-3 rounded ${
                    isActive 
                      ? 'bg-primary text-white' 
                      : 'text-light'
                  }`}
                  style={{
                    transition: 'all 0.2s ease',
                    textDecoration: 'none'
                  }}
                >
                  <i className={`${item.icon} fs-5 me-3`}></i>
                  <span className="fw-medium">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-top border-secondary">
        <button className="btn btn-outline-light w-100 d-flex align-items-center justify-content-center">
          <i className="bi bi-box-arrow-right me-2"></i>
          Sign Out
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
