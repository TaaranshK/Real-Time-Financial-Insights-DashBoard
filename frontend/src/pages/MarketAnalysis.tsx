import { useState, useEffect } from 'react';
import { motion, AnimatePresence, Variants } from 'framer-motion';
import {
  Search, Zap, Loader2, TrendingUp, TrendingDown, Minus,
  ChevronDown, ChevronUp, BarChart2, Newspaper
} from 'lucide-react';
import toast from 'react-hot-toast';
import { analyzeStock, getAnalyses } from '@/lib/api';

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const SECTORS = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer', 'Real Estate', 'Industrial', 'Other'];

interface AnalysisResult {
  stock_symbol: string;
  stock_name?: string;
  summary?: string;
  sentiment?: string;
  market_sentiment?: string;
  recommendation?: {
    action?: string;
    confidence?: number | string;
    reason?: string;
  };
  news_headlines?: string[];
  created_at?: string;
  id?: number;
}

function SentimentBadge({ sentiment }: { sentiment?: string }) {
  const lower = (sentiment ?? '').toLowerCase();
  if (lower.includes('bull') || lower === 'positive') {
    return <span className="badge-profit flex items-center gap-1"><TrendingUp size={12} /> {sentiment}</span>;
  }
  if (lower.includes('bear') || lower === 'negative') {
    return <span className="badge-loss flex items-center gap-1"><TrendingDown size={12} /> {sentiment}</span>;
  }
  return <span className="badge-neutral flex items-center gap-1"><Minus size={12} /> {sentiment ?? 'Neutral'}</span>;
}

function ActionBadge({ action }: { action?: string }) {
  const a = (action ?? '').toUpperCase();
  if (a === 'BUY') return <span className="badge-profit text-sm font-bold px-4 py-1.5">{a}</span>;
  if (a === 'SELL') return <span className="badge-loss text-sm font-bold px-4 py-1.5">{a}</span>;
  return <span className="badge-neutral text-sm font-bold px-4 py-1.5">{a || 'HOLD'}</span>;
}

