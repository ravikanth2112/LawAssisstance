import React from 'react';
import { AlertTriangle, Clock } from 'lucide-react';

const DeadlineItem = ({ name, caseType, date, priority }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return '#dc2626';
      case 'high': return '#ea580c';
      case 'medium': return '#d97706';
      default: return '#059669';
    }
  };

  const getPriorityBg = (priority) => {
    switch (priority) {
      case 'urgent': return '#fef2f2';
      case 'high': return '#fff7ed';
      case 'medium': return '#fffbeb';
      default: return '#f0fdf4';
    }
  };

  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 'urgent': return 'Urgent';
      case 'high': return 'High';
      case 'medium': return 'Medium';
      default: return 'Normal';
    }
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const today = new Date();
    const diffTime = date - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Tomorrow';
    if (diffDays < 7) return `${diffDays} days`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '12px 0',
      borderBottom: '1px solid #f1f5f9'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', flex: 1 }}>
        <AlertTriangle 
          size={16} 
          color={getPriorityColor(priority)}
          style={{ marginRight: '8px' }}
        />
        <div>
          <div style={{ 
            fontSize: '14px', 
            fontWeight: '500', 
            color: '#1e293b',
            marginBottom: '2px'
          }}>
            {name}
          </div>
          <div style={{ 
            fontSize: '12px', 
            color: '#64748b' 
          }}>
            {caseType}
          </div>
        </div>
      </div>
      <div style={{ textAlign: 'right' }}>
        <div style={{
          fontSize: '12px',
          padding: '4px 8px',
          borderRadius: '4px',
          backgroundColor: getPriorityBg(priority),
          color: getPriorityColor(priority),
          marginBottom: '4px'
        }}>
          {formatDate(date)}
        </div>
        <div style={{
          fontSize: '10px',
          color: '#64748b'
        }}>
          {getPriorityLabel(priority)}
        </div>
      </div>
    </div>
  );
};

const UpcomingDeadlines = () => {
  const deadlines = [
    {
      name: 'Elena Rodriguez',
      caseType: 'STEM Application Deadline',
      date: '2025-08-26',
      priority: 'urgent'
    },
    {
      name: 'Anna Kowalski',
      caseType: 'H1B Filing Deadline',
      date: '2025-08-28',
      priority: 'high'
    },
    {
      name: 'Sarah Johnson',
      caseType: 'OPT Report Due',
      date: '2025-09-01',
      priority: 'medium'
    },
    {
      name: 'Michael Chen',
      caseType: 'Medical Exam Schedule',
      date: '2025-09-05',
      priority: 'normal'
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
        color: '#1e293b',
        display: 'flex',
        alignItems: 'center'
      }}>
        <Clock size={18} style={{ marginRight: '8px', color: '#3b82f6' }} />
        Upcoming Deadlines
      </h3>
      <div>
        {deadlines.map((deadline, index) => (
          <DeadlineItem key={index} {...deadline} />
        ))}
      </div>
    </div>
  );
};

export default UpcomingDeadlines;
