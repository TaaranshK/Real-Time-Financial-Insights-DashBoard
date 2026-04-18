import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, ChevronDown, User, LogOut, Settings } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const Topbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const initials = user
    ? `${user.first_name?.[0] ?? user.username?.[0] ?? 'U'}${user.last_name?.[0] ?? ''}`.toUpperCase()
    : 'U';

  const displayName = user?.first_name
    ? `${user.first_name} ${user.last_name ?? ''}`.trim()
    : user?.username ?? 'User';

  return (
    <header
      className="flex items-center justify-between px-6 h-16 flex-shrink-0"
      style={{
        borderBottom: '1px solid rgba(255,255,255,0.06)',
        background: 'rgba(15, 23, 42, 0.8)',
        backdropFilter: 'blur(20px)',
      }}
    >
      {/* Left: current time / greeting */}
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-profit animate-pulse" />
        <span className="text-sm text-muted-foreground">Live Market Data</span>
      </div>

      {/* Right: bell + user */}
      <div className="flex items-center gap-3">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="w-9 h-9 rounded-xl flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-white/5 transition-all"
        >
          <Bell size={18} />
        </motion.button>

        {/* User dropdown */}
        <div className="relative">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-white/5 transition-all duration-200"
          >
            <div className="w-8 h-8 rounded-xl bg-gradient-primary flex items-center justify-center text-xs font-bold text-white">
              {initials}
            </div>
            <span className="text-sm font-medium text-foreground hidden sm:block">{displayName}</span>
            <ChevronDown size={14} className="text-muted-foreground hidden sm:block" />
          </motion.button>

          <AnimatePresence>
            {dropdownOpen && (
              <motion.div
                initial={{ opacity: 0, y: -8, scale: 0.96 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -8, scale: 0.96 }}
                transition={{ duration: 0.15 }}
                className="absolute right-0 top-12 w-52 glass-card py-2 z-50"
                style={{ border: '1px solid rgba(255,255,255,0.1)' }}
              >
                <div className="px-4 py-2 border-b border-white/5">
                  <p className="text-sm font-semibold text-foreground">{displayName}</p>
                  <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
                </div>
                <button
                  onClick={() => { navigate('/settings'); setDropdownOpen(false); }}
                  className="w-full flex items-center gap-3 px-4 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-white/5 transition-colors"
                >
                  <Settings size={15} />
                  Settings
                </button>
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-3 px-4 py-2 text-sm text-loss hover:bg-loss/10 transition-colors"
                >
                  <LogOut size={15} />
                  Logout
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  );
};

export default Topbar;
