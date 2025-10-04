import React, { createContext, useContext, useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import * as api from "./api";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem("uzuri_auth");
    if (stored) {
      try {
        const tokens = JSON.parse(stored);
        if (tokens?.access)
          axiosClient.defaults.headers.common.Authorization = `Bearer ${tokens.access}`;
        api
          .me()
          .then((u) => setUser(u))
          .catch(() => setUser(null))
          .finally(() => setLoading(false));
      } catch (e) {
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (creds) => {
    const data = await api.login(creds);
    const access = data.access || data.token;
    const refresh = data.refresh || null;
    if (access) {
      axiosClient.defaults.headers.common.Authorization = `Bearer ${access}`;
      localStorage.setItem("uzuri_auth", JSON.stringify({ access, refresh }));
      const u = await api.me();
      setUser(u);
      return u;
    }
    throw new Error("Login failed");
  };

  const logout = () => {
    localStorage.removeItem("uzuri_auth");
    delete axiosClient.defaults.headers.common.Authorization;
    setUser(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
export default AuthProvider;
