import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function Settings() {
  const { user, updateProfile } = useAuth();
  const [form, setForm] = useState({
    username: user?.username || "",
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    phone: user?.phone || "",
  });
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");

  const handleSave = async (e) => {
    e.preventDefault();
    setError("");
    setMsg("");
    const result = await updateProfile(form);
    if (result.success) {
      setMsg("Profile updated!");
    } else {
      setError(result.error || "Update failed");
    }
  };

  return (
    <section>
      <h1>Settings</h1>
      {error && <div className="error">{error}</div>}
      {msg && <div className="card" style={{color: "#22c55e", borderColor: "#166534"}}>{msg}</div>}
      <form className="card form-grid" onSubmit={handleSave} style={{maxWidth: 450}}>
        <h3>Profile</h3>
        <div className="row-line" style={{borderTop: "none"}}>
          <strong>Email</strong>
          <span style={{color: "#64748b"}}>{user?.email || "-"}</span>
        </div>
        <label>Username</label>
        <input value={form.username} onChange={(e) => setForm(s => ({...s, username: e.target.value}))} />
        <label>First Name</label>
        <input value={form.first_name} onChange={(e) => setForm(s => ({...s, first_name: e.target.value}))} />
        <label>Last Name</label>
        <input value={form.last_name} onChange={(e) => setForm(s => ({...s, last_name: e.target.value}))} />
        <label>Phone</label>
        <input value={form.phone} onChange={(e) => setForm(s => ({...s, phone: e.target.value}))} />
        <button className="button" type="submit">Save Changes</button>
      </form>
    </section>
  );
}
