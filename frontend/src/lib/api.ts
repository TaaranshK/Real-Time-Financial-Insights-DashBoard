import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor: attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ─── AUTH ───────────────────────────────────────────────────────────────────
export const registerUser = (data: {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}) => api.post('/api/auth/register', data);

export const loginUser = (data: { email: string; password: string }) =>
  api.post('/api/auth/login', data);

export const getProfile = () => api.get('/api/auth/profile');

export const updateProfile = (data: {
  username?: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}) => api.put('/api/auth/profile', data);

export const forgotPassword = (email: string) =>
  api.post('/api/auth/forgot-password', { email });

export const verifyOtp = (data: { email: string; otp: string }) =>
  api.post('/api/auth/verify-otp', data);

export const resetPassword = (data: { token: string; new_password: string }) =>
  api.post('/api/auth/reset-password', data);

export const changePassword = (data: {
  current_password: string;
  new_password: string;
}) => api.post('/api/auth/change-password', data);

// ─── PORTFOLIO ───────────────────────────────────────────────────────────────
export const createPortfolio = (data: {
  name: string;
  description?: string;
  portfolio_type?: string;
}) => api.post('/api/portfolio/portfolios', data);

export const getPortfolios = () => api.get('/api/portfolio/portfolios');

export const getPortfolio = (id: number) =>
  api.get(`/api/portfolio/portfolios/${id}`);

export const addHolding = (
  portfolioId: number,
  data: {
    stock_symbol: string;
    stock_name: string;
    quantity: number;
    buy_price: number;
    sector?: string;
  }
) => api.post(`/api/portfolio/portfolios/${portfolioId}/holdings`, data);

export const getHoldings = (portfolioId: number) =>
  api.get(`/api/portfolio/portfolios/${portfolioId}/holdings`);

export const updateHoldingPrice = (holdingId: number, new_price: number) =>
  api.put(`/api/portfolio/holdings/${holdingId}/price`, { new_price });

export const getPortfolioSummary = () => api.get('/api/portfolio/summary');

// ─── MARKET ANALYSIS ─────────────────────────────────────────────────────────
export const analyzeStock = (data: {
  stock_symbol: string;
  stock_name?: string;
  current_price?: number;
  sector?: string;
}) => api.post('/api/market-analysis/analyze', data);

export const getAnalyses = (limit = 10) =>
  api.get(`/api/market-analysis/analyses?limit=${limit}`);

export const getMarketNews = () => api.get('/api/market-analysis/news');

export default api;