const MarketAnalysis: React.FC = () => {
  const [symbol, setSymbol] = useState('');
  const [stockName, setStockName] = useState('');
  const [price, setPrice] = useState('');
  const [sector, setSector] = useState('Technology');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [history, setHistory] = useState<AnalysisResult[]>([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const normalizeAnalysis = (raw: unknown): AnalysisResult => {
    const item = (raw ?? {}) as Record<string, unknown>;
    const recRaw = (item.recommendation ?? {}) as Record<string, unknown>;
    const recommendation = typeof item.recommendation === 'object' && item.recommendation !== null
      ? {
          action: typeof recRaw.action === 'string' ? recRaw.action : undefined,
          confidence: typeof recRaw.confidence === 'number' || typeof recRaw.confidence === 'string' ? recRaw.confidence : undefined,
          reason: typeof recRaw.reason === 'string' ? recRaw.reason : undefined,
        }
      : undefined;

    return {
      id: typeof item.id === 'number' ? item.id : undefined,
      stock_symbol: String(item.stock_symbol ?? ''),
      stock_name: typeof item.stock_name === 'string' ? item.stock_name : undefined,
      summary: typeof item.summary === 'string' ? item.summary : undefined,
      sentiment: typeof item.sentiment === 'string' ? item.sentiment : undefined,
      market_sentiment: typeof item.market_sentiment === 'string' ? item.market_sentiment : undefined,
      recommendation,
      news_headlines: Array.isArray(item.news_headlines) ? item.news_headlines.map(String) : undefined,
      created_at: typeof item.created_at === 'string' ? item.created_at : undefined,
    };
  };

  useEffect(() => {
    const fetchHistory = async () => {
      setHistoryLoading(true);
      try {
        const res = await getAnalyses(10);
        const list = (res.data?.analyses ?? res.data ?? []) as unknown[];
        setHistory(Array.isArray(list) ? list.map(normalizeAnalysis) : []);
      } catch { /* silent */ }
      finally { setHistoryLoading(false); }
    };
    fetchHistory();
  }, []);

  const handleAnalyze = async () => {
    if (!symbol.trim()) { toast.error('Please enter a stock symbol'); return; }
    setLoading(true);
    setResult(null);
    try {
      const res = await analyzeStock({
        stock_symbol: symbol.toUpperCase().trim(),
        stock_name: stockName || undefined,
        current_price: price ? Number(price) : undefined,
        sector: sector || undefined,
      });
      setResult(normalizeAnalysis(res.data?.analysis ?? res.data));
      toast.success('Analysis complete!');
      // refresh history
      const histRes = await getAnalyses(10);
      const list = (histRes.data?.analyses ?? histRes.data ?? []) as unknown[];
      setHistory(Array.isArray(list) ? list.map(normalizeAnalysis) : []);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Analysis failed. Please try again.');
    } finally { setLoading(false); }
  };

  const confidenceRaw = result?.recommendation?.confidence;
  const confidence = typeof confidenceRaw === 'number'
    ? confidenceRaw
    : confidenceRaw === 'High'
      ? 85
      : confidenceRaw === 'Medium'
        ? 60
        : confidenceRaw === 'Low'
          ? 35
          : 0;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-2xl font-black text-foreground mb-6">
        Market Analysis
      </motion.h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Form */}
        <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-primary/15 flex items-center justify-center">
              <BarChart2 size={20} className="text-primary" />
            </div>
            <div>
              <h2 className="font-bold text-foreground">AI Stock Analyzer</h2>
              <p className="text-xs text-muted-foreground">Powered by market intelligence</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Stock Symbol *</label>
              <div className="relative">
                <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                <input
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                  placeholder="AAPL, TSLA, MSFT..."
                  className="fin-input pl-10 font-mono tracking-wider"
                  onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Stock Name</label>
              <input value={stockName} onChange={(e) => setStockName(e.target.value)} placeholder="Apple Inc." className="fin-input" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Current Price</label>
                <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} placeholder="150.00" className="fin-input" />
              </div>
              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Sector</label>
                <select value={sector} onChange={(e) => setSector(e.target.value)} className="fin-input">
                  {SECTORS.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.97 }}
              onClick={handleAnalyze}
              disabled={loading}
              className={`btn-gradient w-full py-3.5 rounded-xl text-sm font-bold flex items-center justify-center gap-2 ${!loading ? 'btn-pulse' : ''}`}
            >
              {loading ? (
                <><Loader2 size={16} className="animate-spin" /> Analyzing with AI...</>
              ) : (
                <><Zap size={16} fill="white" /> Analyze with AI</>
              )}
            </motion.button>
          </div>

          {/* Loading skeleton */}
          {loading && (
            <div className="mt-6 space-y-3">
              <div className="skeleton h-5 rounded-lg w-3/4" />
              <div className="skeleton h-4 rounded-lg w-full" />
              <div className="skeleton h-4 rounded-lg w-5/6" />
              <div className="skeleton h-20 rounded-xl" />
            </div>
          )}
        </motion.div>

        {/* Right: Result */}
        <div>
          <AnimatePresence mode="wait">
            {result && !loading ? (
              <motion.div
                key="result"
                initial={{ opacity: 0, y: 30, scale: 0.97 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.4 }}
                className="glass-card p-6 space-y-5"
              >
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-2xl font-black text-gradient">{result.stock_symbol}</h3>
                    {result.stock_name && <p className="text-muted-foreground text-sm">{result.stock_name}</p>}
                  </div>
                  <SentimentBadge sentiment={result.market_sentiment ?? result.sentiment} />
                </div>

                {/* Summary */}
                {result.summary && (
                  <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5">
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">AI Summary</p>
                    <p className="text-sm text-foreground leading-relaxed">{result.summary}</p>
                  </div>
                )}

                {/* Recommendation */}
                {result.recommendation && (
                  <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5 space-y-3">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Recommendation</p>
                      <ActionBadge action={result.recommendation.action} />
                    </div>
                    {confidence > 0 && (
                      <div>
                        <div className="flex justify-between text-xs text-muted-foreground mb-1">
                          <span>Confidence</span>
                          <span>{confidence}%</span>
                        </div>
                        <div className="h-2 rounded-full bg-white/10 overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${confidence}%` }}
                            transition={{ duration: 0.8, delay: 0.3 }}
                            className="h-full rounded-full bg-gradient-primary"
                          />
                        </div>
                      </div>
                    )}
                    {result.recommendation.reason && (
                      <p className="text-sm text-muted-foreground">{result.recommendation.reason}</p>
                    )}
                  </div>
                )}

                {/* News headlines used */}
                {result.news_headlines && result.news_headlines.length > 0 && (
                  <div>
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2 flex items-center gap-1.5"><Newspaper size={12} /> News Used in Analysis</p>
                    <div className="space-y-2">
                      {result.news_headlines.slice(0, 3).map((headline, i) => (
                        <div key={i} className="text-xs text-muted-foreground bg-white/[0.03] border border-white/5 rounded-lg px-3 py-2">
                          {headline}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ) : !loading && (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="glass-card p-12 text-center h-full flex flex-col items-center justify-center"
              >
                <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-4">
                  <Zap size={32} className="text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">AI-Powered Analysis</h3>
                <p className="text-sm text-muted-foreground max-w-xs">Enter a stock symbol and click analyze to get AI-powered sentiment analysis and recommendations</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Analysis History */}
      <motion.div variants={cardVariants} initial="hidden" animate="show" className="glass-card p-5 mt-6">
        <h2 className="font-semibold text-foreground text-sm mb-4">Analysis History</h2>
        {historyLoading ? (
          <div className="space-y-2">{[1,2,3].map(i => <div key={i} className="skeleton h-14 rounded-xl" />)}</div>
        ) : history.length === 0 ? (
          <p className="text-sm text-muted-foreground text-center py-6">No past analyses yet</p>
        ) : (
          <div className="space-y-2">
            {history.map((a, i) => (
              <motion.div key={a.id ?? i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.04 }} className="rounded-xl border border-white/5 overflow-hidden">
                <button
                  onClick={() => setExpandedId(expandedId === (a.id ?? i) ? null : (a.id ?? i))}
                  className="w-full flex items-center justify-between p-4 hover:bg-white/[0.03] transition-colors text-left"
                >
                  <div className="flex items-center gap-3">
                    <span className="font-bold text-primary">{a.stock_symbol}</span>
                    {a.stock_name && <span className="text-sm text-muted-foreground">{a.stock_name}</span>}
                    <SentimentBadge sentiment={a.market_sentiment ?? a.sentiment} />
                  </div>
                  <div className="flex items-center gap-3">
                    <ActionBadge action={a.recommendation?.action} />
                    {expandedId === (a.id ?? i) ? <ChevronUp size={15} className="text-muted-foreground" /> : <ChevronDown size={15} className="text-muted-foreground" />}
                  </div>
                </button>
                <AnimatePresence>
                  {expandedId === (a.id ?? i) && (
                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.25 }} className="overflow-hidden">
                      <div className="px-4 pb-4 border-t border-white/5 pt-3 space-y-2">
                        {a.summary && <p className="text-sm text-muted-foreground">{a.summary}</p>}
                        {a.recommendation?.reason && <p className="text-xs text-muted-foreground bg-white/[0.03] rounded-lg p-2">{a.recommendation.reason}</p>}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default MarketAnalysis;
