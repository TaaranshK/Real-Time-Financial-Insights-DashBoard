import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function Settings() {
  const { user } = useAuth();
  const [profile] = useState(user || {});

  return (
    <section>
      <h1>Settings</h1>
      <div className="card">
        <h3>Profile</h3>
        <div className="row-line">
          <strong>Username</strong>
          <span>{profile.username || "-"}</span>
        </div>
        <div className="row-line">
          <strong>Email</strong>
          <span>{profile.email || "-"}</span>
        </div>
        <div className="row-line">
          <strong>Role</strong>
          <span>{profile.role || "USER"}</span>
        </div>
      </div>
    </section>
  );
}
