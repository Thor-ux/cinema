const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

function errorMessage(detail) {
  if (!detail) return "Something went wrong";
  if (typeof detail === "string") return detail;
  // FastAPI validation errors: [{loc, msg}, ...]
  if (Array.isArray(detail)) return detail.map((d) => d.msg.replace(/^Value error, /, "")).join("; ");
  return "Something went wrong";
}

export async function api(path, { method = "GET", body, params } = {}) {
  const url = new URL(API_URL + path);
  if (params) Object.entries(params).forEach(([k, v]) => v != null && url.searchParams.set(k, v));

  const token = localStorage.getItem("token");
  const res = await fetch(url, {
    method,
    headers: {
      ...(body !== undefined && { "Content-Type": "application/json" }),
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    if (res.status === 401) window.dispatchEvent(new Event("auth:expired"));
    throw new ApiError(errorMessage(data?.detail), res.status);
  }
  return data;
}

export const formatPrice = (value) => `${Number(value).toLocaleString("ru-RU")} ₽`;
export const formatTime = (iso) =>
  new Date(iso).toLocaleString(undefined, { weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
