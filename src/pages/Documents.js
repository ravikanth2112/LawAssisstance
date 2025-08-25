import React, { useState } from 'react';
import { Search, Plus, Filter, Download, Eye, MoreHorizontal, FileText, Upload } from 'lucide-react';

const DocumentCard = ({ document }) => (
  <div style={{
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    border: '1px solid #e2e8f0'
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{
          width: '48px',
          height: '48px',
          borderRadius: '8px',
          backgroundColor: document.type === 'PDF' ? '#dc2626' : 
                           document.type === 'DOCX' ? '#2563eb' : '#059669',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginRight: '12px'
        }}>
          <FileText size={20} color="white" />
        </div>
        <div>
          <h3 style={{ margin: '0 0 4px 0', fontSize: '16px', fontWeight: '600', color: '#1e293b' }}>
            {document.name}
          </h3>
          <p style={{ margin: '0', fontSize: '14px', color: '#64748b' }}>
            {document.client} • {document.type} • {document.size}
          </p>
        </div>
      </div>
      <button style={{
        padding: '8px',
        backgroundColor: 'transparent',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        color: '#64748b'
      }}>
        <MoreHorizontal size={16} />
      </button>
    </div>
    
    <div style={{ marginBottom: '16px' }}>
      <p style={{ margin: '0', fontSize: '14px', color: '#64748b' }}>
        <strong>Case:</strong> {document.caseType}
      </p>
      <p style={{ margin: '4px 0 0 0', fontSize: '14px', color: '#64748b' }}>
        <strong>Last Modified:</strong> {document.lastModified}
      </p>
    </div>
    
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{
        padding: '4px 12px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: '500',
        backgroundColor: document.status === 'Approved' ? '#dcfce7' : 
                         document.status === 'Under Review' ? '#fef3c7' : '#f3f4f6',
        color: document.status === 'Approved' ? '#166534' : 
               document.status === 'Under Review' ? '#92400e' : '#374151'
      }}>
        {document.status}
      </span>
      <div style={{ display: 'flex', gap: '8px' }}>
        <button onClick={() => alert(`Viewing ${document.name}`)} style={{
          padding: '6px 12px',
          backgroundColor: '#f8fafc',
          color: '#64748b',
          border: '1px solid #e2e8f0',
          borderRadius: '4px',
          fontSize: '12px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '4px'
        }}>
          <Eye size={12} />
          View
        </button>
        <button onClick={() => alert(`Downloading ${document.name}`)} style={{
          padding: '6px 12px',
          backgroundColor: '#3b82f6',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          fontSize: '12px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '4px'
        }}>
          <Download size={12} />
          Download
        </button>
      </div>
    </div>
  </div>
);

const Documents = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('All');
  
  const documents = [
    {
      id: 1,
      name: 'I-485 Application Form',
      client: 'Maria Rodriguez',
      type: 'PDF',
      size: '2.3 MB',
      caseType: 'Family-based Green Card',
      status: 'Approved',
      lastModified: 'Aug 22, 2025'
    },
    {
      id: 2,
      name: 'H-1B Petition Package',
      client: 'Ahmed Hassan',
      type: 'DOCX',
      size: '1.8 MB',
      caseType: 'H-1B Visa Application',
      status: 'Under Review',
      lastModified: 'Aug 20, 2025'
    },
    {
      id: 3,
      name: 'Employment Authorization',
      client: 'Li Wei',
      type: 'PDF',
      size: '950 KB',
      caseType: 'EB-1 Petition',
      status: 'Approved',
      lastModified: 'Aug 23, 2025'
    },
    {
      id: 4,
      name: 'L-1 Transfer Documents',
      client: 'Priya Patel',
      type: 'ZIP',
      size: '4.2 MB',
      caseType: 'L-1 Visa Transfer',
      status: 'Draft',
      lastModified: 'Aug 15, 2025'
    },
    {
      id: 5,
      name: 'Asylum Application I-589',
      client: 'Carlos Mendez',
      type: 'PDF',
      size: '3.1 MB',
      caseType: 'Asylum Application',
      status: 'Under Review',
      lastModified: 'Aug 21, 2025'
    },
    {
      id: 6,
      name: 'STEM OPT Extension',
      client: 'Sarah Kim',
      type: 'DOCX',
      size: '1.2 MB',
      caseType: 'STEM OPT Extension',
      status: 'Draft',
      lastModified: 'Aug 19, 2025'
    }
  ];

  const filteredDocuments = documents.filter(doc =>
    doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.client.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.caseType.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h1 style={{ margin: '0 0 8px 0', fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
              Documents
            </h1>
            <p style={{ margin: '0', color: '#64748b' }}>
              Manage case documents and files ({documents.length} total documents)
            </p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button onClick={() => setShowUploadModal(true)} style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '12px 20px',
              backgroundColor: 'white',
              color: '#64748b',
              border: '1px solid #e2e8f0',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500'
            }}>
              <Upload size={16} />
              Upload Documents
            </button>
            <button style={{
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
              New Document
            </button>
          </div>
        </div>
        
        {/* Search and Filter Bar */}
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div style={{ position: 'relative', flex: 1, maxWidth: '400px' }}>
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
              placeholder="Search documents by name, client, or case type..."
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
          <button style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '12px 16px',
            backgroundColor: 'white',
            border: '1px solid #e2e8f0',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '14px',
            color: '#64748b'
          }}>
            <Filter size={16} />
            Filter
          </button>
        </div>
      </div>

      {/* Documents Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))',
        gap: '20px'
      }}>
        {filteredDocuments.map((document) => (
          <DocumentCard key={document.id} document={document} />
        ))}
      </div>
      
      {filteredDocuments.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '40px',
          color: '#64748b'
        }}>
          <FileText size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
          <p>No documents found matching your search criteria.</p>
        </div>
      )}
    </div>
  );
};

export default Documents;
