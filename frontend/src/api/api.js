const API_BASE = "http://localhost:8000";

export async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: {
            "Content-Type": "application/json",
            ...(token && { Authorization: `Bearer ${token}` }),
        },
        ...options,
    });

    let data;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        throw new Error(data?.detail || "API Error");
    }

    return data;
}

export async function login(email, password) {
    const res = await apiFetch(`/auth/login?email=${email}&password=${password}`, {
        method: "POST",
    });

    localStorage.setItem("token", res.access_token);

    return res;
}