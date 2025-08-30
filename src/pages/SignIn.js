import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authAPI } from '../services/api';

const SignIn = () => {
  const [activePortal, setActivePortal] = useState(null); // Start with no portal selected
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const credentials = { email, password };
      const response = await authAPI.login(credentials);
      
      // Store authentication data
      await login(response.data.access_token, response.data.user);
      
      // Navigate based on user role and portal
      if (response.data.user.role === 'lawyer' || response.data.user.role === 'admin') {
        navigate('/dashboard');
      } else {
        // For client portal
        alert('Welcome to Client Portal! Client dashboard coming soon.');
        // navigate('/client-dashboard'); // Uncomment when client dashboard is ready
      }
    } catch (error) {
      console.error('Login error:', error);
      setError(error.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError('Passwords do not match!');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const userData = {
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        role: activePortal === 'lawyer' ? 'lawyer' : 'client'
      };

      const response = await authAPI.register(userData);
      
      alert(`Welcome ${firstName} ${lastName}! Your ${activePortal} account has been created. You can now sign in.`);
      
      // Reset form and switch to sign in
      setIsSignUp(false);
      setFirstName('');
      setLastName('');
      setConfirmPassword('');
      setPassword('');
      setEmail('');
    } catch (error) {
      console.error('Registration error:', error);
      setError(error.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setFirstName('');
    setLastName('');
    setError('');
  };

  const switchMode = (mode) => {
    setIsSignUp(mode === 'signup');
    resetForm();
  };

  const switchPortal = (portal) => {
    setActivePortal(portal);
    setIsSignUp(false);
    resetForm();
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center" style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      fontFamily: 'Inter, system-ui, -apple-system, sans-serif'
    }}>
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-12 col-lg-10 col-xl-8">
            
            {/* Header */}
            <div className="text-center mb-5">
              <h1 className="display-5 fw-bold text-white mb-3">
                Immigration Law Platform
              </h1>
              <p className="lead text-white-50">
                Comprehensive white-label branding and payment/invoice tracking features for immigration law firms
              </p>
            </div>

            {/* Portal Selection Cards */}
            <div className="row g-4 mb-5">
              {/* Show instruction when no portal is selected */}
              {!activePortal && (
                <div className="col-12 text-center mb-3">
                  <p className="text-white-50">
                    <i className="bi bi-hand-index me-2"></i>
                    Please select a portal to continue
                  </p>
                </div>
              )}
              
              {/* Law Firm Dashboard */}
              <div className="col-md-6">
                <div 
                  className={`card h-100 border-0 shadow-lg cursor-pointer transition-all ${
                    activePortal === 'lawyer' ? 'border-primary border-3' : 'border-light'
                  }`}
                  onClick={() => switchPortal('lawyer')}
                  style={{
                    transform: activePortal === 'lawyer' ? 'translateY(-5px)' : 'none',
                    transition: 'all 0.3s ease',
                    cursor: 'pointer',
                    opacity: activePortal && activePortal !== 'lawyer' ? 0.6 : 1
                  }}
                >
                  <div className="card-body p-4 text-center">
                    <div className="bg-primary bg-gradient rounded-circle d-inline-flex align-items-center justify-content-center mb-3" 
                         style={{ width: '64px', height: '64px' }}>
                      <i className="bi bi-briefcase text-white fs-3"></i>
                    </div>
                    <h3 className="card-title h4 mb-3">Law Firm Dashboard</h3>
                    <p className="card-text text-muted mb-4">
                      Manage hundreds of clients efficiently
                    </p>
                    
                    {/* Sign In/Up Form for Lawyers */}
                    {activePortal === 'lawyer' && (
                      <div className="mt-4" onClick={(e) => e.stopPropagation()}>
                        <div className="d-flex gap-2 mb-3">
                          <button 
                            className={`btn ${!isSignUp ? 'btn-primary' : 'btn-outline-primary'} flex-fill`}
                            onClick={(e) => { e.stopPropagation(); switchMode('signin'); }}
                          >
                            <i className="bi bi-box-arrow-in-right me-2"></i>
                            Sign In
                          </button>
                          <button 
                            className={`btn ${isSignUp ? 'btn-primary' : 'btn-outline-primary'} flex-fill`}
                            onClick={(e) => { e.stopPropagation(); switchMode('signup'); }}
                          >
                            <i className="bi bi-person-plus me-2"></i>
                            Sign Up
                          </button>
                        </div>
                        
                        <form onSubmit={isSignUp ? handleSignUp : handleSignIn} onClick={(e) => e.stopPropagation()}>
                          {error && (
                            <div className="alert alert-danger py-2 mb-3" role="alert">
                              <i className="bi bi-exclamation-triangle me-2"></i>
                              {error}
                            </div>
                          )}
                          
                          {isSignUp && (
                            <>
                              <div className="row mb-3">
                                <div className="col-6">
                                  <label className="form-label text-start d-block">First Name</label>
                                  <input
                                    type="text"
                                    className="form-control"
                                    placeholder="John"
                                    value={firstName}
                                    onChange={(e) => setFirstName(e.target.value)}
                                    required
                                    disabled={loading}
                                  />
                                </div>
                                <div className="col-6">
                                  <label className="form-label text-start d-block">Last Name</label>
                                  <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Doe"
                                    value={lastName}
                                    onChange={(e) => setLastName(e.target.value)}
                                    required
                                    disabled={loading}
                                  />
                                </div>
                              </div>
                            </>
                          )}
                          
                          <div className="mb-3">
                            <label className="form-label text-start d-block">Email</label>
                            <input
                              type="email"
                              className="form-control"
                              placeholder="lawyer@firm.com"
                              value={email}
                              onChange={(e) => setEmail(e.target.value)}
                              required
                              disabled={loading}
                            />
                          </div>
                          
                          <div className="mb-3">
                            <label className="form-label text-start d-block">Password</label>
                            <input
                              type="password"
                              className="form-control"
                              placeholder="Enter your password"
                              value={password}
                              onChange={(e) => setPassword(e.target.value)}
                              required
                              disabled={loading}
                            />
                          </div>
                          
                          {isSignUp && (
                            <div className="mb-3">
                              <label className="form-label text-start d-block">Confirm Password</label>
                              <input
                                type="password"
                                className="form-control"
                                placeholder="Confirm your password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                disabled={loading}
                              />
                            </div>
                          )}
                          
                          <button 
                            type="submit"
                            className="btn btn-dark w-100 py-2 mb-3"
                            disabled={loading}
                          >
                            {loading ? (
                              <>
                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                {isSignUp ? 'Creating Account...' : 'Signing In...'}
                              </>
                            ) : (
                              <>
                                <i className="bi bi-briefcase me-2"></i>
                                {isSignUp ? 'Create Lawyer Account' : 'Sign In as Lawyer'}
                              </>
                            )}
                          </button>
                        </form>
                        
                        {!isSignUp && (
                          <p className="small text-muted">
                            Forgot password? 
                            <a href="#" className="text-primary text-decoration-none ms-1">Reset here</a>
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Client Portal */}
              <div className="col-md-6">
                <div 
                  className={`card h-100 border-0 shadow-lg cursor-pointer transition-all ${
                    activePortal === 'client' ? 'border-success border-3' : 'border-light'
                  }`}
                  onClick={() => switchPortal('client')}
                  style={{
                    transform: activePortal === 'client' ? 'translateY(-5px)' : 'none',
                    transition: 'all 0.3s ease',
                    cursor: 'pointer',
                    opacity: activePortal && activePortal !== 'client' ? 0.6 : 1
                  }}
                >
                  <div className="card-body p-4 text-center">
                    <div className="bg-success bg-gradient rounded-circle d-inline-flex align-items-center justify-content-center mb-3" 
                         style={{ width: '64px', height: '64px' }}>
                      <i className="bi bi-person-circle text-white fs-3"></i>
                    </div>
                    <h3 className="card-title h4 mb-3">Client Portal</h3>
                    <p className="card-text text-muted mb-4">
                      Track your immigration case progress
                    </p>
                    
                    {/* Sign In/Up Form for Clients */}
                    {activePortal === 'client' && (
                      <div className="mt-4" onClick={(e) => e.stopPropagation()}>
                        <div className="d-flex gap-2 mb-3">
                          <button 
                            className={`btn ${!isSignUp ? 'btn-success' : 'btn-outline-success'} flex-fill`}
                            onClick={(e) => { e.stopPropagation(); switchMode('signin'); }}
                          >
                            <i className="bi bi-box-arrow-in-right me-2"></i>
                            Sign In
                          </button>
                          <button 
                            className={`btn ${isSignUp ? 'btn-success' : 'btn-outline-success'} flex-fill`}
                            onClick={(e) => { e.stopPropagation(); switchMode('signup'); }}
                          >
                            <i className="bi bi-person-plus me-2"></i>
                            Sign Up
                          </button>
                        </div>
                        
                        <form onSubmit={isSignUp ? handleSignUp : handleSignIn} onClick={(e) => e.stopPropagation()}>
                          {error && (
                            <div className="alert alert-danger py-2 mb-3" role="alert">
                              <i className="bi bi-exclamation-triangle me-2"></i>
                              {error}
                            </div>
                          )}
                          
                          {isSignUp && (
                            <>
                              <div className="row mb-3">
                                <div className="col-6">
                                  <label className="form-label text-start d-block">First Name</label>
                                  <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Maria"
                                    value={firstName}
                                    onChange={(e) => setFirstName(e.target.value)}
                                    required
                                    disabled={loading}
                                  />
                                </div>
                                <div className="col-6">
                                  <label className="form-label text-start d-block">Last Name</label>
                                  <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Garcia"
                                    value={lastName}
                                    onChange={(e) => setLastName(e.target.value)}
                                    required
                                    disabled={loading}
                                  />
                                </div>
                              </div>
                            </>
                          )}
                          
                          <div className="mb-3">
                            <label className="form-label text-start d-block">Email</label>
                            <input
                              type="email"
                              className="form-control"
                              placeholder="student@university.edu"
                              value={email}
                              onChange={(e) => setEmail(e.target.value)}
                              required
                              disabled={loading}
                            />
                          </div>
                          
                          <div className="mb-3">
                            <label className="form-label text-start d-block">Password</label>
                            <input
                              type="password"
                              className="form-control"
                              placeholder="Enter your password"
                              value={password}
                              onChange={(e) => setPassword(e.target.value)}
                              required
                              disabled={loading}
                            />
                          </div>
                          
                          {isSignUp && (
                            <div className="mb-3">
                              <label className="form-label text-start d-block">Confirm Password</label>
                              <input
                                type="password"
                                className="form-control"
                                placeholder="Confirm your password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                disabled={loading}
                              />
                            </div>
                          )}
                          
                          <button 
                            type="submit"
                            className="btn btn-success w-100 py-2 mb-3"
                            disabled={loading}
                          >
                            {loading ? (
                              <>
                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                {isSignUp ? 'Creating Account...' : 'Signing In...'}
                              </>
                            ) : (
                              <>
                                <i className="bi bi-person-circle me-2"></i>
                                {isSignUp ? 'Create Client Account' : 'Sign In as Client'}
                              </>
                            )}
                          </button>
                        </form>
                        
                        {!isSignUp && (
                          <p className="small text-muted">
                            Forgot password? 
                            <a href="#" className="text-success text-decoration-none ms-1">Reset here</a>
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Features Section */}
            <div className="row g-3 mb-4">
              <div className="col-6 col-lg-3">
                <div className="d-flex align-items-center text-white-50">
                  <i className="bi bi-robot me-2 text-success"></i>
                  <small>AI-Powered Document Analysis</small>
                </div>
              </div>
              <div className="col-6 col-lg-3">
                <div className="d-flex align-items-center text-white-50">
                  <i className="bi bi-calendar-check me-2 text-warning"></i>
                  <small>Automated Deadline Tracking</small>
                </div>
              </div>
              <div className="col-6 col-lg-3">
                <div className="d-flex align-items-center text-white-50">
                  <i className="bi bi-palette me-2 text-info"></i>
                  <small>White-label Branding</small>
                </div>
              </div>
              <div className="col-6 col-lg-3">
                <div className="d-flex align-items-center text-white-50">
                  <i className="bi bi-credit-card me-2 text-primary"></i>
                  <small>Integrated Billing System</small>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="text-center">
              <p className="text-white-50 mb-0">
                Both features are fully integrated into the existing dual-portal system with professional UI/UX design
                that maintains the clean, trustworthy aesthetic perfect for law firms.
              </p>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default SignIn;
