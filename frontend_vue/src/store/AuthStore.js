import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('authStore', () => {
  const accessToken = ref(localStorage.getItem('access_token') || '');
  const refreshToken = ref(localStorage.getItem('refresh_token') || '');
  //const user = ref(null);
  const user = ref(JSON.parse(localStorage.getItem('user')) || null);
  
  const router = useRouter();

  // Check if user is authenticated
  const isAuthenticated = computed(() => !!accessToken.value);

  // Save tokens to local storage
  function setTokens({access, refresh, user: userData}) {
    console.log('setTokens', access, refresh,user);
    accessToken.value = access;
    refreshToken.value = refresh;
    
    const storedUser = {
      id: userData.id,
      fname: userData.fname,
      lname: userData.lname,
      role: userData.role
    };

    user.value = storedUser;
    console.log(user.value);
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    localStorage.setItem('user', JSON.stringify(storedUser));
    console.log('User stored:', localStorage.getItem('user'));
  }

  // Remove tokens on logout
  function logout() {
    accessToken.value = '';
    refreshToken.value = '';
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');

    setTimeout(() => {
     // Redirect to login page
    router.push("/login");
  }, 100); // Small delay to ensure state updates
    
  }

  // Refresh the access token
  async function refreshAccessToken() {
    if (!refreshToken.value) 
      return setTimeout(() => {
        // Redirect to login page
       router.push("/login");
     }, 100); // Small delay to ensure state updates;
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
