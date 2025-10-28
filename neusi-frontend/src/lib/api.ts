/**
 * Funciones de conexión con el backend Django
 * Maneja sesión, login, logout y CSRF.
 */

const API = process.env.NEXT_PUBLIC_API_BASE!; // Ej: http://192.168.2.29:8076/api/

/* --- Utilidad para leer cookie CSRF --- */
function getCookie(name: string) {
  const m = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return m ? m[2] : "";
}

/* --- CSRF Token --- */
export async function getCsrf(): Promise<string> {
  const res = await fetch(`${API}auth/csrf/`, { credentials: "include" });
  const data = await res.json().catch(() => ({}));
  return data?.csrfToken || getCookie("csrftoken") || "";
}

/* --- Login --- */
export async function login(username: string, password: string) {
  const csrftoken = await getCsrf();

  const res = await fetch(`${API}auth/login/`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Error al iniciar sesión");
  return data;
}

/* --- Verificar sesión actual --- */
export async function me() {
  try {
    const res = await fetch(`${API}auth/me/`, { credentials: "include" });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

/* --- Logout --- */
export async function logout() {
  const csrftoken = await getCsrf();
  const res = await fetch(`${API}auth/logout/`, {
    method: "POST",
    credentials: "include",
    headers: { "X-CSRFToken": csrftoken },
  });
  if (!res.ok) throw new Error("No se pudo cerrar sesión");
  return true;
}
