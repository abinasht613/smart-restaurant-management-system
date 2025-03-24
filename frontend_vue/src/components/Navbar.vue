<template>
  <v-app-bar color="green-darken-3" density="comfortable">
    <v-container class="d-flex align-center justify-space-between">
      <!-- Logo (if needed) -->
      <!-- <v-img src="logo.png" max-height="40" max-width="40" contain></v-img> -->

      <!-- Desktop Navigation (Hidden on Mobile) -->
      <v-row class="d-none d-md-flex">
        <v-btn
          v-for="link in filteredLinks"
          :key="link.to"
          :to="link.to"
          :variant="isActiveLink(link.to) ? 'elevated' : 'text'"
          :color="isActiveLink(link.to) ? 'white' : 'green-lighten-3'"
          class="font-bold"
        >
          {{ link.label }}
        </v-btn>
        
      </v-row>
      
      <!-- Right Section: User Info & Logout -->
      <v-menu v-if="authStore.isAuthenticated" offset-y>
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            color="white"
            variant="text"
            class="text-truncate"
            style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
          >
            <v-icon class="mr-2">mdi-account</v-icon>
            Welcome {{ authStore.user?.fname }} ({{ authStore.user?.role }})
          </v-btn>
        </template>

        <v-list style="min-width: 120px;"> 
          <v-list-item @click="logoutUser">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>



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
  <!-- <button v-if="authStore.isAuthenticated" @click="logoutUser">Logout</button> -->
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from '@/store/AuthStore';
import { useRoute } from "vue-router";

const authStore = useAuthStore();
const route = useRoute();
const drawer = ref(false); // Controls the mobile menu drawer

// Navigation links
const links = ref([
  // { to: "/", label: "Dummy", guestOnly: true },
  { to: "/login", label: "Login", guestOnly: true },
  { to: "/registration", label: "Registration", guestOnly: true },
  { to: "/place-order", label: "Place Order", requiresAuth: true },
  { to: "/chef-order", label: "Chef Order", requiresAuth: true },
  { to: "/report", label: "Report", requiresAuth: true },
  { to: "/size", label: "Size", requiresAuth: true },
  { to: "/type", label: "Type", requiresAuth: true },
  { to: "/modifier", label: "Modifier", requiresAuth: true },
  { to: "/menu", label: "Menu", requiresAuth: true },
  { to: "/order", label: "Order", requiresAuth: true },
  { to: "/item", label: "Items", requiresAuth: true },
  // { to: "/text", label: "text", requiresAuth: true },
]);

// Filter links based on authentication
const filteredLinks = computed(() => {
  return links.value.filter(link =>
    authStore.isAuthenticated ? link.requiresAuth : link.guestOnly
  );
});

// Function to check if link is active
const isActiveLink = (path) => {
  return route.path === path;
};

const logoutUser = () => {
  authStore.logout();
};
</script>
