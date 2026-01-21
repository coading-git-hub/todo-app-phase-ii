/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  transpilePackages: ['better-auth'],

  experimental: {
    serverActions: {
      allowedOrigins: [
        'https://todo-app-phase-ii-jt2k.vercel.app',
        'http://localhost:3000',
        'http://localhost:3001',
        
      ],
    },
  },
}

module.exports = nextConfig
