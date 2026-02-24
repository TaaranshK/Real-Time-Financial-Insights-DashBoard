import React, { useEffect, useState } from "react";
import { analysisAPI, portfolioAPI } from "../services/api";

export default function Dashboard() {
  const [portfolios, setPortfolios] = useState([]);
  const [analyses, setAnalyses] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const p = await portfolioAPI.getPortfolios();
        setPortfolios(p.data.portfolios || []);
        const a = await analysisAPI.getAnalyses(5);
        setAnalyses(a.data.analyses || []);
      } catch {
        setError("Failed to load dashboard data");
      }
    };
    load();
  }, []);

  return (
    <section>
      <h1>Dashboard</h1>
      {error ? <div className="error">{error}</div> : null}
      <div className="stats-grid">
        <div className="card">
          <h3>Portfolios</h3>
          <p>{portfolios.length}</p>
        </div>
        <div className="card">
          <h3>Recent Analyses</h3>
          <p>{analyses.length}</p>
        </div>
      </div>
      <div className="card">
        <h3>Recent Analysis</h3>
        {analyses.length === 0 ? <p>No analysis records yet.</p> : null}
        {analyses.map((a) => (
          <div className="row-line" key={a.id}>
            <strong>{a.stock_symbol}</strong>
            <span>{a.recommendation || "HOLD"}</span>
            <span>{a.sentiment || "NEUTRAL"}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
