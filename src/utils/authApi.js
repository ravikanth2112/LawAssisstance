/**
 * Strict Login API Helper
 * Implements fail-closed security for authentication
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Strict login API function
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<{access_token: string, token_type: string, user: object}>}
 * @throws {Error} On any failure condition
 */
export const loginApi = async (email, password) => {
  if (!email || !password) {
    throw new Error('Email and password are required');
  }

  let response;
  
  try {
    // POST to /api/auth/login
    response = await fetch(${API_BASE_URL}/api/auth/login, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
  } catch (networkError) {
    // Network error (no internet, server down, etc.)
    throw new Error('Network error: Unable to connect to server');
  }

  // STRICT: If response is not 200, parse JSON and throw Error
  if (response.status !== 200) {
    let errorMessage = 'Login failed';
    
    try {
      const errorData = await response.json();
      // Use backend error detail if available
      errorMessage = errorData.detail || errorData.message || HTTP : ;
    } catch (jsonError) {
      // If JSON parsing fails, use HTTP status
      errorMessage = HTTP : ;
    }
    
    throw new Error(errorMessage);
  }

  // Parse JSON response
  let data;
  try {
    data = await response.json();
  } catch (jsonError) {
    throw new Error('Invalid server response: Unable to parse JSON');
  }

  // STRICT: If response is 200 but no access_token, throw Error
  if (!data.access_token || typeof data.access_token !== 'string' || data.access_token.trim() === '') {
    throw new Error('Missing access token');
  }

  // Validate required fields
  if (!data.user || typeof data.user !== 'object') {
    throw new Error('Invalid server response: Missing user data');
  }

  // Return success data - no mocks, no interceptors
  return {
    access_token: data.access_token,
    token_type: data.token_type || 'bearer',
    user: data.user
  };
};

export default { loginApi };
