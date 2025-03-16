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
  <div>
    <!-- Popular Items Chart -->
    <h2>Popular Items</h2>
    <VueApexCharts
      type="bar"
      height="350"
      :options="{
        chart: { type: 'bar' },
        xaxis: { categories: popularItems.map(item => item.item) },
        title: { text: 'Top 10 Popular Items' }
      }"
      :series="[{ name: 'Quantity', data: popularItems.map(item => item.quantity) }]"
    />

    <!-- Peak Hours Chart -->
    <h2>Peak Order Hours</h2>
    <VueApexCharts
      type="line"
      height="350"
      :options="{
        chart: { type: 'line' },
        xaxis: { categories: peakHours.map(hour => hour.hour) },
        title: { text: 'Orders by Hour' }
      }"
      :series="[{ name: 'Total Orders', data: peakHours.map(hour => hour.total_orders) }]"
    />

    <!-- Sales Trends Chart -->
    <h2>Sales Trends</h2>
    <VueApexCharts
      type="area"
      height="350"
      :options="{
        chart: { type: 'area' },
        xaxis: { categories: salesTrends.map(sale => sale.date) },
        title: { text: 'Daily Sales Trends' }
      }"
      :series="[{ name: 'Total Sales', data: salesTrends.map(sale => sale.total_sales) }]"
    />
  </div>
</template>
