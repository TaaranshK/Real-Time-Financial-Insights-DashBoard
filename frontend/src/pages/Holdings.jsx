import React, { useEffect, useState } from "react";
import { holdingAPI, portfolioAPI } from "../services/api";

export default function Holdings() {
  const [portfolios, setPortfolios] = useState([]);
  const [portfolioId, setPortfolioId] = useState("");
  const [holdings, setHoldings] = useState([]);
  const [form, setForm] = useState({ stock_symbol: "", stock_name: "", quantity: "", buy_price: "" });
  const [priceUpdate, setPriceUpdate] = useState({ holdingId: "", newPrice: "" });
  const [error, setError] = useState("");

  useEffect(() => {
    const loadPortfolios = async () => {
      try {
        const res = await portfolioAPI.getPortfolios();
        const list = res.data.portfolios || [];
        setPortfolios(list);
        if (list[0]) setPortfolioId(String(list[0].id));
      } catch {
        setError("Failed to load portfolios");
      }
    };
    loadPortfolios();
  }, []);

  useEffect(() => {
    const loadHoldings = async () => {
      if (!portfolioId) return;
      try {
        const res = await portfolioAPI.getHoldings(portfolioId);
        setHoldings(res.data.holdings || []);
      } catch {
        setError("Failed to load holdings");
      }
    };
    loadHoldings();
  }, [portfolioId]);

  const addHolding = async (e) => {
    e.preventDefault();
    try {
      await portfolioAPI.addHolding(portfolioId, {
        ...form,
        quantity: Number(form.quantity),
        buy_price: Number(form.buy_price),
      });
      setForm({ stock_symbol: "", stock_name: "", quantity: "", buy_price: "" });
      const res = await portfolioAPI.getHoldings(portfolioId);
      setHoldings(res.data.holdings || []);
    } catch {
      setError("Failed to add holding");
    }
  };

  const updatePrice = async (e) => {
    e.preventDefault();
    try {
      await holdingAPI.updatePrice(Number(priceUpdate.holdingId), Number(priceUpdate.newPrice));
      const res = await portfolioAPI.getHoldings(portfolioId);
      setHoldings(res.data.holdings || []);
      setPriceUpdate({ holdingId: "", newPrice: "" });
    } catch {
      setError("Failed to update price");
    }
  };

  return (
    <section>
      <h1>Holdings</h1>
      {error ? <div className="error">{error}</div> : null}
      <div className="card form-grid">
        <h3>Select Portfolio</h3>
        <select value={portfolioId} onChange={(e) => setPortfolioId(e.target.value)}>
          <option value="">Select...</option>
          {portfolios.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
      </div>
      <form className="card form-grid" onSubmit={addHolding}>
        <h3>Add Holding</h3>
        <input
          placeholder="Symbol (AAPL)"
          value={form.stock_symbol}
          onChange={(e) => setForm((s) => ({ ...s, stock_symbol: e.target.value }))}
          required
        />
        <input
          placeholder="Stock name"
          value={form.stock_name}
          onChange={(e) => setForm((s) => ({ ...s, stock_name: e.target.value }))}
          required
        />
        <input
          placeholder="Quantity"
          type="number"
          value={form.quantity}
          onChange={(e) => setForm((s) => ({ ...s, quantity: e.target.value }))}
          required
        />
        <input
          placeholder="Buy price"
          type="number"
          value={form.buy_price}
          onChange={(e) => setForm((s) => ({ ...s, buy_price: e.target.value }))}
          required
        />
        <button className="button" type="submit">
          Add
        </button>
      </form>
      <form className="card form-grid" onSubmit={updatePrice}>
        <h3>Update Price</h3>
        <input
          placeholder="Holding ID"
          value={priceUpdate.holdingId}
          onChange={(e) => setPriceUpdate((s) => ({ ...s, holdingId: e.target.value }))}
          required
        />
        <input
          placeholder="New price"
          type="number"
          value={priceUpdate.newPrice}
          onChange={(e) => setPriceUpdate((s) => ({ ...s, newPrice: e.target.value }))}
          required
        />
        <button className="button" type="submit">
          Update
        </button>
      </form>
      <div className="card">
        <h3>Current Holdings</h3>
        {holdings.length === 0 ? <p>No holdings yet.</p> : null}
        {holdings.map((h) => (
          <div key={h.id} className="row-line">
            <strong>
              {h.stock_symbol} ({h.stock_name})
            </strong>
            <span>Qty: {h.quantity}</span>
            <span>Price: {h.current_price}</span>
            <span>ID: {h.id}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
