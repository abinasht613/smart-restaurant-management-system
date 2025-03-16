import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';

export const useOrderStore = defineStore('orderStore', () => {
  const orders = ref([]);
  const loading = ref(false);
  const error = ref(null);

  // Fetch orders from API with authentication
  async function fetchOrders() {
    loading.value = true;
    try {
      const response = await api.get('/orders'); // Uses Axios with token
      orders.value = response.data;
    } catch (err) {
      error.value = err.response?.data?.message || err.message;
    } finally {
      loading.value = false;
    }
  }

  // Place a new order
  async function placeOrder(orderData) {
    try {
      const response = await api.post('/order', orderData);
      if(response.status==201){
        // console.log(response);
        orders.value.push(response.data);
      }
      else {
        console.log(response);
        // error.value = err.response?.data?.error || err.message;  
      }
    } catch (err) {
      // console.log(err);
      error.value = err.response?.data?.error || err.message;
    }
  }

  return { orders, loading, error, fetchOrders, placeOrder };
});
