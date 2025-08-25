import React, { useState } from 'react';

const ClientCard = ({ client, onViewDetails, onEdit, onDelete, onCall, onEmail }) => (
  <div className="col-lg-4 col-md-6 mb-4">
    <div className="card border-0 shadow-sm h-100">
      <div className="card-body">
        <div className="d-flex align-items-center mb-3">
          <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" style={{width: '50px', height: '50px'}}>
            <i className="bi bi-person text-white fs-4"></i>
          </div>
          <div className="flex-grow-1">
            <h6 className="card-title mb-1">{client.name}</h6>
            <small className="text-muted">{client.email}</small>
          </div>
          <div className="dropdown">
            <button className="btn btn-outline-secondary btn-sm dropdown-toggle" data-bs-toggle="dropdown">
              <i className="bi bi-three-dots"></i>
            </button>
            <ul className="dropdown-menu">
              <li><button className="dropdown-item" onClick={() => onCall(client)}><i className="bi bi-telephone me-2"></i>Call</button></li>
              <li><button className="dropdown-item" onClick={() => onEmail(client)}><i className="bi bi-envelope me-2"></i>Email</button></li>
              <li><hr className="dropdown-divider"/></li>
              <li><button className="dropdown-item text-danger" onClick={() => onDelete(client)}><i className="bi bi-trash me-2"></i>Delete</button></li>
            </ul>
          </div>
        </div>
        
        <div className="mb-3">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <span className="fw-medium">Case Type:</span>
            <span className="text-muted">{client.caseType}</span>
          </div>
          <div className="d-flex justify-content-between align-items-center mb-2">
            <span className="fw-medium">Status:</span>
            <span className={`badge bg-${client.status === 'Active' ? 'success' : client.status === 'Pending' ? 'warning' : 'secondary'}`}>
              {client.status}
            </span>
          </div>
          <div className="d-flex justify-content-between align-items-center">
            <span className="fw-medium">Last Contact:</span>
            <span className="text-muted">{client.lastContact}</span>
          </div>
        </div>
        
        <div className="d-flex gap-2">
          <button 
            className="btn btn-primary btn-sm flex-grow-1"
            onClick={() => onViewDetails(client)}
          >
            <i className="bi bi-eye me-1"></i>
            View Details
          </button>
          <button 
            className="btn btn-outline-secondary btn-sm"
            onClick={() => onEdit(client)}
          >
            <i className="bi bi-pencil"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
);

