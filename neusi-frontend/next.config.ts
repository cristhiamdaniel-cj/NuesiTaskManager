import type { NextConfig } from "next";

/**
 * Configuración de conexión al backend Django.
 * Puedes cambiar la IP o dominio si trabajas desde otra red.
 * Ejemplo LAN: http://10.100.42.36:8076
 */
const BACKEND_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8076";

const nextConfig: NextConfig = {
  // Reescribe las peticiones /api/* hacia el backend Django
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${BACKEND_BASE}/api/:path*` },
    ];
  },

  // Opcionalmente, si vas a exportar estático:
  reactStrictMode: true,
  swcMinify: true,
};

export default nextConfig;
