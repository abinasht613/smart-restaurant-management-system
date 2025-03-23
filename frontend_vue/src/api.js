import axios from 'axios';
import { useAuthStore } from '@/store/AuthStore';

const api = axios.create({
  baseURL: import.meta.env.VUE_APP_API_URL || "http://localhost:5000", // Replace with your API base URL
  headers: { 'Content-Type': 'application/json' }
});

// Attach the access token to every request
api.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Handle token expiration and refresh
api.interceptors.response.use(
  (response) => response, 
  async (error) => {
    const authStore = useAuthStore();
    const originalRequest = error.config;

    // If token expired, refresh and retry request
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newToken = await authStore.refreshAccessToken();
      if (newToken) {
        api.defaults.headers.common.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
