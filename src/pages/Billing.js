import React, { useState } from 'react';
import { Search, Plus, FileText, Download } from 'lucide-react';

const InvoiceCard = ({ invoice }) => (
  <div style={{
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    border: '1px solid #e2e8f0'
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
      <div>
        <h3 style={{ margin: '0 0 4px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
          Invoice #{invoice.invoiceNumber}
        </h3>
        <p style={{ margin: '0', fontSize: '14px', color: '#64748b' }}>
          {invoice.client}
        </p>
      </div>
      <span style={{
        padding: '4px 12px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: '500',
        backgroundColor: invoice.status === 'paid' ? '#dcfce7' : 
                         invoice.status === 'pending' ? '#fef3c7' : '#fef2f2',
        color: invoice.status === 'paid' ? '#166534' : 
               invoice.status === 'pending' ? '#92400e' : '#dc2626'
      }}>
        {invoice.status.toUpperCase()}
      </span>
    </div>
    
    <div style={{ marginBottom: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '14px', color: '#64748b' }}>Amount:</span>
        <span style={{ fontSize: '16px', fontWeight: '600', color: '#1e293b' }}>${invoice.amount}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '14px', color: '#64748b' }}>Issue Date:</span>
        <span style={{ fontSize: '14px', color: '#64748b' }}>{invoice.issueDate}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <span style={{ fontSize: '14px', color: '#64748b' }}>Due Date:</span>
        <span style={{ fontSize: '14px', color: '#64748b' }}>{invoice.dueDate}</span>
      </div>
    </div>
    
    <div style={{ display: 'flex', gap: '8px' }}>
      <button onClick={() => alert(`Downloading ${invoice.client} invoice`)} style={{
        flex: 1,
        padding: '8px 16px',
        backgroundColor: '#f8fafc',
        color: '#64748b',
        border: '1px solid #e2e8f0',
        borderRadius: '4px',
        fontSize: '12px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '4px'
      }}>
        <Download size={12} />
        Download
      </button>
      <button onClick={() => {
        if (invoice.status === 'paid') {
          alert(`Viewing details for ${invoice.client} invoice`);
        } else {
          alert(`Sending reminder to ${invoice.client}`);
        }
      }} style={{
        flex: 1,
        padding: '8px 16px',
        backgroundColor: '#3b82f6',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        fontSize: '12px',
        cursor: 'pointer'
      }}>
        {invoice.status === 'paid' ? 'View Details' : 'Send Reminder'}
      </button>
    </div>
  </div>
);

const Billing = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  const invoices = [
    {
      id: 1,
      invoiceNumber: 'INV-2025-001',
      client: 'Maria Rodriguez',
      amount: '4,500.00',
      status: 'paid',
      issueDate: 'Aug 15, 2025',
      dueDate: 'Sep 15, 2025'
    },
    {
      id: 2,
      invoiceNumber: 'INV-2025-002',
      client: 'Ahmed Hassan',
      amount: '3,200.00',
      status: 'pending',
      issueDate: 'Aug 20, 2025',
      dueDate: 'Sep 20, 2025'
    },
    {
      id: 3,
      invoiceNumber: 'INV-2025-003',
      client: 'Li Wei',
      amount: '5,800.00',
      status: 'overdue',
      issueDate: 'Jul 30, 2025',
      dueDate: 'Aug 30, 2025'
    },
    {
      id: 4,
      invoiceNumber: 'INV-2025-004',
      client: 'Carlos Mendez',
      amount: '6,200.00',
      status: 'pending',
      issueDate: 'Aug 22, 2025',
      dueDate: 'Sep 22, 2025'
    }
  ];

  const filteredInvoices = invoices.filter(invoice =>
    invoice.client.toLowerCase().includes(searchTerm.toLowerCase()) ||
    invoice.invoiceNumber.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h1 style={{ margin: '0 0 8px 0', fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
              Billing & Invoices
            </h1>
            <p style={{ margin: '0', color: '#64748b' }}>
              Manage invoices and track payments ({invoices.length} total invoices)
            </p>
          </div>
          <button onClick={() => setShowCreateModal(true)} style={{
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
            Create Invoice
          </button>
        </div>
        
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
            placeholder="Search invoices by client or invoice number..."
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

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
        gap: '20px'
      }}>
        {filteredInvoices.map((invoice) => (
          <InvoiceCard key={invoice.id} invoice={invoice} />
        ))}
      </div>
      
      {filteredInvoices.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '40px',
          color: '#64748b'
        }}>
          <FileText size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
          <p>No invoices found matching your search criteria.</p>
        </div>
      )}
    </div>
  );
};

export default Billing;
