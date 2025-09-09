import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const isValidToken = (token) => {
  return token && typeof token === 'string' && token.trim().length > 0;
};

const isValidUser = (user) => {
  return user && typeof user === 'object' && user.id && user.email;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const token = localStorage.getItem('authToken');
        const savedUser = localStorage.getItem('currentUser');
        
        if (isValidToken(token) && savedUser) {
          const parsedUser = JSON.parse(savedUser);
          
          if (isValidUser(parsedUser)) {
            setUser(parsedUser);
            apiService.setToken(token);
            
            try {
              const currentUser = await apiService.getCurrentUser();
              if (isValidUser(currentUser)) {
                setUser(currentUser);
                localStorage.setItem('currentUser', JSON.stringify(currentUser));
              } else {
                logout();
              }
            } catch (error) {
              logout();
            }
          } else {
            logout();
          }
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        logout();
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      setLoading(true);
      
      const response = await apiService.login(email, password);
      
      if (!isValidToken(response.access_token) || !isValidUser(response.user)) {
        throw new Error('Login failed: Invalid authentication response');
      }
      
      setUser(response.user);
      
      return { success: true, user: response.user };
    } catch (error) {
      const errorMessage = error.message || 'Login failed';
      setError(errorMessage);
      setUser(null);
      
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const setAuth = (token, userData) => {
    if (token) {
      if (!userData || typeof userData !== 'object') {
        console.error('setAuth: userData is required when token is provided');
        return;
      }
      
      apiService.setToken(token);
      localStorage.setItem('authToken', token);
      localStorage.setItem('currentUser', JSON.stringify(userData));
      setUser(userData);
      setError(null);
    } else {
      apiService.clearAuth();
      localStorage.removeItem('authToken');
      localStorage.removeItem('currentUser');
      setUser(null);
      setError(null);
    }
  };

  const logout = (redirectToLogin = true) => {
    apiService.clearAuth();
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    setUser(null);
    setError(null);
    
    if (redirectToLogin) {
      return '/signin';
    }
    return null;
  };

  const isAuthenticated = () => {
    return !!user && !!apiService.getToken();
  };

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    setAuth,
    isAuthenticated,
    setError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
