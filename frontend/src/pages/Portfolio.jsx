import React, { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";
import { portfolioAPI } from "../services/api";

export default function Portfolio() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const res = await portfolioAPI.getPortfolios();
      setItems(res.data.portfolios || []);
    } catch {
      setError("Failed to load portfolios");
    }
  };

  useEffect(() => { load(); }, []);

  const createPortfolio = async (e) => {
    e.preventDefault();
    try {
      await portfolioAPI.createPortfolio({ name, description, portfolio_type: "Equity" });
      setName("");
      setDescription("");
      await load();
    } catch {
      setError("Portfolio creation failed");
    }
  };

  return (
    <section>
      <h1>Portfolio</h1>
      {error && <div className="error">{error}</div>}
      <form className="card form-grid" onSubmit={createPortfolio} style={{maxWidth: 450}}>
        <h3><FiPlus style={{marginRight: 6}} />Create Portfolio</h3>
        <input placeholder="Portfolio name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input placeholder="Description (optional)" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button className="button" type="submit">Create</button>
      </form>
      <div className="card">
        <h3>Your Portfolios</h3>
        {items.length === 0 && <p style={{color: "#64748b"}}>No portfolios yet. Create one above.</p>}
        {items.map((item) => (
          <div className="row-line" key={item.id}>
            <div>
              <strong>{item.name}</strong>
              {item.description && <div style={{fontSize: "0.8rem", color: "#64748b"}}>{item.description}</div>}
            </div>
            <span className="badge hold">{item.portfolio_type}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
