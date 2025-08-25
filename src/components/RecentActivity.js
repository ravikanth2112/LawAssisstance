import React from 'react';

const ActivityItem = ({ type, title, subtitle, time, status }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'approved': return '#10b981';
      case 'payment': return '#f59e0b';
      case 'new': return '#3b82f6';
      default: return '#6b7280';
    }
  };

  const getStatusIcon = (type) => {
    switch (type) {
      case 'approved': return '✅';
      case 'payment': return '💰';
      case 'new': return '👤';
      default: return '📄';
    }
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      padding: '12px 0',
      borderBottom: '1px solid #f1f5f9'
    }}>
      <div style={{ 
        fontSize: '20px',
        marginRight: '12px',
        color: getStatusColor(type)
      }}>
        {getStatusIcon(type)}
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ 
          fontSize: '14px', 
          fontWeight: '500', 
          color: '#1e293b',
          marginBottom: '2px'
        }}>
          {title}
        </div>
        {subtitle && (
          <div style={{ 
            fontSize: '12px', 
            color: '#64748b' 
          }}>
            {subtitle}
          </div>
        )}
      </div>
      <div style={{ 
        fontSize: '12px', 
        color: '#64748b' 
      }}>
        {time}
      </div>
    </div>
  );
};

const RecentActivity = () => {
  const activities = [
    {
      type: 'approved',
      title: "Sarah Johnson's OPT application approved",
      subtitle: 'Application processing completed',
      time: '2 hours ago'
    },
    {
      type: 'payment',
      title: 'Payment received: Michael Chen ($4,500)',
      subtitle: 'H-1B visa application fee',
      time: '4 hours ago'
    },
    {
      type: 'new',
      title: 'New client onboarded: Elena Rodriguez',
      subtitle: 'Family-based green card case',
      time: '1 day ago'
    },
    {
      type: 'approved',
      title: 'Document review completed',
      subtitle: 'Ahmed Hassan - I-485 forms',
      time: '2 days ago'
    }
  ];

  return (
    <div style={{
      backgroundColor: 'white',
      padding: '24px',
      borderRadius: '8px',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
      border: '1px solid #e2e8f0'
    }}>
      <h3 style={{ 
        margin: '0 0 16px 0', 
        fontSize: '18px', 
        fontWeight: '600', 
        color: '#1e293b' 
      }}>
        Recent Activity
      </h3>
      <div>
        {activities.map((activity, index) => (
          <ActivityItem key={index} {...activity} />
        ))}
      </div>
    </div>
  );
};

export default RecentActivity;
