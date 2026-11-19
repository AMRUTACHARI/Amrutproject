import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import api from "@/lib/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // null = checking, false = guest, object = authed
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    try {
      const { data } = await api.get("/auth/me", { timeout: 3500 });
      setUser(data.user);
      return data.user;
    } catch {
      setUser(false);
      return false;
    }
  }, []);

  useEffect(() => {
    let active = true;
    const safetyTimer = setTimeout(() => {
      if (active) setLoading(false);
    }, 2500);

    (async () => {
      try {
        await refreshUser();
      } catch {
        if (active) setUser(false);
      } finally {
        if (active) {
          clearTimeout(safetyTimer);
          setLoading(false);
        }
      }
    })();

    return () => {
      active = false;
      clearTimeout(safetyTimer);
    };
  }, [refreshUser]);

  const login = async (email, password, remember) => {
    const { data } = await api.post("/auth/login", { email, password, remember });
    if (data.token) {
      localStorage.setItem("flora_token", data.token);
    }
    setUser(data.user);
    return data.user;
  };

  const register = async (payload) => {
    const { data } = await api.post("/auth/register", payload);
    if (data.token) {
      localStorage.setItem("flora_token", data.token);
    }
    setUser(data.user);
    return data;
  };

  const logout = async () => {
    try {
      await api.post("/auth/logout");
    } catch {
      /* ignore */
    }
    localStorage.removeItem("flora_token");
    setUser(false);
  };

  const value = { user, loading, login, register, logout, setUser, refreshUser };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
