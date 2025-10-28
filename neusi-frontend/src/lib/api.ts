// src/lib/api.ts
// API base (absoluta, evita problemas de proxy en Next)
const ABS = process.env.NEXT_PUBLIC_API_BASE?.replace(/\/+$/, "") || "http://localhost:8076";
export const API = `${ABS}/api/backlog`;

// --- Utilidad para obtener cookie CSRF ---
function getCookie(name: string) {
  return document.cookie
    .split("; ")
    .find((x) => x.startsWith(name + "="))
    ?.split("=")[1] ?? "";
}

// --- Sesión actual ---
export async function me() {
  const r = await fetch(`${API}/auth/me/`, {
    credentials: "include",
  });
  if (!r.ok) throw new Error(`Error (${r.status}) al consultar sesión`);
  return r.json();
}

// --- Login ---
export async function login(username: string, password: string) {
  // 1️⃣ Pedir CSRF (cookie)
  await fetch(`${API}/auth/csrf/`, { credentials: "include" });

  // 2️⃣ Extraer cookie csrftoken
  const csrftoken = getCookie("csrftoken");

  // 3️⃣ Enviar credenciales
  const r = await fetch(`${API}/auth/login/`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ username, password }),
  });

  if (!r.ok) {
    const msg = await r.text();
    throw new Error(`Login failed (${r.status}): ${msg}`);
  }

  return r.json();
}

// --- Logout ---
export async function logout() {
  const csrftoken = getCookie("csrftoken");
  const r = await fetch(`${API}/auth/logout/`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: "{}",
  });
  if (!r.ok) throw new Error(`Logout failed (${r.status})`);
  return r.json();
}
