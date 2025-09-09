import { loginApi } from '../utils/authApi.js';

const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('authToken');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }

  getToken() {
    return this.token || localStorage.getItem('authToken');
  }

  clearAuth() {
    this.token = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = Bearer ;
    }

    return headers;
  }

  async request(endpoint, options = {}) {
    const url = ${this.baseURL};
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (response.status === 401) {
        this.clearAuth();
        window.location.href = '/signin';
        throw new Error('Authentication required');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || HTTP : );
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      
      return await response.text();
    } catch (error) {
      console.error(API Request failed for :, error);
      throw error;
    }
  }

  async get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString();
    const url = query ? ${endpoint}? : endpoint;
    return this.request(url);
  }

  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async login(email, password) {
    try {
      const data = await loginApi(email, password);
      this.setToken(data.access_token);

      try {
        const currentUser = await this.getCurrentUser();
        if (currentUser) {
          localStorage.setItem('currentUser', JSON.stringify(currentUser));
          return {
            access_token: data.access_token,
            token_type: data.token_type || 'bearer',
            user: currentUser
          };
        }
      } catch (err) {
        this.clearAuth();
        throw new Error('Login verification failed');
      }

      this.clearAuth();
      throw new Error('Login verification failed');
    } catch (error) {
      this.clearAuth();
      throw error;
    }
  }

  async getCurrentUser() {
    return this.get('/api/auth/me');
  }

  logout() {
    this.clearAuth();
  }

  async getClients(params = {}) {
    return this.get('/api/clients', params);
  }

  async getDashboardStats() {
    return this.get('/api/dashboard/stats');
  }
}

const apiService = new ApiService();
export default apiService;
