<template>
  <v-container class="order-container">
    <h2 class="text-h5 mb-4">Live Order Updates</h2>

    <v-alert v-if="orders.length === 0" type="info">
      No orders yet...
    </v-alert>

    <v-row>
      <v-col v-for="(order, index) in orders" :key="index" cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Order #{{ index + 1 }}</v-card-title>
          <v-card-subtitle>Customer: {{ order.customer }}</v-card-subtitle>
          
          <v-list dense>
            <v-list-item v-for="(item, i) in order.items" :key="i">
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.quantity }} × {{ item.item_detail.size }} {{ item.item_detail.type }} {{ item.item_detail.item }}
                  <span v-for="modifier in item.modifiers">{{ modifier.name }}</span>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-card-text>
            <strong>Total:</strong> ${{ order.total_amount }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { io } from "socket.io-client";
import { useToast } from "vue-toastification";

const authStore = useAuthStore();
const orders = ref([]);
const toast = useToast();

const apiBaseUrl = import.meta.env.VUE_APP_API_URL || "http://localhost:5000";
const wsBaseUrl = apiBaseUrl.replace(/^http/, "ws"); // Convert http to ws

const socket = io(wsBaseUrl, {
  // transports: ["websocket"],
  query: {
    token: authStore.accessToken
  },
});

onMounted(() => {
  if (authStore.isAuthenticated) {
      socket.on("connect", () => {
          console.log("Connected to WebSocket!");
          socket.emit("join", { room: "chefs" });
      });

      socket.on("new_order", (order) => {
          console.log("New order received:", order);
          toast.success("New order received!");
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
<style>
.order-container {
  min-width: 800px; /* Ensures the container doesn't shrink too much */
  max-width: 100%; /* Allows it to expand dynamically */
}
</style>
