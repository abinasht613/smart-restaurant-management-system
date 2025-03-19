<template>
  <div>
    <h2>Live Order Updates</h2>
    <div v-if="orders.length === 0">No orders yet...</div>
    <ul>
      <li v-for="(order, index) in orders" :key="index">
        <strong>Order #{{ index + 1 }}</strong>: {{ order.customer }} - {{ order.total_amount }}
      </li>
    </ul>
  </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { io } from "socket.io-client";

const authStore = useAuthStore();
const orders = ref([]);

onMounted(() => {
  if (authStore.isAuthenticated) {
      const socket = io("ws://localhost:5000", {
        // transports: ["websocket"],
        query: {
          token: authStore.accessToken
        },
      });

      

      socket.on("connect", () => {
          console.log("Connected to WebSocket!");
          socket.emit("join", { room: "chefs" });
      });

      socket.on("new_order", (order) => {
          console.log("New order received:", order);
          // Update UI or trigger a notification
          orders.value.push(order);
      });
      // socket.onAny((event, data) => {
      //     console.log(`Received event: ${event}`, data);
      // });

      socket.on("connect_error", (err) => {
        console.error("Connection Error:", err.message);
      });

      socket.on("disconnect", () => {
        console.log("Disconnected from WebSocket.");
      });
  }
});

onUnmounted(() => {
      socket.disconnect(); // Cleanup on unmount
});

</script>