const AddClientModal = ({ show, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    caseType: '',
    status: 'Active'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ name: '', email: '', phone: '', caseType: '', status: 'Active' });
    onClose();
  };

  if (!show) return null;

  return (
    <div className="modal show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Add New Client</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  className="form-control"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  className="form-control"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Phone</label>
                <input
                  type="tel"
                  className="form-control"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Case Type</label>
                <select
                  className="form-select"
                  value={formData.caseType}
                  onChange={(e) => setFormData({...formData, caseType: e.target.value})}
                  required
                >
                  <option value="">Select Case Type</option>
                  <option value="I-485 Adjustment of Status">I-485 Adjustment of Status</option>
                  <option value="H-1B Visa Application">H-1B Visa Application</option>
                  <option value="Family-Based Green Card">Family-Based Green Card</option>
                  <option value="L-1 Visa Transfer">L-1 Visa Transfer</option>
                  <option value="O-1 Extraordinary Ability">O-1 Extraordinary Ability</option>
                  <option value="Citizenship Application">Citizenship Application</option>
                </select>
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
              <button type="submit" className="btn btn-primary">Add Client</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

const Clients = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [showAddModal, setShowAddModal] = useState(false);
  const [clients, setClients] = useState([
    {
      id: 1,
      name: 'Maria Rodriguez',
      email: 'maria.rodriguez@email.com',
      phone: '+1 (555) 123-4567',
      caseType: 'I-485 Adjustment of Status',
      status: 'Active',
      lastContact: '2 days ago'
    },
    {
      id: 2,
      name: 'John Chen',
      email: 'john.chen@email.com',
      phone: '+1 (555) 234-5678',
      caseType: 'H-1B Visa Application',
      status: 'Pending',
      lastContact: '1 week ago'
    },
    {
      id: 3,
      name: 'Ahmed Hassan',
      email: 'ahmed.hassan@email.com',
      phone: '+1 (555) 345-6789',
      caseType: 'Family-Based Green Card',
      status: 'Active',
      lastContact: '3 days ago'
    },
    {
      id: 4,
      name: 'Lisa Thompson',
      email: 'lisa.thompson@email.com',
      phone: '+1 (555) 456-7890',
      caseType: 'L-1 Visa Transfer',
      status: 'Completed',
      lastContact: '2 weeks ago'
    },
    {
      id: 5,
      name: 'David Kim',
      email: 'david.kim@email.com',
      phone: '+1 (555) 567-8901',
      caseType: 'O-1 Extraordinary Ability',
      status: 'Active',
      lastContact: '1 day ago'
    },
    {
      id: 6,
      name: 'Sofia Martinez',
      email: 'sofia.martinez@email.com',
      phone: '+1 (555) 678-9012',
      caseType: 'Citizenship Application',
      status: 'Pending',
      lastContact: '5 days ago'
    }
  ]);

  const filteredClients = clients.filter(client => {
    const matchesSearch = client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.caseType.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'All' || client.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleAddClient = (newClient) => {
    const client = {
      ...newClient,
      id: clients.length + 1,
      lastContact: 'Just added'
    };
    setClients([...clients, client]);
    alert(`Client "${newClient.name}" added successfully!`);
  };

  const handleViewDetails = (client) => {
    alert(`Viewing details for ${client.name}\n\nCase: ${client.caseType}\nStatus: ${client.status}\nEmail: ${client.email}\nPhone: ${client.phone}`);
  };

  const handleEdit = (client) => {
    alert(`Editing client: ${client.name}`);
  };

  const handleDelete = (client) => {
    if (window.confirm(`Are you sure you want to delete ${client.name}?`)) {
      setClients(clients.filter(c => c.id !== client.id));
      alert(`Client "${client.name}" deleted successfully!`);
    }
  };

  const handleCall = (client) => {
    alert(`Calling ${client.name} at ${client.phone}`);
  };

  const handleEmail = (client) => {
    alert(`Opening email to ${client.name} (${client.email})`);
  };

  const handleMoreFilters = () => {
    alert('Advanced filters functionality would be implemented here');
  };

  return (
    <div className="p-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h2 mb-1">Client Management</h1>
          <p className="text-muted mb-0">Manage your immigration clients and cases</p>
        </div>
        <button 
          className="btn btn-primary d-flex align-items-center"
          onClick={() => setShowAddModal(true)}
        >
          <i className="bi bi-plus-circle me-2"></i>
          Add New Client
        </button>
      </div>

      {/* Search and Filters */}
      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-md-6">
              <div className="input-group">
                <span className="input-group-text">
                  <i className="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Search clients by name, email, or case type..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="col-md-3">
              <select
                className="form-select"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="All">All Statuses</option>
                <option value="Active">Active</option>
                <option value="Pending">Pending</option>
                <option value="Completed">Completed</option>
              </select>
            </div>
            <div className="col-md-3">
              <button 
                className="btn btn-outline-secondary w-100"
                onClick={handleMoreFilters}
              >
                <i className="bi bi-funnel me-2"></i>
                More Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card border-0 bg-primary text-white">
            <div className="card-body text-center">
              <i className="bi bi-people fs-1 mb-2"></i>
              <h4>{clients.length}</h4>
              <p className="mb-0">Total Clients</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 bg-success text-white">
            <div className="card-body text-center">
              <i className="bi bi-check-circle fs-1 mb-2"></i>
              <h4>{clients.filter(c => c.status === 'Active').length}</h4>
              <p className="mb-0">Active Cases</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 bg-warning text-white">
            <div className="card-body text-center">
              <i className="bi bi-clock fs-1 mb-2"></i>
              <h4>{clients.filter(c => c.status === 'Pending').length}</h4>
              <p className="mb-0">Pending Review</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 bg-info text-white">
            <div className="card-body text-center">
              <i className="bi bi-trophy fs-1 mb-2"></i>
              <h4>{clients.filter(c => c.status === 'Completed').length}</h4>
              <p className="mb-0">Completed This Month</p>
            </div>
          </div>
        </div>
      </div>

      {/* Client Cards */}
      <div className="row">
        {filteredClients.map((client) => (
          <ClientCard 
            key={client.id} 
            client={client}
            onViewDetails={handleViewDetails}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onCall={handleCall}
            onEmail={handleEmail}
          />
        ))}
      </div>

      {filteredClients.length === 0 && (
        <div className="text-center py-5">
          <i className="bi bi-search fs-1 text-muted mb-3"></i>
          <h5 className="text-muted">No clients found</h5>
          <p className="text-muted">Try adjusting your search criteria or add a new client.</p>
        </div>
      )}

      {/* Add Client Modal */}
      <AddClientModal
        show={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSubmit={handleAddClient}
      />
    </div>
  );
};

export default Clients;

