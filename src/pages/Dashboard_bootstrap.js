import React from 'react';

const StatCard = ({ title, value, change, icon }) => (
  <div className="col-md-3 mb-4">
    <div className="card border-0 shadow-sm h-100">
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

const ActivityItem = ({ action, client, time }) => (
  <div className="d-flex align-items-center py-3 border-bottom">
    <div className="bg-primary rounded-circle me-3 d-flex align-items-center justify-content-center" style={{width: '40px', height: '40px'}}>
      <i className="bi bi-person text-white"></i>
    </div>
    <div className="flex-grow-1">
      <div className="fw-medium">{action}</div>
      <small className="text-muted">{client}</small>
    </div>
    <small className="text-muted">{time}</small>
  </div>
);

const DeadlineItem = ({ title, date, priority }) => {
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
      <span className={`badge bg-${priorityColors[priority]}`}>{priority}</span>
    </div>
  );
};

const Dashboard = () => {
  const stats = [
    { title: 'Active Cases', value: '247', change: 12, icon: 'bi-briefcase' },
    { title: 'This Month Revenue', value: '$87,320', change: 8, icon: 'bi-currency-dollar' },
    { title: 'Pending Documents', value: '34', change: -5, icon: 'bi-file-earmark' },
    { title: 'Upcoming Deadlines', value: '12', change: 15, icon: 'bi-calendar' }
  ];

  const recentActivity = [
    { action: 'New I-485 application filed', client: 'Maria Rodriguez', time: '2 hours ago' },
    { action: 'Document uploaded', client: 'John Chen', time: '4 hours ago' },
    { action: 'Case status updated', client: 'Ahmed Hassan', time: '6 hours ago' },
    { action: 'Payment received', client: 'Lisa Thompson', time: '1 day ago' }
  ];

  const upcomingDeadlines = [
    { title: 'I-140 Response Due', date: 'Dec 15, 2024', priority: 'High' },
    { title: 'H-1B Extension Filing', date: 'Dec 18, 2024', priority: 'High' },
    { title: 'Client Meeting - Kumar Family', date: 'Dec 20, 2024', priority: 'Medium' },
    { title: 'Document Review', date: 'Dec 22, 2024', priority: 'Low' }
  ];

  return (
    <div className="p-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h2 mb-1">Firm Dashboard</h1>
          <p className="text-muted mb-0">Overview of your immigration practice</p>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-secondary d-flex align-items-center">
            <i className="bi bi-bell me-2"></i>
            Notifications
          </button>
          <button className="btn btn-outline-secondary d-flex align-items-center">
            <i className="bi bi-gear me-2"></i>
            Settings
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-4">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      {/* Main Content */}
      <div className="row">
        {/* Recent Activity */}
        <div className="col-lg-8 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-0 py-3">
              <h5 className="card-title mb-0">Recent Activity</h5>
            </div>
            <div className="card-body">
              {recentActivity.map((activity, index) => (
                <ActivityItem key={index} {...activity} />
              ))}
            </div>
          </div>
        </div>

        {/* Upcoming Deadlines */}
        <div className="col-lg-4 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-0 py-3">
              <h5 className="card-title mb-0">Upcoming Deadlines</h5>
            </div>
            <div className="card-body">
              {upcomingDeadlines.map((deadline, index) => (
                <DeadlineItem key={index} {...deadline} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
