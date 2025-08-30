import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Home, 
  Users, 
  FileText, 
  Calendar, 
  DollarSign, 
  Building, 
  BarChart3, 
  Bot,
  Scale,
  LogOut
} from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleSignOut = async () => {
    try {
      await logout();
      navigate('/signin');
    } catch (error) {
      console.error('Logout error:', error);
      // Force navigation even if logout fails
      navigate('/signin');
    }
  };

  const menuItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/clients', icon: Users, label: 'Clients' },
    { path: '/documents', icon: FileText, label: 'Documents' },
    { path: '/deadlines', icon: Calendar, label: 'Deadlines' },
    { path: '/billing', icon: DollarSign, label: 'Billing & Invoices' },
    { path: '/branding', icon: Building, label: 'Firm Branding' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  ];

  return (
    <div style={{
      width: '280px',
      backgroundColor: '#1e293b',
      color: 'white',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      boxShadow: '2px 0 4px rgba(0,0,0,0.1)',
      position: 'fixed',
      left: 0,
      top: 0
    }}>
      {/* Header */}
      <div style={{
        padding: '24px 20px',
        borderBottom: '1px solid #334155'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          marginBottom: '8px'
        }}>
          <Scale size={28} style={{ color: '#3b82f6', marginRight: '12px' }} />
          <div>
            <h2 style={{
              margin: '0',
              fontSize: '18px',
              fontWeight: 'bold',
              color: 'white',
              lineHeight: '1.2'
            }}>
              Immigration Law Partners
            </h2>
            <p style={{
              margin: '4px 0 0 0',
              fontSize: '13px',
              color: '#94a3b8',
              display: 'flex',
              alignItems: 'center'
            }}>
              <Bot size={14} style={{ marginRight: '6px' }} />
              AI-Powered Assistant
            </p>
          </div>
        </div>
      </div>

      {/* User Section */}
      <div style={{
        padding: '20px',
        borderBottom: '1px solid #334155'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          marginBottom: '16px',
          padding: '12px',
          backgroundColor: '#0f172a',
          borderRadius: '8px',
          border: '1px solid #334155'
        }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: '#3b82f6',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginRight: '12px'
          }}>
            <Scale size={18} color="white" />
          </div>
          <div>
            <div style={{
              fontSize: '15px',
              fontWeight: '600',
              color: 'white',
              marginBottom: '2px'
            }}>
              {user?.first_name && user?.last_name 
                ? `${user.first_name} ${user.last_name}` 
                : user?.email || 'User'}
            </div>
            <div style={{
              fontSize: '12px',
              color: '#94a3b8'
            }}>
              {user?.role?.charAt(0).toUpperCase() + user?.role?.slice(1) || 'User'}
            </div>
          </div>
        </div>
        
        <div style={{
          display: 'flex',
          alignItems: 'center',
          padding: '12px',
          backgroundColor: '#059669',
          borderRadius: '8px',
          opacity: 0.9
        }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: 'rgba(255,255,255,0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginRight: '12px'
          }}>
            <Users size={18} color="white" />
          </div>
          <div>
            <div style={{
              fontSize: '15px',
              fontWeight: '600',
              color: 'white',
              marginBottom: '2px'
            }}>
              Client
            </div>
            <div style={{
              fontSize: '12px',
              color: 'rgba(255,255,255,0.8)'
            }}>
              247 Active Cases
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav style={{
        flex: 1,
        padding: '20px 0',
        overflowY: 'auto'
      }}>
        {menuItems.map((item, index) => {
          const IconComponent = item.icon;
          const isActive = location.pathname === item.path || (item.path === '/' && location.pathname === '/dashboard');
          
          return (
            <Link
              key={index}
              to={item.path}
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '14px 20px',
                color: isActive ? '#3b82f6' : '#94a3b8',
                backgroundColor: isActive ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
                textDecoration: 'none',
                borderLeft: isActive ? '3px solid #3b82f6' : '3px solid transparent',
                fontSize: '15px',
                fontWeight: isActive ? '600' : '500',
                transition: 'all 0.2s ease',
                marginBottom: '2px'
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.backgroundColor = '#334155';
                  e.currentTarget.style.color = 'white';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.color = '#94a3b8';
                }
              }}
            >
              <IconComponent 
                size={20} 
                style={{ 
                  marginRight: '14px',
                  color: isActive ? '#3b82f6' : 'inherit'
                }} 
              />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* AI Assistant Section */}
      <div style={{
        padding: '20px',
        borderTop: '1px solid #334155',
        backgroundColor: '#0f172a'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          padding: '14px',
          backgroundColor: '#1e293b',
          borderRadius: '8px',
          border: '1px solid #334155',
          cursor: 'pointer',
          transition: 'all 0.2s ease'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = '#334155';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = '#1e293b';
        }}
        >
          <Bot size={22} style={{ color: '#3b82f6', marginRight: '12px' }} />
          <div>
            <div style={{
              fontSize: '15px',
              fontWeight: '600',
              color: 'white',
              marginBottom: '2px'
            }}>
              AI Assistant
            </div>
            <div style={{
              fontSize: '12px',
              color: '#94a3b8'
            }}>
              Ready to help
            </div>
          </div>
        </div>

        {/* Sign Out Button */}
        <div style={{ padding: '0 16px', marginTop: 'auto', paddingBottom: '16px' }}>
          <button
            onClick={handleSignOut}
            style={{
              width: '100%',
              display: 'flex',
              alignItems: 'center',
              padding: '12px 16px',
              backgroundColor: 'transparent',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#94a3b8',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#ef4444';
              e.currentTarget.style.borderColor = '#ef4444';
              e.currentTarget.style.color = 'white';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent';
              e.currentTarget.style.borderColor = '#475569';
              e.currentTarget.style.color = '#94a3b8';
            }}
          >
            <LogOut size={18} style={{ marginRight: '12px' }} />
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
