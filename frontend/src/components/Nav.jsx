import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Nav() {
  const auth = useAuth();
  return (
    <nav style={{ margin: "12px 0", display: "flex", gap: 12 }}>
      <Link to="/">Home</Link>
      <Link to="/notifications">Notifications</Link>
      <Link to="/fees">Fees</Link>
      <Link to="/resources">Resources</Link>
      <Link to="/attachments">Attachments</Link>
      {!auth?.token ? (
        <Link to="/login">Login</Link>
      ) : (
        <button onClick={auth.logout}>Logout</button>
      )}
    </nav>
  );
}
