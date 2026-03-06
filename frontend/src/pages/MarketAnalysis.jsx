import React, { useState } from "react";
import { FiSearch } from "react-icons/fi";
import { analysisAPI } from "../services/api";

export default function MarketAnalysis() {
  const [symbol, setSymbol] = useState("");
  const [stockName, setStockName] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // pick the right css class for badges
  const badgeClass = (val) => {
    if (!val) return "neutral";
    const lower = val.toLowerCase();
    if (lower === "buy" || lower === "bullish" || lower === "high") return "buy";
    if (lower === "sell" || lower === "bearish" || lower === "low") return "sell";
    return "hold";
  };

  const analyze = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await analysisAPI.analyzeStock({
        stock_symbol: symbol,
        stock_name: stockName || null,
      });
      setResult(res.data.analysis || null);
    } catch {
      setError("Analysis failed. Please try again.");
    }
    setLoading(false);
  };

  const rec = result?.recommendation || {};

  return (
    <section>
      <h1>Market Analysis</h1>
      {error && <div className="error">{error}</div>}

      {/* search form */}
      <form className="card form-grid" onSubmit={analyze} style={{maxWidth: 500}}>
        <h3><FiSearch style={{marginRight: 6}} />Analyze a Stock</h3>
        <input
          placeholder="Stock symbol (e.g. AAPL, TSLA)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          required
        />
        <input
          placeholder="Company name (optional)"
          value={stockName}
          onChange={(e) => setStockName(e.target.value)}
        />
        <button className="button" type="submit" disabled={loading}>
          {loading ? <><span className="spinner"></span> Analyzing...</> : "Run Analysis"}
        </button>
      </form>

      {/* results */}
      {result && (
        <div className="analysis-result" style={{marginTop: 14}}>
          <h3 style={{marginBottom: 12}}>
            Analysis: {result.stock_symbol}
          </h3>

          {/* summary */}
          <div className="summary">{result.summary}</div>

          {/* sentiment + recommendation badges */}
          <div className="rec-row">
            <span className={`badge ${badgeClass(result.market_sentiment)}`}>
              {result.market_sentiment}
            </span>
            <span className={`badge ${badgeClass(rec.action)}`}>
              {rec.action || "HOLD"}
            </span>
            <span className={`badge ${badgeClass(rec.confidence)}`}>
              Confidence: {rec.confidence || "N/A"}
            </span>
          </div>

          {/* reason */}
          {rec.reason && <div className="reason">{rec.reason}</div>}

          {/* related news */}
          {result.news_headlines && result.news_headlines.length > 0 && (
            <div style={{marginTop: 16}}>
              <h3>Related Headlines</h3>
              {result.news_headlines.map((headline, i) => (
                <div className="news-item" key={i}>
                  <div className="news-title">{headline}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!result && !loading && (
        <div className="card" style={{marginTop: 14, color: "#64748b"}}>
          <p>Enter a stock symbol above and click "Run Analysis" to get AI-powered insights.</p>
        </div>
      )}
    </section>
  );
}
