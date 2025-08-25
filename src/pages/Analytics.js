import React, { useState } from 'react';
import { BarChart3, TrendingUp, Users, DollarSign, Calendar, Award } from 'lucide-react';

const MetricCard = ({ title, value, change, icon: Icon, color }) => (
  <div style={{
    backgroundColor: 'white',
    padding: '24px',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    border: '1px solid #e2e8f0'
  }}>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
      <div>
        <p style={{ fontSize: '14px', color: '#64748b', margin: '0 0 4px 0' }}>{title}</p>
        <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b', margin: '0' }}>{value}</p>
      </div>
      <div style={{
        backgroundColor: color,
        padding: '12px',
        borderRadius: '8px'
      }}>
        <Icon size={24} color="white" />
      </div>
    </div>
    <div style={{ 
      fontSize: '14px', 
      color: change.startsWith('+') ? '#059669' : '#dc2626',
      display: 'flex',
      alignItems: 'center'
    }}>
      <TrendingUp size={14} style={{ marginRight: '4px' }} />
      {change} from last month
    </div>
  </div>
);

const Analytics = () => {
  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ margin: '0 0 8px 0', fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
          Analytics Dashboard
        </h1>
        <p style={{ margin: '0', color: '#64748b' }}>
          View practice analytics and performance metrics
        </p>
      </div>

      {/* Key Metrics */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '20px',
        marginBottom: '32px'
      }}>
        <MetricCard
          title="Total Clients"
          value="247"
          change="+12.3%"
          icon={Users}
          color="#3b82f6"
        />
        <MetricCard
          title="Monthly Revenue"
          value="$48,200"
          change="+8.7%"
          icon={DollarSign}
          color="#059669"
        />
        <MetricCard
          title="Cases Completed"
          value="89"
          change="+15.2%"
          icon={Award}
          color="#7c3aed"
        />
        <MetricCard
          title="Success Rate"
          value="94.2%"
          change="+2.1%"
          icon={TrendingUp}
          color="#059669"
        />
      </div>

      {/* Charts Placeholder */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '2fr 1fr',
        gap: '24px',
        marginBottom: '32px'
      }}>
        <div style={{
          backgroundColor: 'white',
          padding: '24px',
          borderRadius: '8px',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
          border: '1px solid #e2e8f0'
        }}>
          <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
            Monthly Revenue Trend
          </h3>
          <div style={{
            height: '200px',
            backgroundColor: '#f8fafc',
            borderRadius: '4px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#64748b'
          }}>
            <div style={{ textAlign: 'center' }}>
              <BarChart3 size={48} style={{ marginBottom: '8px', opacity: 0.5 }} />
              <p>Revenue Chart Visualization</p>
            </div>
          </div>
        </div>

        <div style={{
          backgroundColor: 'white',
          padding: '24px',
          borderRadius: '8px',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
          border: '1px solid #e2e8f0'
        }}>
          <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
            Case Types Distribution
          </h3>
          <div style={{
            height: '200px',
            backgroundColor: '#f8fafc',
            borderRadius: '4px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#64748b'
          }}>
            <div style={{ textAlign: 'center' }}>
              <BarChart3 size={48} style={{ marginBottom: '8px', opacity: 0.5 }} />
              <p>Pie Chart Visualization</p>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Summary */}
      <div style={{
        backgroundColor: 'white',
        padding: '24px',
        borderRadius: '8px',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        border: '1px solid #e2e8f0'
      }}>
        <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
          Performance Summary
        </h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '20px'
        }}>
          <div style={{ textAlign: 'center', padding: '16px' }}>
            <Calendar size={32} style={{ color: '#3b82f6', marginBottom: '8px' }} />
            <h4 style={{ margin: '0 0 4px 0', fontSize: '20px', fontWeight: '600', color: '#1e293b' }}>
              Average Processing Time
            </h4>
            <p style={{ margin: '0', color: '#64748b' }}>45 days</p>
          </div>
          
          <div style={{ textAlign: 'center', padding: '16px' }}>
            <Award size={32} style={{ color: '#059669', marginBottom: '8px' }} />
            <h4 style={{ margin: '0 0 4px 0', fontSize: '20px', fontWeight: '600', color: '#1e293b' }}>
              Client Satisfaction
            </h4>
            <p style={{ margin: '0', color: '#64748b' }}>4.8/5.0</p>
          </div>
          
          <div style={{ textAlign: 'center', padding: '16px' }}>
            <TrendingUp size={32} style={{ color: '#7c3aed', marginBottom: '8px' }} />
            <h4 style={{ margin: '0 0 4px 0', fontSize: '20px', fontWeight: '600', color: '#1e293b' }}>
              Growth Rate
            </h4>
            <p style={{ margin: '0', color: '#64748b' }}>+18% YoY</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
