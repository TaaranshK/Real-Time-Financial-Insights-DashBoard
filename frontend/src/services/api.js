import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post("/auth/register", data),
  login: (data) => api.post("/auth/login", data),
  getProfile: () => api.get("/auth/profile"),
  updateProfile: (data) => api.put("/auth/profile", data),
};

export const portfolioAPI = {
  createPortfolio: (data) => api.post("/portfolio/portfolios", data),
  getPortfolios: () => api.get("/portfolio/portfolios"),
  getPortfolio: (portfolioId) => api.get(`/portfolio/portfolios/${portfolioId}`),
  addHolding: (portfolioId, data) => api.post(`/portfolio/portfolios/${portfolioId}/holdings`, data),
  getHoldings: (portfolioId) => api.get(`/portfolio/portfolios/${portfolioId}/holdings`),
};

export const holdingAPI = {
  updatePrice: (holdingId, newPrice) =>
    api.put(`/portfolio/holdings/${holdingId}/price`, { new_price: newPrice }),
};

export const analysisAPI = {
  analyzeStock: (data) => api.post("/market-analysis/analyze", data),
  getAnalyses: (limit = 10) => api.get(`/market-analysis/analyses?limit=${limit}`),
};

export const saveToken = (token) => {
  localStorage.setItem("access_token", token);
};

export const saveUser = (user) => {
  localStorage.setItem("user", JSON.stringify(user));
};

export const getToken = () => localStorage.getItem("access_token");

export const getUser = () => {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
};

export const handleError = (error) => {
  if (error.response?.data?.message) return error.response.data.message;
  if (error.response?.data?.detail) return error.response.data.detail;
  if (error.request) return "No response from server.";
  return error.message || "An error occurred";
};

export default api;
