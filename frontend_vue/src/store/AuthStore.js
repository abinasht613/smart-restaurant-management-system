import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/api';

export const useAuthStore = defineStore('authStore', () => {
  const accessToken = ref(localStorage.getItem('access_token') || '');
  const refreshToken = ref(localStorage.getItem('refresh_token') || '');
  const user = ref(null);

  // Check if user is authenticated
  const isAuthenticated = computed(() => !!accessToken.value);

  // Save tokens to local storage
  function setTokens({access, refresh}) {
    console.log('setTokens', access, refresh);
    accessToken.value = access;
    refreshToken.value = refresh;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  // Remove tokens on logout
  function logout() {
    accessToken.value = '';
    refreshToken.value = '';
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Refresh the access token
  async function refreshAccessToken() {
    if (!refreshToken.value) return null;
    try {
      const response = await api.post('/refresh', {
        refresh_token: refreshToken.value,
      });
      setTokens(response.data.access_token, response.data.refresh_token);
      return response.data.access_token;
    } catch (err) {
      console.error('Failed to refresh token:', err);
      logout();
      return null;
    }
  }

  return { accessToken, refreshToken, user, isAuthenticated, setTokens, logout, refreshAccessToken };
});
