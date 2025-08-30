// API configuration and base setup
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// API service class
class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('authToken');
  }

  // Set authorization token
  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }

  // Get authorization headers
  getHeaders(contentType = 'application/json') {
    const headers = {
      'Content-Type': contentType,
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  // Generic API request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error?.message || data.detail || 'API request failed');
      }

      return data;
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  }

  // GET request
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  // POST request
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // PUT request
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // DELETE request
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Create singleton instance
const apiService = new ApiService();

// Authentication API
export const authAPI = {
  // Login user
  async login(email, password) {
    const response = await apiService.post('/auth/login', { email, password });
    if (response.success && response.data.access_token) {
      apiService.setToken(response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
      localStorage.setItem('currentUser', JSON.stringify(response.data.user));
    }
    return response;
  },

  // Register user
  async register(userData) {
    const response = await apiService.post('/auth/register', userData);
    return response;
  },

  // Logout user
  logout() {
    apiService.setToken(null);
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('currentUser');
  },

  // Get current user
  async getCurrentUser() {
    const response = await apiService.get('/auth/me');
    return response;
  },

  // Refresh token
  async refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) throw new Error('No refresh token available');
    
    const response = await apiService.post('/auth/refresh', { refresh_token: refreshToken });
    if (response.success && response.data.access_token) {
      apiService.setToken(response.data.access_token);
    }
    return response;
  },
};

// Dashboard API
export const dashboardAPI = {
  // Get dashboard data
  async getDashboardData() {
    const response = await apiService.get('/dashboard/');
    return response;
  },

  // Get dashboard summary
  async getDashboardSummary() {
    const response = await apiService.get('/dashboard/summary');
    return response;
  },
};

// Cases API
export const casesAPI = {
  // Get all cases
  async getCases(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/cases/?${queryString}` : '/cases/';
    const response = await apiService.get(endpoint);
    return response;
  },

  // Get case by ID
  async getCase(caseId) {
    const response = await apiService.get(`/cases/${caseId}`);
    return response;
  },

  // Create new case
  async createCase(caseData) {
    const response = await apiService.post('/cases/', caseData);
    return response;
  },

  // Update case
  async updateCase(caseId, caseData) {
    const response = await apiService.put(`/cases/${caseId}`, caseData);
    return response;
  },

  // Get case statistics
  async getCaseStatistics() {
    const response = await apiService.get('/cases/statistics');
    return response;
  },
};

// Users API
export const usersAPI = {
  // Get all users
  async getUsers(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/users/?${queryString}` : '/users/';
    const response = await apiService.get(endpoint);
    return response;
  },

  // Get user by ID
  async getUser(userId) {
    const response = await apiService.get(`/users/${userId}`);
    return response;
  },

  // Update user
  async updateUser(userId, userData) {
    const response = await apiService.put(`/users/${userId}`, userData);
    return response;
  },

  // Get current user profile
  async getProfile() {
    const response = await apiService.get('/users/me');
    return response;
  },
};

// Lawyers API
export const lawyersAPI = {
  // Get all lawyers
  async getLawyers(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/lawyers/?${queryString}` : '/lawyers/';
    const response = await apiService.get(endpoint);
    return response;
  },

  // Get lawyer by ID
  async getLawyer(lawyerId) {
    const response = await apiService.get(`/lawyers/${lawyerId}`);
    return response;
  },

  // Create lawyer profile
  async createLawyer(lawyerData) {
    const response = await apiService.post('/lawyers/', lawyerData);
    return response;
  },

  // Update lawyer profile
  async updateLawyer(lawyerId, lawyerData) {
    const response = await apiService.put(`/lawyers/${lawyerId}`, lawyerData);
    return response;
  },
};

// Clients API
export const clientsAPI = {
  // Get all clients
  async getClients(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/clients/?${queryString}` : '/clients/';
    const response = await apiService.get(endpoint);
    return response;
  },

  // Get client by ID
  async getClient(clientId) {
    const response = await apiService.get(`/clients/${clientId}`);
    return response;
  },

  // Create client profile
  async createClient(clientData) {
    const response = await apiService.post('/clients/', clientData);
    return response;
  },

  // Update client profile
  async updateClient(clientId, clientData) {
    const response = await apiService.put(`/clients/${clientId}`, clientData);
    return response;
  },
};

// Health check
export const healthAPI = {
  async check() {
    const response = await apiService.get('/health');
    return response;
  },
};

export default apiService;
