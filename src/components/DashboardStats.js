import React from 'react';
import { Users, Clock, DollarSign, FileText } from 'lucide-react';

const StatCard = ({ title, value, subtitle, icon: Icon, trend }) => (
  <div style={{
    backgroundColor: 'white',
    padding: '24px',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    border: '1px solid #e2e8f0'
  }}>
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'space-between',
      marginBottom: '12px'
    }}>
      <h3 style={{ 
        margin: '0', 
        fontSize: '16px', 
        fontWeight: '600', 
        color: '#64748b' 
      }}>
        {title}
      </h3>
      <Icon size={20} style={{ color: '#3b82f6' }} />
    </div>
    <div style={{ 
      fontSize: '32px', 
      fontWeight: 'bold', 
      color: '#1e293b',
      marginBottom: '8px'
    }}>
      {value}
    </div>
    <div style={{ 
      fontSize: '14px', 
      color: '#64748b' 
    }}>
      {subtitle}
      {trend && (
        <span style={{ 
          color: '#059669', 
          fontWeight: '600',
          marginLeft: '8px'
        }}>
          {trend}
        </span>
      )}
    </div>
  </div>
);

const DashboardStats = () => {
  const stats = [
    {
      title: 'Total Clients',
      value: '247',
      subtitle: '156 Active / 91 Pending',
      icon: Users
    },
    {
      title: 'Deadlines This Week',
      value: '23',
      subtitle: '5 urgent, 18 normal',
      icon: Clock
    },
    {
      title: 'Monthly Revenue',
      value: '$48,200',
      subtitle: 'from last month',
      icon: DollarSign,
      trend: '+12%'
    },
    {
      title: 'Pending Payments',
      value: '$12,700',
      subtitle: '3 overdue invoices',
      icon: FileText
    }
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
      gap: '20px',
      marginBottom: '24px'
    }}>
      {stats.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  );
};

export default DashboardStats;
