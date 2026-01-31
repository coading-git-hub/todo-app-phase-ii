/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  transpilePackages: ['better-auth'],

  webpack: (config) => {
    config.resolve.alias['@/lib/utils'] = require('path').resolve(__dirname, 'src/lib/utils');
    return config;
  },

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
