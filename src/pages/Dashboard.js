import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI, casesAPI } from '../services/api';

const StatCard = ({ title, value, change, icon, onClick }) => (
  <div className="col-md-3 mb-4">
    <div className="card border-0 shadow-sm h-100" style={{ cursor: 'pointer' }} onClick={onClick}>
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <h6 className="card-title text-muted mb-2">{title}</h6>
            <h3 className="mb-1">{value}</h3>
            <small className={`text-${change > 0 ? 'success' : 'danger'}`}>
              <i className={`bi bi-arrow-${change > 0 ? 'up' : 'down'}`}></i>
              {Math.abs(change)}% from last month
            </small>
          </div>
          <div className="text-primary">
            <i className={`bi ${icon} fs-3`}></i>
          </div>
        </div>
      </div>
    </div>
  </div>
);

const ActivityItem = ({ action, client, time, onViewDetails }) => (
  <div className="d-flex align-items-center py-3 border-bottom">
    <div className="bg-primary rounded-circle me-3 d-flex align-items-center justify-content-center" style={{width: '40px', height: '40px'}}>
      <i className="bi bi-person text-white"></i>
    </div>
    <div className="flex-grow-1">
      <div className="fw-medium">{action}</div>
      <small className="text-muted">{client}</small>
    </div>
    <div className="d-flex gap-2">
      <small className="text-muted me-3">{time}</small>
      <button className="btn btn-outline-primary btn-sm" onClick={() => onViewDetails(client, action)}>
        <i className="bi bi-eye"></i>
      </button>
    </div>
  </div>
);

