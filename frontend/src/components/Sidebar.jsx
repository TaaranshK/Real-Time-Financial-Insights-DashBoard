import React from "react";
import { FiBarChart2, FiBriefcase, FiHome, FiSettings, FiTrendingUp } from "react-icons/fi";
import { Link, useLocation } from "react-router-dom";

const items = [
  { name: "Dashboard", path: "/", icon: FiHome },
  { name: "Portfolio", path: "/portfolio", icon: FiBriefcase },
  { name: "Holdings", path: "/holdings", icon: FiBarChart2 },
  { name: "Market Analysis", path: "/analysis", icon: FiTrendingUp },
  { name: "Settings", path: "/settings", icon: FiSettings },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="brand">
        <h1>FinDash</h1>
        <p>Monitoring</p>
      </div>
      <nav className="menu">
        {items.map((item) => {
          const Icon = item.icon;
          const active = location.pathname === item.path;
          return (
            <Link key={item.path} to={item.path} className={`menu-item ${active ? "active" : ""}`}>
              <Icon />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
