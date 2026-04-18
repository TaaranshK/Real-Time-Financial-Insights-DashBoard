import { useState, useEffect } from 'react';
import { motion, Variants } from 'framer-motion';
import { TrendingUp, TrendingDown, Search, BarChart3 } from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { getPortfolios, getHoldings } from '@/lib/api';
import toast from 'react-hot-toast';

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const formatCurrency = (v: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 }).format(v);

const SECTOR_COLORS = ['#6366f1', '#22d3ee', '#10b981', '#f59e0b', '#f43f5e', '#a855f7', '#3b82f6'];

interface Portfolio { id: number; name: string; description?: string; }

interface Holding {
  id: number; stock_symbol: string; stock_name: string; quantity: number;
  buy_price: number; current_price?: number; sector?: string; portfolio_name?: string;
  invested?: number; current?: number; pnl?: number; pct?: number;
}

const Holdings: React.FC = () => {
  const [allHoldings, setAllHoldings] = useState<Holding[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<string>('pnl');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    const fetchAll = async () => {
      setLoading(true);
      try {
        const portfoliosRes = await getPortfolios();
        const portfolios = portfoliosRes.data?.portfolios ?? portfoliosRes.data ?? [];
        const all: Holding[] = [];
        await Promise.all(
          portfolios.map(async (p: Portfolio) => {
            try {
              const holdRes = await getHoldings(p.id);
              const holdings = holdRes.data?.holdings ?? holdRes.data ?? [];
              holdings.forEach((h: Holding) => all.push({ ...h, portfolio_name: p.name }));
            } catch { /* skip */ }
          })
        );
        setAllHoldings(all);
      } catch {
        toast.error('Failed to load holdings');
      } finally { setLoading(false); }
    };
    fetchAll();
  }, []);

  const enriched = allHoldings.map(h => {
    const cp = h.current_price ?? h.buy_price;
    const invested = h.quantity * h.buy_price;
    const current = h.quantity * cp;
    const pnl = current - invested;
    const pct = invested > 0 ? (pnl / invested) * 100 : 0;
    return { ...h, invested, current, pnl, pct };
  });

  const filtered = enriched.filter(h =>
    h.stock_symbol.toLowerCase().includes(search.toLowerCase()) ||
    h.stock_name.toLowerCase().includes(search.toLowerCase()) ||
    (h.sector ?? '').toLowerCase().includes(search.toLowerCase())
  );

  const sorted = [...filtered].sort((a, b) => {
    const aVal = (a[sortKey as keyof Holding] as number) ?? 0;
    const bVal = (b[sortKey as keyof Holding] as number) ?? 0;
    return sortDir === 'desc' ? bVal - aVal : aVal - bVal;
  });

  const totalInvested = enriched.reduce((s, h) => s + h.invested, 0);
  const totalCurrent = enriched.reduce((s, h) => s + h.current, 0);
  const totalPnl = totalCurrent - totalInvested;
  const totalPct = totalInvested > 0 ? (totalPnl / totalInvested) * 100 : 0;

  const topGainers = [...enriched].sort((a, b) => b.pct - a.pct).slice(0, 3);
  const topLosers = [...enriched].sort((a, b) => a.pct - b.pct).slice(0, 3).filter(h => h.pct < 0);

  // Sector distribution
  const sectorMap: Record<string, number> = {};
  enriched.forEach(h => {
    const s = h.sector ?? 'Other';
    sectorMap[s] = (sectorMap[s] ?? 0) + h.current;
  });
  const sectorData = Object.entries(sectorMap).map(([name, value]) => ({ name, value: Math.round(value) }));

  const handleSort = (key: string) => {
    if (sortKey === key) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortKey(key); setSortDir('desc'); }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-2xl font-black text-foreground mb-6">
        All Holdings
      </motion.h1>

      {/* Summary Bar */}
      <motion.div variants={{ show: { transition: { staggerChildren: 0.08 } } }} initial="hidden" animate="show" className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: 'Total Invested', value: formatCurrency(totalInvested), color: 'text-foreground' },
          { label: 'Current Value', value: formatCurrency(totalCurrent), color: 'text-foreground' },
          { label: 'Overall P&L', value: `${totalPnl >= 0 ? '+' : ''}${formatCurrency(totalPnl)} (${totalPct.toFixed(2)}%)`, color: totalPnl >= 0 ? 'text-profit' : 'text-loss' },
        ].map(({ label, value, color }) => (
          <motion.div key={label} variants={cardVariants} className="glass-card p-4 text-center">
            <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">{label}</p>
            <p className={`text-xl font-black tabular ${color}`}>{value}</p>
          </motion.div>
        ))}
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        {/* Top Gainers */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-4">
          <h3 className="text-sm font-semibold text-profit mb-3 flex items-center gap-2"><TrendingUp size={14} /> Top Gainers</h3>
          {topGainers.length === 0 ? <p className="text-xs text-muted-foreground">No data</p> : topGainers.map(h => (
            <div key={h.id} className="flex items-center justify-between py-2 border-b border-white/[0.04] last:border-0">
              <div>
                <p className="text-sm font-bold text-foreground">{h.stock_symbol}</p>
                <p className="text-xs text-muted-foreground">{h.sector ?? 'N/A'}</p>
              </div>
              <span className="badge-profit">+{h.pct.toFixed(2)}%</span>
            </div>
          ))}
        </motion.div>

        {/* Top Losers */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-4">
          <h3 className="text-sm font-semibold text-loss mb-3 flex items-center gap-2"><TrendingDown size={14} /> Top Losers</h3>
          {topLosers.length === 0 ? <p className="text-xs text-muted-foreground">No losses</p> : topLosers.map(h => (
            <div key={h.id} className="flex items-center justify-between py-2 border-b border-white/[0.04] last:border-0">
              <div>
                <p className="text-sm font-bold text-foreground">{h.stock_symbol}</p>
                <p className="text-xs text-muted-foreground">{h.sector ?? 'N/A'}</p>
              </div>
              <span className="badge-loss">{h.pct.toFixed(2)}%</span>
            </div>
          ))}
        </motion.div>

        {/* Sector Donut */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-4">
          <h3 className="text-sm font-semibold text-foreground mb-2 flex items-center gap-2"><BarChart3 size={14} /> Sector Distribution</h3>
          {sectorData.length === 0 ? (
            <div className="h-32 flex items-center justify-center text-xs text-muted-foreground">No data</div>
          ) : (
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie data={sectorData} cx="50%" cy="50%" innerRadius={40} outerRadius={65} paddingAngle={2} dataKey="value">
                  {sectorData.map((_, i) => <Cell key={i} fill={SECTOR_COLORS[i % SECTOR_COLORS.length]} />)}
                </Pie>
                <Tooltip formatter={(v) => [formatCurrency(v as number), 'Value']} contentStyle={{ background: 'rgba(15,23,42,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: 'white', fontSize: 11 }} />
                <Legend iconType="circle" iconSize={7} formatter={(v) => <span style={{ color: 'hsl(215,20%,65%)', fontSize: 10 }}>{v}</span>} />
              </PieChart>
            </ResponsiveContainer>
          )}
        </motion.div>
      </div>

      {/* Search + Table */}
      <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card overflow-hidden">
        <div className="p-4 border-b border-white/5">
          <div className="relative max-w-sm">
            <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by symbol, name or sector..." className="fin-input pl-9 text-sm" />
          </div>
        </div>
        {loading ? (
          <div className="p-6 space-y-3">{[1,2,3,4].map(i => <div key={i} className="skeleton h-14 rounded-xl" />)}</div>
        ) : sorted.length === 0 ? (
          <div className="p-12 text-center">
            <TrendingUp size={40} className="mx-auto text-muted-foreground mb-3" />
            <p className="text-foreground font-semibold">No holdings found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/5">
                  {[
                    { key: 'stock_symbol', label: 'Symbol' },
                    { key: 'stock_name', label: 'Name' },
                    { key: 'sector', label: 'Sector' },
                    { key: 'quantity', label: 'Qty' },
                    { key: 'buy_price', label: 'Buy Price' },
                    { key: 'current', label: 'Value' },
                    { key: 'pnl', label: 'P&L' },
                    { key: 'pct', label: 'P&L%' },
                    { key: 'portfolio_name', label: 'Portfolio' },
                  ].map(({ key, label }) => (
                    <th key={key} onClick={() => handleSort(key)} className="text-left px-4 py-3 text-xs font-medium text-muted-foreground uppercase tracking-wide cursor-pointer hover:text-foreground transition-colors select-none">
                      {label} {sortKey === key ? (sortDir === 'desc' ? '↓' : '↑') : ''}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sorted.map((h, i) => (
                  <motion.tr key={h.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.03 }} className="border-b border-white/[0.04] hover:bg-white/[0.03] transition-colors">
                    <td className="px-4 py-3 font-bold text-primary">{h.stock_symbol}</td>
                    <td className="px-4 py-3 text-foreground">{h.stock_name}</td>
                    <td className="px-4 py-3"><span className="text-xs text-muted-foreground bg-white/[0.05] px-2 py-0.5 rounded-full">{h.sector ?? 'N/A'}</span></td>
                    <td className="px-4 py-3 tabular text-muted-foreground">{h.quantity}</td>
                    <td className="px-4 py-3 tabular text-muted-foreground">{formatCurrency(h.buy_price)}</td>
                    <td className="px-4 py-3 tabular text-foreground font-medium">{formatCurrency(h.current)}</td>
                    <td className={`px-4 py-3 tabular font-semibold ${h.pnl >= 0 ? 'text-profit' : 'text-loss'}`}>{h.pnl >= 0 ? '+' : ''}{formatCurrency(h.pnl)}</td>
                    <td className="px-4 py-3"><span className={h.pct >= 0 ? 'badge-profit' : 'badge-loss'}>{h.pct >= 0 ? '+' : ''}{h.pct.toFixed(2)}%</span></td>
                    <td className="px-4 py-3 text-xs text-muted-foreground">{h.portfolio_name}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Holdings;
