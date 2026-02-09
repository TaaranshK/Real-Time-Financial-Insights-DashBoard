import { Routes, Route, Navigate } from 'react-router-dom'
import { isLoggedIn } from './api'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Portfolio from './pages/Portfolio'
import AIAnalysis from './pages/AIAnalysis'
import Alerts from './pages/Alerts'

// protects routes - redirects to login if not authenticated
function ProtectedRoute({ children }) {
  if (!isLoggedIn()) {
    return <Navigate to="/login" />
  }
  return children
}

function App() {
  return (
    <div>
      {/* show navbar on all pages except login */}
      {isLoggedIn() && <Navbar />}
      
      <Routes>
        {/* public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* protected routes - need to be logged in */}
        <Route path="/" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        
        <Route path="/portfolio" element={
          <ProtectedRoute>
            <Portfolio />
          </ProtectedRoute>
        } />
        
        <Route path="/ai" element={
          <ProtectedRoute>
            <AIAnalysis />
          </ProtectedRoute>
        } />
        
        <Route path="/alerts" element={
          <ProtectedRoute>
            <Alerts />
          </ProtectedRoute>
        } />
        
        {/* catch all - redirect to dashboard */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  )
}

export default App
