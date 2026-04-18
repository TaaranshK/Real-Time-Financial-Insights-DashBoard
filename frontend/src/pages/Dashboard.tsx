import { useState, useEffect, useRef } from 'react';
import { motion, Variants } from 'framer-motion';
import {
  Briefcase, TrendingUp, DollarSign, BarChart3,
  ArrowUpRight, ArrowDownRight, Newspaper, RefreshCw
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { useAuth } from '@/contexts/AuthContext';
import { getPortfolioSummary, getAnalyses, getMarketNews } from '@/lib/api';
import toast from 'react-hot-toast';

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } },
};
const cardVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

// Animated number counter hook
function useCountUp(target: number, duration = 1200) {
  const [count, setCount] = useState(0);
  const start = useRef<number | null>(null);
  useEffect(() => {
    if (target === 0) { setCount(0); return; }
    start.current = null;
    const step = (timestamp: number) => {
      if (!start.current) start.current = timestamp;
      const progress = Math.min((timestamp - start.current) / duration, 1);
      setCount(Math.floor(progress * target));
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [target, duration]);
  return count;
}

const formatCurrency = (v: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 }).format(v);

// Mock area chart data (for demo portfolio performance)
const generateAreaData = () => {
  const data = [];
  let value = 10000;
  for (let i = 0; i < 30; i++) {
    value = value * (1 + (Math.random() - 0.45) * 0.04);
    data.push({ day: `Day ${i + 1}`, value: Math.round(value) });
  }
  return data;
};
const areaData = generateAreaData();

const SECTOR_COLORS = ['#6366f1', '#22d3ee', '#10b981', '#f59e0b', '#f43f5e', '#a855f7', '#3b82f6'];

interface SummaryData {
  total_portfolios: number;
  total_holdings: number;
  total_invested: number;
  total_current_value: number;
  profit_loss: number;
  pct_change: number;
}

interface Analysis {
  id: number;
  stock_symbol: string;
  stock_name?: string;
  sentiment?: string;
  market_sentiment?: string;
  recommendation?: string | {
    action?: string;
    confidence?: string | number;
    reason?: string;
  };
  created_at?: string;
}

interface NewsItem {
  title: string;
  source?: string;
  url?: string;
  published_at?: string;
}

function StatCard({ icon: Icon, label, value, suffix, isProfit, isCurrency, color }: {
  icon: React.ElementType; label: string; value: number; suffix?: string;
  isProfit?: boolean; isCurrency?: boolean; color?: string;
}) {
  const count = useCountUp(Math.abs(value));
  const isPositive = value >= 0;

  return (
    <motion.div variants={cardVariants} whileHover={{ y: -3, scale: 1.01 }} className="glass-card p-5">
      <div className="flex items-start justify-between">
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center`} style={{ background: color ?? 'rgba(99,102,241,0.15)' }}>
          <Icon size={20} style={{ color: color ? 'white' : 'hsl(var(--primary))' }} />
        </div>
        {isProfit && (
          <span className={isPositive ? 'badge-profit' : 'badge-loss'}>
            {isPositive ? '+' : '-'}{Math.abs(value).toFixed(1)}%
          </span>
        )}
      </div>
      <div className="mt-3">
        <p className="text-xs text-muted-foreground uppercase tracking-wide font-medium">{label}</p>
        <p className={`text-2xl font-black mt-0.5 tabular ${isProfit ? (isPositive ? 'text-profit' : 'text-loss') : 'text-foreground'}`}>
          {isCurrency ? formatCurrency(count) : count.toLocaleString()}
          {suffix && <span className="text-sm font-normal text-muted-foreground ml-1">{suffix}</span>}
        </p>
      </div>
    </motion.div>
  );
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);

  const getGreeting = () => {
    const h = new Date().getHours();
    if (h < 12) return 'Good morning';
    if (h < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const firstName = user?.first_name ?? user?.username ?? 'Trader';
  const today = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [sumRes, analRes, newsRes] = await Promise.all([
          getPortfolioSummary(), getAnalyses(3), getMarketNews(),
        ]);
        setSummary(sumRes.data);
        setAnalyses(analRes.data?.analyses ?? analRes.data ?? []);
        setNews((newsRes.data?.news ?? newsRes.data ?? []).slice(0, 5));
      } catch {
        // Use fallback data silently
        setSummary({ total_portfolios: 0, total_holdings: 0, total_invested: 0, total_current_value: 0, profit_loss: 0, pct_change: 0 });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Mock sector allocation
  const sectorData = [
    { name: 'Technology', value: 35 },
    { name: 'Finance', value: 22 },
    { name: 'Healthcare', value: 18 },
    { name: 'Energy', value: 12 },
    { name: 'Consumer', value: 13 },
  ];

  const sentimentColor = (s?: string) => {
    if (!s) return 'badge-neutral';
    const lower = s.toLowerCase();
    if (lower.includes('bull') || lower === 'positive') return 'badge-profit';
    if (lower.includes('bear') || lower === 'negative') return 'badge-loss';
    return 'badge-neutral';
  };

  const recommendationLabel = (rec: Analysis['recommendation']) => {
    if (!rec) return 'HOLD';
    if (typeof rec === 'string') return rec.toUpperCase();
    return (rec.action ?? 'HOLD').toUpperCase();
  };

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ value: number; payload: { day: string } }> }) => {
    if (active && payload?.length) {
      return (
        <div className="glass-card px-3 py-2 text-xs">
          <p className="text-foreground font-semibold">{formatCurrency(payload[0].value)}</p>
          <p className="text-muted-foreground">{payload[0].payload.day}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Welcome Banner */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="glass-card p-6 mb-6 relative overflow-hidden"
        style={{ background: 'linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(34,211,238,0.06) 100%)' }}
      >
        <div className="absolute inset-0 dot-grid opacity-30 pointer-events-none" style={{ backgroundSize: '24px 24px' }} />
        <div className="relative">
          <h1 className="text-2xl font-black text-foreground">
            {getGreeting()}, <span className="text-gradient">{firstName}</span> 👋
          </h1>
          <p className="text-muted-foreground text-sm mt-1">{today}</p>
        </div>
      </motion.div>

      {/* Stats Row */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6"
      >
        <StatCard
          icon={Briefcase}
          label="Total Portfolios"
          value={summary?.total_portfolios ?? 0}
          color="rgba(99,102,241,0.2)"
        />
        <StatCard
          icon={TrendingUp}
          label="Total Holdings"
          value={summary?.total_holdings ?? 0}
          color="rgba(34,211,238,0.2)"
        />
        <StatCard
          icon={DollarSign}
          label="Total Invested"
          value={summary?.total_invested ?? 0}
          isCurrency
          color="rgba(16,185,129,0.2)"
        />
        <StatCard
          icon={BarChart3}
          label="Profit / Loss"
          value={summary?.profit_loss ?? 0}
          isCurrency
          isProfit
          color={`rgba(${(summary?.profit_loss ?? 0) >= 0 ? '16,185,129' : '244,63,94'},0.2)`}
        />
      </motion.div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        {/* Area Chart */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-5 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-foreground text-sm">Portfolio Performance</h2>
            <span className="text-xs text-muted-foreground">Last 30 days</span>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={areaData} margin={{ top: 5, right: 5, left: -10, bottom: 0 }}>
              <defs>
                <linearGradient id="portfolioGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="day" tick={{ fill: 'hsl(215,20%,55%)', fontSize: 11 }} tickLine={false} axisLine={false} interval={4} />
              <YAxis tick={{ fill: 'hsl(215,20%,55%)', fontSize: 11 }} tickLine={false} axisLine={false} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={2} fill="url(#portfolioGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Pie Chart */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-5">
          <h2 className="font-semibold text-foreground text-sm mb-4">Asset Allocation</h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={sectorData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={2} dataKey="value">
                {sectorData.map((_, i) => (
                  <Cell key={i} fill={SECTOR_COLORS[i % SECTOR_COLORS.length]} />
                ))}
              </Pie>
              <Legend 
                iconType="circle" 
                iconSize={8} 
                wrapperStyle={{ color: 'hsl(215,20%,65%)', fontSize: '11px' }}
              />
              <Tooltip formatter={(v) => [`${v}%`, 'Allocation']} contentStyle={{ background: 'rgba(15,23,42,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: 'white', fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Recent Analyses */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-5">
          <h2 className="font-semibold text-foreground text-sm mb-4">Recent Analysis</h2>
          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => <div key={i} className="skeleton h-16 rounded-xl" />)}
            </div>
          ) : analyses.length === 0 ? (
            <div className="text-center py-8">
              <BarChart3 size={32} className="mx-auto text-muted-foreground mb-2" />
              <p className="text-sm text-muted-foreground">No analyses yet. Try analyzing a stock!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {analyses.map((a, i) => (
                <motion.div key={a.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }} className="flex items-center justify-between p-3 rounded-xl bg-white/[0.03] border border-white/5 hover:bg-white/[0.05] transition-colors">
                  <div>
                    <p className="text-sm font-semibold text-foreground">{a.stock_symbol}</p>
                    <p className="text-xs text-muted-foreground">{a.stock_name ?? 'Stock Analysis'}</p>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <span className={sentimentColor(a.market_sentiment ?? a.sentiment)}>
                      {a.market_sentiment ?? a.sentiment ?? 'Neutral'}
                    </span>
                    <span className="text-xs text-muted-foreground">{recommendationLabel(a.recommendation)}</span>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Market News */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-5">
          <div className="flex items-center gap-2 mb-4">
            <Newspaper size={16} className="text-primary" />
            <h2 className="font-semibold text-foreground text-sm">Market News</h2>
          </div>
          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => <div key={i} className="skeleton h-14 rounded-xl" />)}
            </div>
          ) : news.length === 0 ? (
            <div className="text-center py-8">
              <Newspaper size={32} className="mx-auto text-muted-foreground mb-2" />
              <p className="text-sm text-muted-foreground">No news available</p>
            </div>
          ) : (
            <div className="space-y-3">
              {news.map((n, i) => (
                <motion.div key={i} initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }} className="p-3 rounded-xl bg-white/[0.03] border border-white/5 hover:bg-white/[0.05] transition-colors cursor-pointer group">
                  <p className="text-sm text-foreground line-clamp-2 group-hover:text-primary transition-colors">{n.title}</p>
                  {n.source && <p className="text-xs text-muted-foreground mt-1">{n.source}</p>}
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
