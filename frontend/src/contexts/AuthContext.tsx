import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getProfile } from '@/lib/api';

interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  role?: string;
  created_at?: string;
}

interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean;
  login: (token: string, refreshToken: string, user: User) => void;
  logout: () => void;
  updateUser: (user: User) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = useCallback((token: string, refreshToken: string, userData: User) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('user', JSON.stringify(userData));
    setAccessToken(token);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setAccessToken(null);
    setUser(null);
  }, []);

  const updateUser = useCallback((userData: User) => {
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  }, []);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setIsLoading(false);
        return;
      }
      try {
        setAccessToken(token);
        const response = await getProfile();
        // Handle nested response format: { message, user: {...} }
        const userData = response.data?.user || response.data;
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
      } catch (error) {
        console.error('Auth init failed:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        setAccessToken(null);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    initAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, accessToken, isLoading, login, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
