import React from "react";
import { FiLogOut, FiUser } from "react-icons/fi";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const TITLES = {
  "/": "Dashboard",
  "/portfolio": "Portfolio",
  "/holdings": "Holdings",
  "/analysis": "Market Analysis",
  "/settings": "Settings",
};

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <header className="navbar">
      <h2>{TITLES[location.pathname] || "Financial Monitoring"}</h2>
      <div className="navbar-right">
        <span className="user-pill">
          <FiUser />
          {user?.username || user?.email || "User"}
        </span>
        <button
          className="button danger"
          onClick={() => {
            logout();
            navigate("/login");
          }}
        >
          <FiLogOut />
          Logout
        </button>
      </div>
    </header>
  );
}
