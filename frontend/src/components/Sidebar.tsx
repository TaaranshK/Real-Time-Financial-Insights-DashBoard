import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Briefcase,
  TrendingUp,
  BarChart2,
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap,
} from 'lucide-react';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: Briefcase, label: 'Portfolio', path: '/portfolio' },
  { icon: TrendingUp, label: 'Holdings', path: '/holdings' },
  { icon: BarChart2, label: 'Market Analysis', path: '/market-analysis' },
  { icon: Settings, label: 'Settings', path: '/settings' },
];

interface SidebarProps {
  collapsed: boolean;
  setCollapsed: (v: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed, setCollapsed }) => {
  const location = useLocation();

  return (
    <motion.aside
      animate={{ width: collapsed ? 72 : 240 }}
      transition={{ duration: 0.25, ease: 'easeInOut' }}
      className="relative flex flex-col h-full flex-shrink-0 overflow-hidden"
      style={{
        background: 'hsl(var(--sidebar-background))',
        borderRight: '1px solid rgba(255,255,255,0.06)',
      }}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-white/5">
        <div className="w-9 h-9 flex-shrink-0 rounded-xl bg-gradient-primary flex items-center justify-center shadow-glow-primary">
          <Zap size={18} className="text-white" fill="white" />
        </div>
        <AnimatePresence>
          {!collapsed && (
            <motion.span
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.15 }}
              className="text-lg font-black text-gradient whitespace-nowrap"
            >
              FinVue
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      {/* Nav items */}
      <nav className="flex-1 py-4 px-2 space-y-1">
        {navItems.map((item) => {
          const isActive =
            item.path === '/'
              ? location.pathname === '/'
              : location.pathname.startsWith(item.path);
          return (
            <Link key={item.path} to={item.path}>
              <motion.div
                whileHover={{ x: 2 }}
                whileTap={{ scale: 0.97 }}
                className={`relative flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 cursor-pointer ${
                  isActive
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:text-foreground hover:bg-white/5'
                }`}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 rounded-r-full bg-gradient-primary"
                  />
                )}
                <item.icon
                  size={20}
                  className={`flex-shrink-0 ${isActive ? 'text-primary' : ''}`}
                />
                <AnimatePresence>
                  {!collapsed && (
                    <motion.span
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -8 }}
                      transition={{ duration: 0.15 }}
                      className="text-sm font-medium whitespace-nowrap"
                    >
                      {item.label}
                    </motion.span>
                  )}
                </AnimatePresence>
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* Collapse toggle */}
      <div className="p-3 border-t border-white/5">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setCollapsed(!collapsed)}
          className="w-full flex items-center justify-center p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-white/5 transition-colors duration-200"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </motion.button>
      </div>
    </motion.aside>
  );
};

export default Sidebar;
