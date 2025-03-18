<template>
  <v-container>
    <v-row>
      <v-col v-for="item in menuItems" :key="item.id" cols="12" md="6" lg="4">
        <v-card class="mx-auto" elevation="4">
          <v-card-title class="bg-green-darken-3 text-white">
            {{ item.name }}
          </v-card-title>

          <v-card-text v-if="item.variants.length">
            <v-data-table
              :headers="headers"
              :items="item.variants"
              density="compact"
              class="elevation-2"
              items-per-page="-1" 
              hide-items-per-page
              disable-pagination
              hide-default-footer
            />
          </v-card-text>

          <v-card-text v-else class="text-center text-grey-darken-1">
            No Variants Available
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loader -->
    <v-overlay v-if="loading" persistent>
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from '@/api';

const menuItems = ref([]); // Store API data
const loading = ref(true); // Show loader while fetching

// Table headers for variants
const headers = ref([
  { title: "Size", key: "size" },
  { title: "Type", key: "type", value: (v) => v.type || "N/A" },
  { title: "Price", key: "price", align: "end" },
  { title: "Stock", key: "stock", align: "end" },
]);

// Fetch menu items from API
const fetchMenuItems = async () => {
  try {
    const response = await api.get("/menu");
    menuItems.value = response.data;
  } catch (error) {
    console.error("Error fetching menu:", error);
  } finally {
    loading.value = false;
  }
};

// Fetch data when component mounts
onMounted(fetchMenuItems);
</script>
