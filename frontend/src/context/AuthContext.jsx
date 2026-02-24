import React, { createContext, useEffect, useState } from "react";
import { authAPI, getToken, getUser, handleError, logout as logoutAPI, saveToken, saveUser } from "../services/api";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const savedToken = getToken();
    const savedUser = getUser();
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(savedUser);
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      const response = await authAPI.login({ email, password });
      const payload = response.data.data || {};
      const nextToken = payload.access_token;
      const nextUser = payload.user;
      if (!nextToken || !nextUser) {
        return { success: false, error: "Invalid login response" };
      }
      setToken(nextToken);
      setUser(nextUser);
      setIsAuthenticated(true);
      saveToken(nextToken);
      saveUser(nextUser);
      return { success: true, message: response.data.message };
    } catch (err) {
      const msg = handleError(err);
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await authAPI.register(userData);
      return { success: true, message: response.data.message };
    } catch (err) {
      const msg = handleError(err);
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    setError(null);
    logoutAPI();
  };

  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      const response = await authAPI.updateProfile(profileData);
      const updated = response.data.user;
      setUser(updated);
      saveUser(updated);
      return { success: true, message: response.data.message };
    } catch (err) {
      const msg = handleError(err);
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        error,
        isAuthenticated,
        login,
        register,
        logout,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = React.useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
