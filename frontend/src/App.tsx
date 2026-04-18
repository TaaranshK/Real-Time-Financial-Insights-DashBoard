import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import ProtectedRoute from './components/ProtectedRoute';
import AppLayout from './components/AppLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import Dashboard from './pages/Dashboard';
import Portfolio from './pages/Portfolio';
import Holdings from './pages/Holdings';
import MarketAnalysis from './pages/MarketAnalysis';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';

const queryClient = new QueryClient();

const App = () => (
  <ErrorBoundary>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: 'rgba(15, 23, 42, 0.95)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: 'hsl(210, 40%, 96%)',
              borderRadius: '12px',
              backdropFilter: 'blur(20px)',
              fontSize: '14px',
              fontFamily: 'Inter, sans-serif',
            },
            success: { iconTheme: { primary: 'hsl(158, 64%, 52%)', secondary: 'white' } },
            error: { iconTheme: { primary: 'hsl(350, 89%, 60%)', secondary: 'white' } },
          }}
        />
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />

          {/* Protected routes */}
          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<Dashboard />} />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/holdings" element={<Holdings />} />
            <Route path="/market-analysis" element={<MarketAnalysis />} />
            <Route path="/settings" element={<Settings />} />
          </Route>

          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
    </QueryClientProvider>
  </ErrorBoundary>
);

export default App;
