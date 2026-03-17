const API_BASE = "http://localhost:8000";

export async function apiFetch(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: {
            "Content-Type": "application/json",
        },
        ...options,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "API Error");
    }

    return response.json();
}