import { useState, useEffect } from 'react';
import { motion, AnimatePresence, Variants } from 'framer-motion';
import {
  Plus, Briefcase, ChevronRight, TrendingUp, TrendingDown,
  X, Loader2, Edit2, Check, Layers
} from 'lucide-react';
import toast from 'react-hot-toast';
import {
  getPortfolios, createPortfolio, getPortfolio, addHolding, updateHoldingPrice
} from '@/lib/api';

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const formatCurrency = (v: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 }).format(v);

const PORTFOLIO_TYPES = ['Equity', 'Mutual Fund', 'Crypto', 'Mixed'];
const SECTORS = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer', 'Real Estate', 'Industrial', 'Other'];

interface Portfolio { id: number; name: string; description?: string; portfolio_type?: string; created_at?: string; holdings?: Holding[]; }
interface Holding {
  id: number; stock_symbol: string; stock_name: string; quantity: number;
  buy_price: number; current_price?: number; sector?: string;
}

function ModalWrapper({ show, onClose, title, children }: {
  show: boolean; onClose: () => void; title: string; children: React.ReactNode;
}) {
  return (
    <AnimatePresence>
      {show && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-50 flex items-center justify-center p-4" style={{ background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)' }} onClick={onClose}>
          <motion.div initial={{ opacity: 0, scale: 0.92, y: 20 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.94, y: 10 }} transition={{ duration: 0.25 }} className="glass-card p-6 w-full max-w-md" onClick={(e) => e.stopPropagation()} style={{ border: '1px solid rgba(255,255,255,0.12)' }}>
            <div className="flex items-center justify-between mb-5">
              <h3 className="font-bold text-foreground">{title}</h3>
              <button onClick={onClose} className="w-8 h-8 rounded-lg flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-white/5 transition-colors"><X size={16} /></button>
            </div>
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function PnLCell({ invested, current }: { invested: number; current: number }) {
  const pnl = current - invested;
  const pct = invested > 0 ? (pnl / invested) * 100 : 0;
  const pos = pnl >= 0;
  return (
    <div className={`flex items-center gap-1 text-xs font-semibold ${pos ? 'text-profit' : 'text-loss'}`}>
      {pos ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
      {formatCurrency(pnl)} ({pos ? '+' : ''}{pct.toFixed(2)}%)
    </div>
  );
}

const Portfolio: React.FC = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [selectedPortfolio, setSelectedPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showHoldingModal, setShowHoldingModal] = useState(false);
  const [editPriceId, setEditPriceId] = useState<number | null>(null);
  const [editPriceValue, setEditPriceValue] = useState('');

  // Create portfolio form
  const [pName, setPName] = useState('');
  const [pDesc, setPDesc] = useState('');
  const [pType, setPType] = useState('Equity');
  const [pLoading, setPLoading] = useState(false);

  // Add holding form
  const [hSymbol, setHSymbol] = useState('');
  const [hName, setHName] = useState('');
  const [hQty, setHQty] = useState('');
  const [hPrice, setHPrice] = useState('');
  const [hSector, setHSector] = useState('Technology');
  const [hLoading, setHLoading] = useState(false);

  const fetchPortfolios = async () => {
    setLoading(true);
    try {
      const res = await getPortfolios();
      setPortfolios(res.data?.portfolios ?? res.data ?? []);
    } catch {
      toast.error('Failed to load portfolios');
    } finally { setLoading(false); }
  };

  const fetchPortfolioDetail = async (id: number) => {
    setDetailLoading(true);
    try {
      const res = await getPortfolio(id);
      setSelectedPortfolio(res.data?.portfolio ?? res.data);
    } catch {
      toast.error('Failed to load portfolio');
    } finally { setDetailLoading(false); }
  };

  useEffect(() => { fetchPortfolios(); }, []);

  const handleCreatePortfolio = async () => {
    if (!pName.trim()) { toast.error('Portfolio name is required'); return; }
    setPLoading(true);
    try {
      await createPortfolio({ name: pName, description: pDesc, portfolio_type: pType });
      toast.success('Portfolio created!');
      setShowCreateModal(false);
      setPName(''); setPDesc(''); setPType('Equity');
      fetchPortfolios();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Failed to create portfolio');
    } finally { setPLoading(false); }
  };

  const handleAddHolding = async () => {
    if (!selectedPortfolio) return;
    if (!hSymbol || !hName || !hQty || !hPrice) { toast.error('Please fill all required fields'); return; }
    setHLoading(true);
    try {
      await addHolding(selectedPortfolio.id, { stock_symbol: hSymbol.toUpperCase(), stock_name: hName, quantity: Number(hQty), buy_price: Number(hPrice), sector: hSector });
      toast.success('Holding added!');
      setShowHoldingModal(false);
      setHSymbol(''); setHName(''); setHQty(''); setHPrice(''); setHSector('Technology');
      fetchPortfolioDetail(selectedPortfolio.id);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Failed to add holding');
    } finally { setHLoading(false); }
  };

  const handleUpdatePrice = async (holdingId: number) => {
    if (!editPriceValue || isNaN(Number(editPriceValue))) { toast.error('Enter a valid price'); return; }
    try {
      await updateHoldingPrice(holdingId, Number(editPriceValue));
      toast.success('Price updated!');
      setEditPriceId(null);
      if (selectedPortfolio) fetchPortfolioDetail(selectedPortfolio.id);
    } catch { toast.error('Failed to update price'); }
  };

  const typeColors: Record<string, string> = {
    Equity: 'rgba(99,102,241,0.15)', 'Mutual Fund': 'rgba(34,211,238,0.15)',
    Crypto: 'rgba(251,191,36,0.15)', Mixed: 'rgba(16,185,129,0.15)',
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-black text-foreground">
            {selectedPortfolio ? (
              <span className="flex items-center gap-2">
                <button onClick={() => setSelectedPortfolio(null)} className="text-muted-foreground hover:text-foreground transition-colors text-lg">My Portfolios</button>
                <ChevronRight size={18} className="text-muted-foreground" />
                <span className="text-gradient">{selectedPortfolio.name}</span>
              </span>
            ) : 'My Portfolios'}
          </h1>
          <p className="text-muted-foreground text-sm mt-1">
            {selectedPortfolio ? `${selectedPortfolio.portfolio_type ?? 'Portfolio'} • ${selectedPortfolio.holdings?.length ?? 0} holdings` : `${portfolios.length} portfolios`}
          </p>
        </div>
        <motion.button whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }} onClick={() => selectedPortfolio ? setShowHoldingModal(true) : setShowCreateModal(true)} className="btn-gradient px-4 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-2">
          <Plus size={16} />
          {selectedPortfolio ? 'Add Holding' : 'Create Portfolio'}
        </motion.button>
      </motion.div>

      {/* Portfolio Grid */}
      {!selectedPortfolio && (
        loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map(i => <div key={i} className="skeleton h-44 rounded-2xl" />)}
          </div>
        ) : portfolios.length === 0 ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card p-16 text-center">
            <Briefcase size={48} className="mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold text-foreground mb-2">No portfolios yet</h3>
            <p className="text-muted-foreground text-sm mb-4">Create your first portfolio to start tracking investments</p>
            <button onClick={() => setShowCreateModal(true)} className="btn-gradient px-5 py-2.5 rounded-xl text-sm font-semibold">Create Portfolio</button>
          </motion.div>
        ) : (
          <motion.div variants={{ show: { transition: { staggerChildren: 0.1 } } }} initial="hidden" animate="show" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {portfolios.map((p) => {
              const holdings = p.holdings ?? [];
              const invested = holdings.reduce((s, h) => s + h.quantity * h.buy_price, 0);
              const current = holdings.reduce((s, h) => s + h.quantity * (h.current_price ?? h.buy_price), 0);
              const pnl = current - invested;
              const pos = pnl >= 0;
              return (
                <motion.div key={p.id} variants={cardVariants} whileHover={{ y: -4, scale: 1.01 }} className="glass-card p-5 cursor-pointer" onClick={() => fetchPortfolioDetail(p.id)}>
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: typeColors[p.portfolio_type ?? 'Equity'] ?? typeColors.Equity }}>
                      <Layers size={18} className="text-primary" />
                    </div>
                    <span className="text-xs px-2.5 py-1 rounded-full font-medium" style={{ background: typeColors[p.portfolio_type ?? 'Equity'] ?? typeColors.Equity, color: 'hsl(var(--foreground))' }}>
                      {p.portfolio_type ?? 'Equity'}
                    </span>
                  </div>
                  <h3 className="font-bold text-foreground">{p.name}</h3>
                  {p.description && <p className="text-xs text-muted-foreground mt-0.5 line-clamp-1">{p.description}</p>}
                  <div className="mt-4 pt-4 border-t border-white/5">
                    <div className="flex justify-between text-xs text-muted-foreground mb-2">
                      <span>{holdings.length} holdings</span>
                      <span>{invested > 0 ? formatCurrency(invested) : '—'}</span>
                    </div>
                    {pnl !== 0 && <span className={pos ? 'badge-profit' : 'badge-loss'}>{pos ? '+' : ''}{formatCurrency(pnl)}</span>}
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        )
      )}

      {/* Portfolio Detail */}
      {selectedPortfolio && (
        detailLoading ? (
          <div className="space-y-3">
            {[1, 2, 3, 4].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}
          </div>
        ) : (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card overflow-hidden">
            {!selectedPortfolio.holdings || selectedPortfolio.holdings.length === 0 ? (
              <div className="p-12 text-center">
                <TrendingUp size={40} className="mx-auto text-muted-foreground mb-3" />
                <p className="text-foreground font-semibold">No holdings yet</p>
                <p className="text-muted-foreground text-sm mt-1">Add your first holding to this portfolio</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-white/5">
                      {['Symbol', 'Name', 'Qty', 'Buy Price', 'Current', 'Invested', 'Value', 'P&L', 'Actions'].map(h => (
                        <th key={h} className="text-left px-4 py-3 text-xs font-medium text-muted-foreground uppercase tracking-wide">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {selectedPortfolio.holdings.map((h, i) => {
                      const invested = h.quantity * h.buy_price;
                      const current = h.quantity * (h.current_price ?? h.buy_price);
                      return (
                        <motion.tr key={h.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }} className="border-b border-white/[0.04] hover:bg-white/[0.03] transition-colors">
                          <td className="px-4 py-3 font-bold text-primary">{h.stock_symbol}</td>
                          <td className="px-4 py-3 text-foreground">{h.stock_name}</td>
                          <td className="px-4 py-3 tabular text-muted-foreground">{h.quantity}</td>
                          <td className="px-4 py-3 tabular text-muted-foreground">{formatCurrency(h.buy_price)}</td>
                          <td className="px-4 py-3 tabular">
                            {editPriceId === h.id ? (
                              <div className="flex items-center gap-1">
                                <input type="number" value={editPriceValue} onChange={(e) => setEditPriceValue(e.target.value)} className="fin-input w-24 text-xs py-1.5 px-2" placeholder="0.00" />
                                <button onClick={() => handleUpdatePrice(h.id)} className="w-6 h-6 rounded-md flex items-center justify-center bg-profit/20 text-profit hover:bg-profit/30 transition-colors"><Check size={12} /></button>
                                <button onClick={() => setEditPriceId(null)} className="w-6 h-6 rounded-md flex items-center justify-center bg-white/5 text-muted-foreground hover:bg-white/10 transition-colors"><X size={12} /></button>
                              </div>
                            ) : (
                              <span className="text-foreground tabular">{formatCurrency(h.current_price ?? h.buy_price)}</span>
                            )}
                          </td>
                          <td className="px-4 py-3 tabular text-muted-foreground">{formatCurrency(invested)}</td>
                          <td className="px-4 py-3 tabular text-foreground">{formatCurrency(current)}</td>
                          <td className="px-4 py-3"><PnLCell invested={invested} current={current} /></td>
                          <td className="px-4 py-3">
                            <button onClick={() => { setEditPriceId(h.id); setEditPriceValue(String(h.current_price ?? h.buy_price)); }} className="flex items-center gap-1 text-xs text-muted-foreground hover:text-primary transition-colors px-2 py-1 rounded-lg hover:bg-white/5">
                              <Edit2 size={12} /> Update
                            </button>
                          </td>
                        </motion.tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </motion.div>
        )
      )}

      {/* Create Portfolio Modal */}
      <ModalWrapper show={showCreateModal} onClose={() => setShowCreateModal(false)} title="Create Portfolio">
        <div className="space-y-4">
          {[{ label: 'Portfolio Name *', value: pName, set: setPName, placeholder: 'My Growth Portfolio' }, { label: 'Description', value: pDesc, set: setPDesc, placeholder: 'Optional description...' }].map(({ label, value, set, placeholder }) => (
            <div key={label}>
              <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
              <input value={value} onChange={(e) => set(e.target.value)} placeholder={placeholder} className="fin-input" />
            </div>
          ))}
          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Type</label>
            <select value={pType} onChange={(e) => setPType(e.target.value)} className="fin-input">
              {PORTFOLIO_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <button onClick={handleCreatePortfolio} disabled={pLoading} className="btn-gradient w-full py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2">
            {pLoading ? <><Loader2 size={15} className="animate-spin" /> Creating...</> : 'Create Portfolio'}
          </button>
        </div>
      </ModalWrapper>

      {/* Add Holding Modal */}
      <ModalWrapper show={showHoldingModal} onClose={() => setShowHoldingModal(false)} title="Add Holding">
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            {[{ label: 'Symbol *', value: hSymbol, set: setHSymbol, placeholder: 'AAPL' }, { label: 'Quantity *', value: hQty, set: setHQty, placeholder: '10', type: 'number' }].map(({ label, value, set, placeholder, type }) => (
              <div key={label}>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                <input type={type ?? 'text'} value={value} onChange={(e) => set(e.target.value)} placeholder={placeholder} className="fin-input text-sm" />
              </div>
            ))}
          </div>
          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Stock Name *</label>
            <input value={hName} onChange={(e) => setHName(e.target.value)} placeholder="Apple Inc." className="fin-input" />
          </div>
          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Buy Price *</label>
            <input type="number" value={hPrice} onChange={(e) => setHPrice(e.target.value)} placeholder="150.00" className="fin-input" />
          </div>
          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Sector</label>
            <select value={hSector} onChange={(e) => setHSector(e.target.value)} className="fin-input">
              {SECTORS.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <button onClick={handleAddHolding} disabled={hLoading} className="btn-gradient w-full py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2">
            {hLoading ? <><Loader2 size={15} className="animate-spin" /> Adding...</> : 'Add Holding'}
          </button>
        </div>
      </ModalWrapper>
    </div>
  );
};

export default Portfolio;
