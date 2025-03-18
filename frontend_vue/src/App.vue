<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <v-app>
    <v-container>
      <Navbar />
      <RouterView />
    </v-container>
  </v-app>

</template>