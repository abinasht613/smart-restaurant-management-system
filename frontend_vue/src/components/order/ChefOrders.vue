<template>
    <div>
        <h2>Chef Orders</h2>
        
    </div>
</template>
<script setup>
import { onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { io } from "socket.io-client";

const authStore = useAuthStore();

onMounted(() => {
  if (authStore.isAuthenticated) {
      const socket = io("http://localhost:5000", {
        // transports: ["websocket"],
        auth: {
          token: authStore.accessToken
        },
      });

      socket.on("connect", () => {
          console.log("Connected to WebSocket!");
      });

      socket.on("new_order", (order) => {
          console.log("New order received:", order);
          // Update UI or trigger a notification
      });

      socket.on("connect_error", (err) => {
        console.error("Connection Error:", err.message);
      });
  }
});

onUnmounted(() => {
      socket.disconnect(); // Cleanup on unmount
});

const logoutUser = () => {
  authStore.logout();
};






</script>
