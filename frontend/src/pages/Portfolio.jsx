import React, { useEffect, useState } from "react";
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

  useEffect(() => {
    load();
  }, []);

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
      {error ? <div className="error">{error}</div> : null}
      <form className="card form-grid" onSubmit={createPortfolio}>
        <h3>Create Portfolio</h3>
        <input placeholder="Portfolio name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button className="button" type="submit">
          Add Portfolio
        </button>
      </form>
      <div className="card">
        <h3>Your Portfolios</h3>
        {items.length === 0 ? <p>No portfolios yet.</p> : null}
        {items.map((item) => (
          <div className="row-line" key={item.id}>
            <strong>{item.name}</strong>
            <span>{item.portfolio_type}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
