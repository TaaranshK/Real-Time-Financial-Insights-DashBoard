import React, { useEffect, useState } from "react";
import { FiTrendingUp, FiTrendingDown, FiBriefcase, FiBarChart2 } from "react-icons/fi";
import { analysisAPI, dashboardAPI, portfolioAPI } from "../services/api";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [analyses, setAnalyses] = useState([]);
  const [news, setNews] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    // load everything for the dashboard
    const loadData = async () => {
      try {
        const [sumRes, anaRes, newsRes] = await Promise.all([
          dashboardAPI.getSummary(),
          analysisAPI.getAnalyses(5),
          analysisAPI.getNews(),
        ]);
        setSummary(sumRes.data);
        setAnalyses(anaRes.data.analyses || []);
        setNews(newsRes.data.news || []);
      } catch (err) {
        setError("Failed to load dashboard data");
      }
    };
    loadData();
  }, []);

  // helper to pick badge class
  const badgeClass = (val) => {
    if (!val) return "neutral";
    const lower = val.toLowerCase();
    if (lower === "buy" || lower === "bullish") return "buy";
    if (lower === "sell" || lower === "bearish") return "sell";
    return "hold";
  };

  return (
    <section>
      <h1>Market Overview</h1>
      {error && <div className="error">{error}</div>}

      {/* top stats row */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="label">Total Invested</div>
          <div className="value">${summary?.total_invested?.toLocaleString() || "0.00"}</div>
          <div className={`change ${summary?.pct_change > 0 ? "up" : summary?.pct_change < 0 ? "down" : "flat"}`}>
            {summary?.pct_change > 0 ? "+" : ""}{summary?.pct_change || 0}%
          </div>
        </div>
        <div className="stat-card">
          <div className="label">Current Value</div>
          <div className="value">${summary?.total_current_value?.toLocaleString() || "0.00"}</div>
          <div className={`change ${summary?.profit_loss >= 0 ? "up" : "down"}`}>
            {summary?.profit_loss >= 0 ? <FiTrendingUp /> : <FiTrendingDown />}
            {" "}{summary?.profit_loss >= 0 ? "+" : ""}${summary?.profit_loss?.toFixed(2) || "0.00"}
          </div>
        </div>
        <div className="stat-card">
          <div className="label">Portfolios</div>
          <div className="value">{summary?.total_portfolios || 0}</div>
          <div className="change flat"><FiBriefcase /> Active</div>
        </div>
        <div className="stat-card">
          <div className="label">Holdings</div>
          <div className="value">{summary?.total_holdings || 0}</div>
          <div className="change flat"><FiBarChart2 /> Tracked</div>
        </div>
      </div>

      {/* two column grid: AI insights + news */}
      <div className="dashboard-grid">
        {/* recent AI analysis */}
        <div className="card">
          <h3>AI Market Insights</h3>
          {analyses.length === 0 && <p style={{color: "#64748b"}}>Run a stock analysis to see insights here.</p>}
          {analyses.map((a) => (
            <div className="row-line" key={a.id}>
              <div>
                <strong>{a.stock_symbol}</strong>
                <div style={{fontSize: "0.78rem", color: "#64748b", marginTop: 2}}>
                  {a.summary ? a.summary.slice(0, 80) + "..." : "No summary"}
                </div>
              </div>
              <div style={{display: "flex", gap: 6, alignItems: "center"}}>
                <span className={`badge ${badgeClass(a.market_sentiment)}`}>
                  {a.market_sentiment || "Neutral"}
                </span>
                <span className={`badge ${badgeClass(a.recommendation?.action)}`}>
                  {a.recommendation?.action || "HOLD"}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* market news */}
        <div className="card">
          <h3>Market News</h3>
          {news.length === 0 && <p style={{color: "#64748b"}}>No news available.</p>}
          {news.map((item, idx) => (
            <div className="news-item" key={idx}>
              <div className="news-title">{item.title}</div>
              <div className="news-meta">
                {item.source} &middot; {item.category}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
