import React, { useState } from "react";
import { analysisAPI } from "../services/api";

export default function MarketAnalysis() {
  const [symbol, setSymbol] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const analyze = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await analysisAPI.analyzeStock({ stock_symbol: symbol });
      setResult(response.data.analysis || null);
    } catch {
      setError("Analysis failed");
    }
  };

  return (
    <section>
      <h1>Market Analysis</h1>
      {error ? <div className="error">{error}</div> : null}
      <form className="card form-grid" onSubmit={analyze}>
        <h3>Analyze Stock</h3>
        <input
          placeholder="Enter symbol (AAPL)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          required
        />
        <button className="button" type="submit">
          Analyze
        </button>
      </form>
      <div className="card">
        <h3>Result</h3>
        {!result ? <p>No analysis yet.</p> : null}
        {result ? (
          <div className="row-line">
            <strong>{result.stock_symbol}</strong>
            <span>{result.recommendation}</span>
            <span>{result.sentiment}</span>
          </div>
        ) : null}
      </div>
    </section>
  );
}
