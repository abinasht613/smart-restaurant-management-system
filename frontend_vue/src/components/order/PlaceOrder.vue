<template>
    <div>
        <h2>Order</h2>
        <form @submit.prevent="handleSubmit">
            
            Customer Name: <input type="text" v-model="newOrder.customer_name" name="customer_name">
            Customer Phone: <input type="text" v-model="newOrder.customer_mobile" name="customer_mobile" required>

            Input Order: <input type="text" v-model="newOrder.order_text" name="order_text" class="order-input" required>
            <div v-if="orderStore.error">{{ orderStore.error }}</div>
            <button v-if="authStore.isAuthenticated" @click="placeNewOrder">Place Order</button>

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
import { useToast } from "vue-toastification";

const authStore = useAuthStore();
const orderStore = useOrderStore();
const toast = useToast();

onMounted(() => {
  if (authStore.isAuthenticated) {
    // console.log(authStore.isAuthenticated)
    // console.log(authStore.accessToken)
    // console.log(authStore.refreshToken)
    // console.log(authStore.user)
    // console.log("Stored Token:", JSON.stringify(authStore.accessToken, null, 2));
    // orderStore.fetchOrders();
    console.log("Access Token:", authStore.accessToken);
    console.log("auth-user",authStore.user);
  }
});

const newOrder = {
    order_text: "Two large chicken pepperoni pizza extra cheese, one caesar salad, and two diet coke with Origano",
    "customer_mobile":"N/A",
    "customer_name":"N/A"
};

const placeNewOrder = () => {
  orderStore.placeOrder(newOrder);
};


</script>

<style>
.order-input {
  width: 100%;
  height: 100px; /* Adjust as needed */
  padding: 10px;
  font-size: 16px;
}

</style>
