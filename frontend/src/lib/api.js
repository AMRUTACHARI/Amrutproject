import axios from "axios";

export function resolveApiBaseUrl() {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    const isLocalhost =
      hostname === "localhost" ||
      hostname === "127.0.0.1" ||
      hostname.endsWith(".local");

    // In production, when hosted on Vercel, or over HTTPS, ALWAYS use relative "/api"
    // to prevent browser Mixed Content blocks and ensure Vercel rewrites handle it.
    if (!isLocalhost || window.location.protocol === "https:") {
      return "/api";
    }

    // In local development on HTTP localhost, use backend port if set or fallback to 8001
    const rawUrl = process.env.REACT_APP_BACKEND_URL;
    if (rawUrl && rawUrl !== "undefined" && rawUrl.trim() !== "") {
      return `${rawUrl.replace(/\/+$/, "")}/api`;
    }
    return "http://localhost:8001/api";
  }

  const rawUrl = process.env.REACT_APP_BACKEND_URL;
  if (rawUrl && rawUrl !== "undefined" && rawUrl.trim() !== "") {
    return `${rawUrl.replace(/\/+$/, "")}/api`;
  }
  return "/api";
}

export const API = resolveApiBaseUrl();

const api = axios.create({
  baseURL: API,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("flora_token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Attempt a silent refresh once on 401, then retry the original request.
let refreshing = null;
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    const status = error.response?.status;
    const url = original?.url || "";
    const isAuthProbe =
      url.includes("/auth/login") ||
      url.includes("/auth/refresh") ||
      url.includes("/auth/me") ||
      url.includes("/auth/register");
    if (status === 401 && !original._retry && !isAuthProbe) {
      original._retry = true;
      try {
        refreshing = refreshing || api.post("/auth/refresh");
        await refreshing;
        refreshing = null;
        return api(original);
      } catch (e) {
        refreshing = null;
      }
    }
    return Promise.reject(error);
  }
);

export function formatApiErrorDetail(detail) {
  if (detail == null) return null;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail))
    return detail
      .map((e) => (e && typeof e.msg === "string" ? e.msg : JSON.stringify(e)))
      .filter(Boolean)
      .join(" ");
  if (detail && typeof detail.msg === "string") return detail.msg;
  return String(detail);
}

export function apiError(e) {
  const detail = formatApiErrorDetail(e?.response?.data?.detail);
  if (detail) return detail;
  if (e?.response?.data?.message) return String(e.response.data.message);
  if (typeof e?.response?.data === "string" && e.response.data.length > 0 && e.response.data.length < 200) {
    return e.response.data;
  }
  if (e?.response?.status) {
    return `Server error (${e.response.status}): ${e.response.statusText || "Request failed"}`;
  }
  if (e?.message) return e.message;
  return "Something went wrong. Please try again.";
}

export default api;
