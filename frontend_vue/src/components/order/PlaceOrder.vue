<template>
    <div>
        <h2>Order</h2>
        <form @submit.prevent="handleSubmit">
            
            Input Order: <input type="text" v-model="newOrder.order_text" name="order_text" required>
            <div v-if="orderStore.error">{{ orderStore.error }}</div>
            <button v-if="authStore.isAuthenticated" @click="placeNewOrder">Place Order</button>
            <button v-if="authStore.isAuthenticated" @click="logoutUser">Logout</button>
            <button v-else>Not Logged In</button>

            

            <div v-if="orderStore.loading">Loading...</div>
                

        <div class="imgcontainer">
            <!-- <img src="img_avatar2.png" alt="Avatar" class="avatar"> -->
        </div>
        </form>
    </div>
</template>
<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { useOrderStore } from '@/store/order/OrderStore';

const authStore = useAuthStore();
const orderStore = useOrderStore();

onMounted(() => {
  if (authStore.isAuthenticated) {
    // console.log(authStore.isAuthenticated)
    // console.log(authStore.accessToken)
    // console.log(authStore.refreshToken)
    // console.log(authStore.user)
    // console.log("Stored Token:", JSON.stringify(authStore.accessToken, null, 2));
    // orderStore.fetchOrders();
  }
});

const newOrder = {
    order_text: "Two large chicken pepperoni pizza extra cheese, one caesar salad, and two diet coke with Origano",
};

const placeNewOrder = () => {
  orderStore.placeOrder(newOrder);
};

const logoutUser = () => {
  authStore.logout();
};
</script>
