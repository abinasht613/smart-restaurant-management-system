<template>
  <v-app-bar color="green-darken-3" density="comfortable">
    <v-container class="d-flex align-center justify-space-between">
      <!-- Logo (if needed) -->
      <!-- <v-img src="logo.png" max-height="40" max-width="40" contain></v-img> -->

      <!-- Desktop Navigation (Hidden on Mobile) -->
      <v-row class="d-none d-md-flex">
        <v-btn
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          :variant="isActiveLink(link.to) ? 'elevated' : 'text'"
          :color="isActiveLink(link.to) ? 'white' : 'green-lighten-3'"
          class="font-bold"
        >
          {{ link.label }}
        </v-btn>
      </v-row>

      <!-- Mobile Menu Button (Visible on Small Screens) -->
      <v-app-bar-nav-icon class="d-md-none" @click="drawer = !drawer" />
    </v-container>
  </v-app-bar>

  <!-- Mobile Navigation Drawer -->
  <v-navigation-drawer v-model="drawer" temporary app>
    <v-list>
      <v-list-item
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        @click="drawer = false"
      >
        <v-list-item-title>{{ link.label }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const drawer = ref(false); // Controls the mobile menu drawer

// Navigation links
const links = ref([
  { to: "/", label: "Dummy" },
  { to: "/login", label: "Login" },
  { to: "/registration", label: "Registration" },
  { to: "/place-order", label: "Place Order" },
  { to: "/chef-order", label: "Chef Order" },
  { to: "/report", label: "Report" },
  { to: "/size", label: "Size" },
  { to: "/type", label: "Type" },
  { to: "/modifier", label: "Modifier" },
  { to: "/menu", label: "Menu" },
  { to: "/order", label: "Order"}
]);

// Function to check if link is active
const isActiveLink = (path) => {
  return route.path === path;
};
</script>
