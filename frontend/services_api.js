"""
API SERVICE - Configure Axios and all API calls

This file handles:
- Axios instance setup
- Base URL configuration
- Authentication headers
- All API requests
"""

// src/services/api.js

import axios from 'axios';

// ============================================
// AXIOS INSTANCE SETUP
// ============================================

// Get API URL from environment
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Create Axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================
// AXIOS INTERCEPTORS
// ============================================

// Request Interceptor - Add token to headers
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('access_token');
    
    // Add token to headers if exists
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If token expired, logout user
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============================================
// AUTHENTICATION APIs
// ============================================

export const authAPI = {
  // Register new user
  register: (data) => api.post('/auth/register', data),
  
  // Login user
  login: (data) => api.post('/auth/login', data),
  
  // Get user profile
  getProfile: () => api.get('/auth/profile'),
  
  // Update profile
  updateProfile: (data) => api.put('/auth/profile', data),
  
  // Change password
  changePassword: (data) => api.post('/auth/change-password', data),
  
  // Logout (refresh token)
  refreshToken: (refreshToken) => api.post('/auth/refresh-token', { refresh_token: refreshToken }),
};

// ============================================
// PASSWORD RESET APIs
// ============================================

export const passwordAPI = {
  // Request password reset (send OTP)
  forgotPassword: (email) => api.post('/password/forgot-password', { email }),
  
  // Verify OTP
  verifyOTP: (email, otp) => api.post('/password/verify-otp', { email, otp }),
  
  // Reset password
  resetPassword: (email, newPassword) => api.post('/password/reset-password', { 
    email, 
    new_password: newPassword 
  }),
};

// ============================================
// PORTFOLIO APIs
// ============================================

export const portfolioAPI = {
  // Create new portfolio
  createPortfolio: (data) => api.post('/portfolio/portfolios', data),
  
  // Get all portfolios
  getPortfolios: () => api.get('/portfolio/portfolios'),
  
  // Get specific portfolio
  getPortfolio: (portfolioId) => api.get(`/portfolio/portfolios/${portfolioId}`),
  
  // Update portfolio
  updatePortfolio: (portfolioId, data) => api.put(`/portfolio/portfolios/${portfolioId}`, data),
  
  // Delete portfolio
  deletePortfolio: (portfolioId) => api.delete(`/portfolio/portfolios/${portfolioId}`),
};

// ============================================
// HOLDING (STOCK) APIs
// ============================================

export const holdingAPI = {
  // Get all holdings in portfolio
  getHoldings: (portfolioId) => api.get(`/portfolio/portfolios/${portfolioId}/holdings`),
  
  // Add stock to portfolio
  addHolding: (portfolioId, data) => api.post(`/portfolio/portfolios/${portfolioId}/holdings`, data),
  
  // Update stock price
  updatePrice: (holdingId, newPrice) => api.put(`/portfolio/holdings/${holdingId}/price`, { 
    new_price: newPrice 
  }),
  
  // Remove stock from portfolio
  removeHolding: (holdingId) => api.delete(`/portfolio/holdings/${holdingId}`),
  
  // Get portfolio summary
  getPortfolioSummary: (portfolioId) => api.get(`/portfolio/portfolios/${portfolioId}/summary`),
  
  // Get asset allocation
  getAllocation: (portfolioId) => api.get(`/portfolio/portfolios/${portfolioId}/allocation`),
};

// ============================================
// MARKET ANALYSIS APIs
// ============================================

export const analysisAPI = {
  // Analyze single stock
  analyzeStock: (data) => api.post('/market-analysis/analyze', data),
  
  // Get analysis history
  getAnalyses: (limit = 10) => api.get(`/market-analysis/analyses?limit=${limit}`),
  
  // Get specific analysis
  getAnalysis: (analysisId) => api.get(`/market-analysis/analyses/${analysisId}`),
  
  // Compare multiple stocks
  compareStocks: (data) => api.post('/market-analysis/compare', data),
  
  // Analyze portfolio with AI
  analyzePortfolio: (data) => api.post('/market-analysis/portfolio-analysis', data),
  
  // Get sentiment analysis
  getSentiment: (data) => api.post('/market-analysis/sentiment', data),
};

// ============================================
// HELPER FUNCTIONS
// ============================================

// Save token to localStorage
export const saveToken = (token) => {
  localStorage.setItem('access_token', token);
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};

// Save user to localStorage
export const saveUser = (user) => {
  localStorage.setItem('user', JSON.stringify(user));
};

// Get token from localStorage
export const getToken = () => localStorage.getItem('access_token');

// Get user from localStorage
export const getUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

// Logout - clear localStorage
export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
  delete api.defaults.headers.common['Authorization'];
};

// ============================================
// ERROR HANDLER
// ============================================

export const handleError = (error) => {
  if (error.response) {
    // Server responded with error status
    return error.response.data.message || 'An error occurred';
  } else if (error.request) {
    // Request made but no response
    return 'No response from server. Check your connection.';
  } else {
    // Error in request setup
    return error.message || 'An error occurred';
  }
};

export default api;
