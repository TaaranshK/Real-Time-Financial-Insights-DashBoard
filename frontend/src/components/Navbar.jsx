import { Link, useNavigate, useLocation } from 'react-router-dom'
import { clearToken } from '../api'
import './Navbar.css'

function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()

  // logout clears token and goes to login
  function handleLogout() {
    clearToken()
    navigate('/login')
  }

  // check if current path matches link
  function isActive(path) {
    return location.pathname === path ? 'active' : ''
  }

  return (
    <nav className="navbar">
      <div className="nav-brand">📈 FinMonitor</div>
      
      <div className="nav-links">
        <Link to="/" className={isActive('/')}>Dashboard</Link>
        <Link to="/portfolio" className={isActive('/portfolio')}>Portfolio</Link>
        <Link to="/ai" className={isActive('/ai')}>AI Analysis</Link>
        <Link to="/alerts" className={isActive('/alerts')}>Alerts</Link>
      </div>
      
      <button onClick={handleLogout} className="logout-btn">Logout</button>
    </nav>
  )
}

export default Navbar
