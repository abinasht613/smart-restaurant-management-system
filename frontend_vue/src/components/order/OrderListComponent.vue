<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="text-h5"> Orders List </v-card-title>

      <v-data-table
        v-model:expanded="expanded"
        :headers="headers"
        :items="orders"
        item-value="id"
        density="compact"
        class="elevation-2"
        show-expand
      >
      
        <!-- ✅ Custom Expand Button for Each Row -->
        <!-- ✅ Custom Expand Button for Each Row -->
        <template v-slot:[`item.expand`]="{ isExpanded, expand }">
          <v-btn
            icon
            :color="isExpanded ? 'red' : 'blue'"
            @click="expand(!isExpanded)"
          >
            <v-icon>{{ isExpanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </template>

        <template v-slot:item.order_time="{ item }">
          {{ formatDate(item.order_time) }}
        </template>

        <template v-slot:item.total_amount="{ item }">
          ₹{{ item.total_amount.toFixed(2) }}
        </template>

        <template v-slot:expanded-row="{ columns, item }">
          <tr>
            <td :colspan="columns.length">
              <v-table density="compact">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Size</th>
                    <th>Type</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Subtotal</th>
                    <th>Modifiers</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="itemDetail in item.items" :key="itemDetail.item_detail.item_id">
                    <td>{{ itemDetail.item_detail.item }}</td>
                    <td>{{ itemDetail.item_detail.size }}</td>
                    <td>{{ itemDetail.item_detail.type || '-' }}</td>
                    <td>{{ itemDetail.quantity }}</td>
                    <td>₹{{ itemDetail.price.toFixed(2) }}</td>
                    <td>₹{{ itemDetail.subtotal.toFixed(2) }}</td>
                    <td>
                      <v-chip
                        v-for="modifier in itemDetail.modifiers"
                        :key="modifier.modifier_id"
                        color="green-lighten-2"
                        class="ma-1"
                      >
                        {{ modifier.name }} (+₹{{ modifier.price }})
                      </v-chip>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </td>
          </tr>
        </template>
      </v-data-table>
      
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from '@/api';

// Store expanded rows
const expanded = ref([]);

// Sample orders data (replace with API call)
const orders = ref([]);

// Table headers
const headers = [
  { title: "Order ID", key: "id" },
  { title: "Customer", key: "customer" },
  { title: "Mobile", key: "mobile" },
  { title: "Order Time", key: "order_time" },
  { title: "Total Amount", key: "total_amount" },
  { title: "Expand", key: "data-table-expand" }
];

// Fetch orders from API
const fetchOrders = async () => {
  try {
    const response = await api.get("/order"); // Replace with actual API URL
    orders.value = response.data;
  } catch (error) {
    console.error("Error fetching orders:", error);
  }
};

// Format date
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString();
};

// Fetch data when component mounts
onMounted(fetchOrders);
</script>
