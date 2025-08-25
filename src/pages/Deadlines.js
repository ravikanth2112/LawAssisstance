import React, { useState } from 'react';
import { Search, Plus, Calendar, Clock, AlertTriangle, CheckCircle } from 'lucide-react';

const DeadlineCard = ({ deadline }) => (
  <div style={{
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    border: '1px solid #e2e8f0',
    borderLeft: `4px solid ${
      deadline.priority === 'urgent' ? '#dc2626' : 
      deadline.priority === 'high' ? '#ea580c' : 
      deadline.priority === 'medium' ? '#d97706' : '#059669'
    }`
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{
          width: '48px',
          height: '48px',
          borderRadius: '50%',
          backgroundColor: deadline.priority === 'urgent' ? '#dc2626' : 
                           deadline.priority === 'high' ? '#ea580c' : 
                           deadline.priority === 'medium' ? '#d97706' : '#059669',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginRight: '12px'
        }}>
          {deadline.status === 'completed' ? 
            <CheckCircle size={20} color="white" /> : 
            <AlertTriangle size={20} color="white" />
          }
        </div>
        <div>
          <h3 style={{ margin: '0 0 4px 0', fontSize: '16px', fontWeight: '600', color: '#1e293b' }}>
            {deadline.title}
          </h3>
          <p style={{ margin: '0', fontSize: '14px', color: '#64748b' }}>
            {deadline.client} • {deadline.caseType}
          </p>
        </div>
      </div>
      <span style={{
        padding: '4px 12px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: '600',
        backgroundColor: deadline.priority === 'urgent' ? '#fef2f2' : 
                         deadline.priority === 'high' ? '#fff7ed' : 
                         deadline.priority === 'medium' ? '#fffbeb' : '#f0fdf4',
        color: deadline.priority === 'urgent' ? '#dc2626' : 
               deadline.priority === 'high' ? '#ea580c' : 
               deadline.priority === 'medium' ? '#d97706' : '#059669'
      }}>
        {deadline.priority.toUpperCase()}
      </span>
    </div>
    
    <div style={{ marginBottom: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
        <Calendar size={16} style={{ marginRight: '8px', color: '#64748b' }} />
        <span style={{ fontSize: '14px', color: '#64748b' }}>
          <strong>Due Date:</strong> {deadline.dueDate}
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <Clock size={16} style={{ marginRight: '8px', color: '#64748b' }} />
        <span style={{ fontSize: '14px', color: '#64748b' }}>
          <strong>Days Remaining:</strong> {deadline.daysRemaining}
        </span>
      </div>
    </div>
    
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{
        padding: '4px 12px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: '500',
        backgroundColor: deadline.status === 'completed' ? '#dcfce7' : 
                         deadline.status === 'in-progress' ? '#fef3c7' : '#f3f4f6',
        color: deadline.status === 'completed' ? '#166534' : 
               deadline.status === 'in-progress' ? '#92400e' : '#374151'
      }}>
        {deadline.status === 'completed' ? 'Completed' : 
         deadline.status === 'in-progress' ? 'In Progress' : 'Pending'}
      </span>
      <button onClick={() => {
        if (deadline.status === 'completed') {
          alert(`Viewing details for: ${deadline.task}`);
        } else {
          alert(`Marking complete: ${deadline.task}`);
        }
      }} style={{
        padding: '6px 12px',
        backgroundColor: deadline.status === 'completed' ? '#6b7280' : '#3b82f6',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        fontSize: '12px',
        cursor: 'pointer'
      }}>
        {deadline.status === 'completed' ? 'View Details' : 'Mark Complete'}
      </button>
    </div>
  </div>
);

const Deadlines = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  
  const deadlines = [
    {
      id: 1,
      title: 'I-130 Response Due',
      client: 'Johnson Family',
      caseType: 'Family-based Green Card',
      dueDate: 'Aug 25, 2025',
      daysRemaining: '1 day',
      priority: 'urgent',
      status: 'pending'
    },
    {
      id: 2,
      title: 'Medical Exam Reminder',
      client: 'Sarah Kim',
      caseType: 'STEM OPT Extension',
      dueDate: 'Aug 28, 2025',
      daysRemaining: '4 days',
      priority: 'high',
      status: 'in-progress'
    },
    {
      id: 3,
      title: 'Biometrics Appointment',
      client: 'Carlos Mendez',
      caseType: 'Asylum Application',
      dueDate: 'Sep 5, 2025',
      daysRemaining: '12 days',
      priority: 'medium',
      status: 'pending'
    },
    {
      id: 4,
      title: 'Court Hearing',
      client: 'Fatima Al-Rashid',
      caseType: 'Deportation Defense',
      dueDate: 'Sep 12, 2025',
      daysRemaining: '19 days',
      priority: 'urgent',
      status: 'in-progress'
    },
    {
      id: 5,
      title: 'H-1B Filing Deadline',
      client: 'Anna Kowalski',
      caseType: 'H-1B Visa Application',
      dueDate: 'Aug 30, 2025',
      daysRemaining: '6 days',
      priority: 'high',
      status: 'pending'
    },
    {
      id: 6,
      title: 'Green Card Interview',
      client: 'Li Wei',
      caseType: 'EB-1 Petition',
      dueDate: 'Aug 20, 2025',
      daysRemaining: 'Completed',
      priority: 'normal',
      status: 'completed'
    }
  ];

  const filteredDeadlines = deadlines.filter(deadline =>
    deadline.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    deadline.client.toLowerCase().includes(searchTerm.toLowerCase()) ||
    deadline.caseType.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h1 style={{ margin: '0 0 8px 0', fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
              Deadlines
            </h1>
            <p style={{ margin: '0', color: '#64748b' }}>
              Track important case deadlines and appointments ({deadlines.length} total deadlines)
            </p>
          </div>
          <button onClick={() => setShowAddModal(true)} style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '12px 20px',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500'
          }}>
            <Plus size={16} />
            Add Deadline
          </button>
        </div>
        
        {/* Search Bar */}
        <div style={{ position: 'relative', maxWidth: '400px' }}>
          <Search 
            size={16} 
            style={{ 
              position: 'absolute', 
              left: '12px', 
              top: '50%', 
              transform: 'translateY(-50%)',
              color: '#64748b'
            }} 
          />
          <input
            type="text"
            placeholder="Search deadlines by title, client, or case type..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '12px 12px 12px 40px',
              border: '1px solid #e2e8f0',
              borderRadius: '6px',
              fontSize: '14px',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* Deadlines Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))',
        gap: '20px'
      }}>
        {filteredDeadlines.map((deadline) => (
          <DeadlineCard key={deadline.id} deadline={deadline} />
        ))}
      </div>
      
      {filteredDeadlines.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '40px',
          color: '#64748b'
        }}>
          <Clock size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
          <p>No deadlines found matching your criteria.</p>
        </div>
      )}
    </div>
  );
};

export default Deadlines;
