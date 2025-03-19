<script setup>
import { ref, onMounted } from "vue";
import api from '@/api';
import VueApexCharts from "vue3-apexcharts";
import { useAuthStore } from '@/store/AuthStore';

const authStore = useAuthStore();
const popularItems = ref([]);
const peakHours = ref([]);
const salesTrends = ref([]);

const fetchReports = async () => {
  try {
    const response = await api.get('/reports');
    popularItems.value = response.data.popular_items;
    peakHours.value = response.data.peak_hours;
    salesTrends.value = response.data.sales_trends;
  } catch (error) {
    console.error("Error fetching reports:", error);
  }
};

onMounted(() => {
    if (authStore.isAuthenticated) {
        fetchReports();
    }
});
</script>
<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Popular Items</h2>
        <VueApexCharts
          type="bar"
          height="350"
          :options="{
            chart: { type: 'bar' },
            xaxis: { categories: popularItems.map(item => item.item) },
            title: { text: 'Top 10 Popular Items' },
            responsive: [{ breakpoint: 600, options: { chart: { width: '100%' } } }]
          }"
          :series="[{ name: 'Quantity', data: popularItems.map(item => item.quantity) }]"
        />
      </v-col>

      <v-col cols="12">
        <h2 class="text-center">Peak Order Hours</h2>
        <VueApexCharts
          type="line"
          height="350"
          :options="{
            chart: { type: 'line' },
            xaxis: { categories: peakHours.map(hour => hour.hour) },
            title: { text: 'Orders by Hour' },
            responsive: [{ breakpoint: 600, options: { chart: { width: '100%' } } }]
          }"
          :series="[{ name: 'Total Orders', data: peakHours.map(hour => hour.total_orders) }]"
        />
      </v-col>

      <v-col cols="12">
        <h2 class="text-center">Sales Trends</h2>
        <VueApexCharts
          type="area"
          height="350"
          :options="{
            chart: { type: 'area' },
            xaxis: { categories: salesTrends.map(sale => sale.date) },
            title: { text: 'Daily Sales Trends' },
            responsive: [{ breakpoint: 600, options: { chart: { width: '100%' } } }]
          }"
          :series="[{ name: 'Total Sales', data: salesTrends.map(sale => sale.total_sales) }]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>