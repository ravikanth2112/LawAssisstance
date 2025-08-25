import React, { useState } from 'react';

const ClientCard = ({ client }) => (
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
          <button className="btn btn-primary btn-sm flex-grow-1">
            <i className="bi bi-eye me-1"></i>
            View Details
          </button>
          <button className="btn btn-outline-secondary btn-sm">
            <i className="bi bi-pencil"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
);

const Clients = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');

  const clients = [
    {
      name: 'Maria Rodriguez',
      email: 'maria.rodriguez@email.com',
      caseType: 'I-485 Adjustment of Status',
      status: 'Active',
      lastContact: '2 days ago'
    },
    {
      name: 'John Chen',
      email: 'john.chen@email.com',
      caseType: 'H-1B Visa Application',
      status: 'Pending',
      lastContact: '1 week ago'
    },
    {
      name: 'Ahmed Hassan',
      email: 'ahmed.hassan@email.com',
      caseType: 'Family-Based Green Card',
      status: 'Active',
      lastContact: '3 days ago'
    },
    {
      name: 'Lisa Thompson',
      email: 'lisa.thompson@email.com',
      caseType: 'L-1 Visa Transfer',
      status: 'Completed',
      lastContact: '2 weeks ago'
    },
    {
      name: 'David Kim',
      email: 'david.kim@email.com',
      caseType: 'O-1 Extraordinary Ability',
      status: 'Active',
      lastContact: '1 day ago'
    },
    {
      name: 'Sofia Martinez',
      email: 'sofia.martinez@email.com',
      caseType: 'Citizenship Application',
      status: 'Pending',
      lastContact: '5 days ago'
    }
  ];

  const filteredClients = clients.filter(client => {
    const matchesSearch = client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.caseType.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'All' || client.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="p-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h2 mb-1">Client Management</h1>
          <p className="text-muted mb-0">Manage your immigration clients and cases</p>
        </div>
        <button className="btn btn-primary d-flex align-items-center">
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
              <button className="btn btn-outline-secondary w-100">
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
              <h4>247</h4>
              <p className="mb-0">Total Clients</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 bg-success text-white">
            <div className="card-body text-center">
              <i className="bi bi-check-circle fs-1 mb-2"></i>
              <h4>189</h4>
              <p className="mb-0">Active Cases</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 bg-warning text-white">
            <div className="card-body text-center">
              <i className="bi bi-clock fs-1 mb-2"></i>
              <h4>34</h4>
              <p className="mb-0">Pending Review</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card border-0 bg-info text-white">
            <div className="card-body text-center">
              <i className="bi bi-trophy fs-1 mb-2"></i>
              <h4>24</h4>
              <p className="mb-0">Completed This Month</p>
            </div>
          </div>
        </div>
      </div>

      {/* Client Cards */}
      <div className="row">
        {filteredClients.map((client, index) => (
          <ClientCard key={index} client={client} />
        ))}
      </div>

      {filteredClients.length === 0 && (
        <div className="text-center py-5">
          <i className="bi bi-search fs-1 text-muted mb-3"></i>
          <h5 className="text-muted">No clients found</h5>
          <p className="text-muted">Try adjusting your search criteria or add a new client.</p>
        </div>
      )}
    </div>
  );
};

export default Clients;
