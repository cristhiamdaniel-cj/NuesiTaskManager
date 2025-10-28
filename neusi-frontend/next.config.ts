import type { NextConfig } from 'next'

/**
 * Base del backend. Ajusta según entorno:
 * - Local LAN: http://10.100.42.36:8076
 * - Producción/ngrok: https://devops-neusi.ngrok.io
 */
const BACKEND_BASE =
  process.env.NEXT_PUBLIC_API_BASE || 'http://10.100.42.36:8076'

const nextConfig: NextConfig = {
  experimental: {
  // @ts-expect-error - allowedDevOrigins aún no está tipado en Next.js
  allowedDevOrigins: [
    'http://10.100.42.36:3000',
    'http://localhost:3000',
  ],
},
  async rewrites() {
    return [
      { source: '/api/:path*', destination: `${BACKEND_BASE}/api/:path*` },
    ]
  },
}

export default nextConfig
