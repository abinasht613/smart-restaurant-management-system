import { defineStore } from 'pinia';
import api from '@/api';

export const useMenuStore = defineStore('menu', {
  state: () => ({
    menuItems: []
  }),

  actions: {
    async fetchMenu() {
      try {
        const response = await api.get('/items');
        this.menuItems = response.data.map(item => item.iname);
      } catch (error) {
        console.error('Error fetching menu:', error);
      }
    }
  }
});