const DeadlineItem = ({ title, date, priority, onMarkComplete, onEdit }) => {
  const priorityColors = {
    High: 'danger',
    Medium: 'warning',
    Low: 'success'
  };

  return (
    <div className="d-flex align-items-center py-3 border-bottom">
      <div className={`bg-${priorityColors[priority]} rounded-circle me-3 d-flex align-items-center justify-content-center`} style={{width: '8px', height: '8px'}}>
      </div>
      <div className="flex-grow-1">
        <div className="fw-medium">{title}</div>
        <small className="text-muted">{date}</small>
      </div>
      <div className="d-flex gap-2">
        <span className={`badge bg-${priorityColors[priority]} me-2`}>{priority}</span>
        <button className="btn btn-outline-success btn-sm" onClick={() => onMarkComplete(title)}>
          <i className="bi bi-check"></i>
        </button>
        <button className="btn btn-outline-secondary btn-sm" onClick={() => onEdit(title)}>
          <i className="bi bi-pencil"></i>
        </button>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const [notifications, setNotifications] = useState([
    'New client inquiry received',
    'Document approval pending',
    '3 deadlines approaching'
  ]);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [stats, setStats] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [upcomingDeadlines, setUpcomingDeadlines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        // Fetch dashboard statistics
        const statsResponse = await dashboardAPI.getStatistics();
        const statsData = statsResponse.data;
        
        setStats([
          { title: 'Active Cases', value: statsData.active_cases?.toString() || '0', change: 12, icon: 'bi-briefcase' },
          { title: 'This Month Revenue', value: `$${statsData.total_revenue?.toLocaleString() || '0'}`, change: 8, icon: 'bi-currency-dollar' },
          { title: 'Pending Documents', value: statsData.pending_documents?.toString() || '0', change: -5, icon: 'bi-file-earmark' },
          { title: 'Upcoming Deadlines', value: statsData.upcoming_deadlines?.toString() || '0', change: 15, icon: 'bi-calendar' }
        ]);

        // Fetch recent activity
        const activityResponse = await dashboardAPI.getRecentActivity();
        setRecentActivity(activityResponse.data || []);

        // Fetch upcoming deadlines  
        const deadlinesResponse = await dashboardAPI.getUpcomingDeadlines();
        setUpcomingDeadlines(deadlinesResponse.data || []);

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Failed to load dashboard data');
        
        // Fallback to default data
        setStats([
          { title: 'Active Cases', value: '247', change: 12, icon: 'bi-briefcase' },
          { title: 'This Month Revenue', value: '$87,320', change: 8, icon: 'bi-currency-dollar' },
          { title: 'Pending Documents', value: '34', change: -5, icon: 'bi-file-earmark' },
          { title: 'Upcoming Deadlines', value: '12', change: 15, icon: 'bi-calendar' }
        ]);
        
        setRecentActivity([
          { action: 'New I-485 application filed', client: 'Maria Rodriguez', time: '2 hours ago' },
          { action: 'Document uploaded', client: 'John Chen', time: '4 hours ago' },
          { action: 'Case status updated', client: 'Ahmed Hassan', time: '6 hours ago' },
          { action: 'Payment received', client: 'Lisa Thompson', time: '1 day ago' }
        ]);
        
        setUpcomingDeadlines([
          { title: 'I-140 Response Due', date: 'Dec 15, 2024', priority: 'High' },
          { title: 'H-1B Extension Filing', date: 'Dec 18, 2024', priority: 'High' },
          { title: 'Client Meeting - Kumar Family', date: 'Dec 20, 2024', priority: 'Medium' },
          { title: 'Document Review', date: 'Dec 22, 2024', priority: 'Low' }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleStatClick = (statTitle) => {
    alert(`Viewing details for: ${statTitle}`);
  };

  const handleNotifications = () => {
    setShowNotifications(!showNotifications);
  };

  const handleSettings = () => {
    setShowSettings(!showSettings);
  };

  const handleViewDetails = (client, action) => {
    alert(`Viewing details for: ${action} - ${client}`);
  };

  const handleMarkComplete = (title) => {
    alert(`Marking as complete: ${title}`);
  };

  const handleEdit = (title) => {
    alert(`Editing: ${title}`);
  };

  const handleRefresh = async () => {
    setLoading(true);
    try {
      // Fetch dashboard statistics
      const statsResponse = await dashboardAPI.getStatistics();
      const statsData = statsResponse.data;
      
      setStats([
        { title: 'Active Cases', value: statsData.active_cases?.toString() || '0', change: 12, icon: 'bi-briefcase' },
        { title: 'This Month Revenue', value: `$${statsData.total_revenue?.toLocaleString() || '0'}`, change: 8, icon: 'bi-currency-dollar' },
        { title: 'Pending Documents', value: statsData.pending_documents?.toString() || '0', change: -5, icon: 'bi-file-earmark' },
        { title: 'Upcoming Deadlines', value: statsData.upcoming_deadlines?.toString() || '0', change: 15, icon: 'bi-calendar' }
      ]);

      // Fetch recent activity
      const activityResponse = await dashboardAPI.getRecentActivity();
      setRecentActivity(activityResponse.data || []);

      // Fetch upcoming deadlines  
      const deadlinesResponse = await dashboardAPI.getUpcomingDeadlines();
      setUpcomingDeadlines(deadlinesResponse.data || []);

    } catch (error) {
      console.error('Error refreshing dashboard data:', error);
      setError('Failed to refresh dashboard data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h2 mb-1">
            Welcome back, {user?.first_name || 'User'}! 
            {loading && <span className="spinner-border spinner-border-sm ms-2" role="status"></span>}
          </h1>
          <p className="text-muted mb-0">Overview of your immigration practice</p>
          {error && (
            <div className="alert alert-warning py-1 px-2 mt-2 small" role="alert">
              <i className="bi bi-exclamation-triangle me-1"></i>
              {error}
            </div>
          )}
        </div>
        <div className="d-flex gap-2 position-relative">
          <button 
            className="btn btn-outline-secondary d-flex align-items-center position-relative"
            onClick={handleNotifications}
          >
            <i className="bi bi-bell me-2"></i>
            Notifications
            {notifications.length > 0 && (
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {notifications.length}
              </span>
            )}
          </button>
          <button 
            className="btn btn-outline-secondary d-flex align-items-center"
            onClick={handleSettings}
          >
            <i className="bi bi-gear me-2"></i>
            Settings
          </button>
          
          {/* Notifications Dropdown */}
          {showNotifications && (
            <div className="position-absolute top-100 end-0 mt-2 bg-white border rounded shadow-lg" style={{width: '300px', zIndex: 1000}}>
              <div className="p-3 border-bottom">
                <h6 className="mb-0">Notifications</h6>
              </div>
              <div className="p-2">
                {notifications.map((notification, index) => (
                  <div key={index} className="p-2 border-bottom">
                    <small>{notification}</small>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Settings Dropdown */}
          {showSettings && (
            <div className="position-absolute top-100 end-0 mt-2 bg-white border rounded shadow-lg" style={{width: '250px', zIndex: 1000}}>
              <div className="p-3 border-bottom">
                <h6 className="mb-0">Settings</h6>
              </div>
              <div className="p-2">
                <button className="btn btn-link text-start w-100 p-2">Profile Settings</button>
                <button className="btn btn-link text-start w-100 p-2">Firm Settings</button>
                <button className="btn btn-link text-start w-100 p-2">Preferences</button>
                <button className="btn btn-link text-start w-100 p-2">Help & Support</button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-4">
        {stats.map((stat, index) => (
          <StatCard 
            key={index} 
            {...stat} 
            onClick={() => handleStatClick(stat.title)}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="row">
        {/* Recent Activity */}
        <div className="col-lg-8 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-0 py-3">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">Recent Activity</h5>
                <button className="btn btn-outline-primary btn-sm" onClick={handleRefresh} disabled={loading}>
                  <i className="bi bi-arrow-clockwise me-1"></i>
                  {loading ? 'Refreshing...' : 'Refresh'}
                </button>
              </div>
            </div>
            <div className="card-body">
              {recentActivity.map((activity, index) => (
                <ActivityItem 
                  key={index} 
                  {...activity} 
                  onViewDetails={handleViewDetails}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Upcoming Deadlines */}
        <div className="col-lg-4 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-0 py-3">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">Upcoming Deadlines</h5>
                <button className="btn btn-primary btn-sm">
                  <i className="bi bi-plus me-1"></i>
                  Add
                </button>
              </div>
            </div>
            <div className="card-body">
              {upcomingDeadlines.map((deadline, index) => (
                <DeadlineItem 
                  key={index} 
                  {...deadline} 
                  onMarkComplete={handleMarkComplete}
                  onEdit={handleEdit}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

