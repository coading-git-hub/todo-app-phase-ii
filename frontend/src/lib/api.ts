
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://kiran-ahmed-todo-phase-ii.hf.space';

// Create axios instance
export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  // Enable withCredentials to handle cookies and authentication properly
  withCredentials: true
});

console.log('API baseURL set to:', `${API_BASE_URL}/api`);

// Request interceptor to add token
apiClient.interceptors.request.use(
  (config) => {
    // Check if we're in browser environment (not SSR)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response || error.message || error);
    if (error.response?.status === 401) {
      // Clear token and redirect to login (only in browser)
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/signin';
      }
    } else if (error.code === 'NETWORK_ERROR' || error.message.includes('Network Error')) {
      console.error('Network error - unable to reach the server. Please check the backend is deployed and accessible.');
    }
    return Promise.reject(error);
  }
);