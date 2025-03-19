import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/AuthStore';
import NotFoundView from '@/views/NotFoundView.vue';
import DummyView from '@/views/demo/DummyView.vue';
import LoginView from '@/views/user/LoginView.vue';
import RegistrationView from '@/views/user/RegistrationView.vue';
import PlaceOrderView from '@/views/order/PlaceOrderView.vue';
import ChefOrdersView from '@/views/order/ChefOrdersView.vue';
import ReportView from '@/views/report/ReportView.vue';
import SizeView from '@/views/item/SizeView.vue';
import TypeView from '@/views/item/TypeView.vue';
import ModifierView from '@/views/item/ModifierView.vue';
import MenuView from '@/views/item/MenuView.vue';
import OrderListView from '@/views/order/OrderListView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //     path: '/',
    //     name: 'dummy',
    //     component: DummyView,
    //   },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/registration',
      name: 'registration',
      component: RegistrationView,
    },
    {
      path: '/place-order',
      name: 'place-order',
      component: PlaceOrderView,
      meta: { requiresAuth: true }
    },
    {
      path: '/chef-order',
      name: 'chef-order',
      component: ChefOrdersView,
      meta: { requiresAuth: true }
    },
    {
      path: '/report',
      name: 'report',
      component: ReportView,
      meta: { requiresAuth: true }
    },
    {
      path: '/size',
      name: 'size',
      component: SizeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/type',
      name: 'type',
      component: TypeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/modifier',
      name: 'modifier',
      component: ModifierView,
      meta: { requiresAuth: true }
    },
    {
      path: '/menu',
      name: 'menu',
      component: MenuView,
      meta: { requiresAuth: true }
    },
    {
      path: '/order',
      name: 'order',
      component: OrderListView,
      meta: { requiresAuth: true }
    },
    // {
    //   path: '/jobs/:id',
    //   name: 'job',
    //   component: JobView,
    // },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
});

// 🔥 Add Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login'); // 🚀 Redirect to login if not authenticated
  } else {
    next();
  }
});

export default router;