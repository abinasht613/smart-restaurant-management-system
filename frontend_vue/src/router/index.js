import { createRouter, createWebHistory } from 'vue-router';
import NotFoundView from '@/views/NotFoundView.vue';
import DummyView from '@/views/demo/DummyView.vue';
import LoginView from '@/views/user/LoginView.vue';
import RegistrationView from '@/views/user/RegistrationView.vue';
import PlaceOrderView from '@/views/order/PlaceOrderView.vue';
import ChefOrdersView from '@/views/order/ChefOrdersView.vue';
import ReportView from '@/views/report/ReportView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/',
        name: 'dummy',
        component: DummyView,
      },
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
    },
    {
      path: '/chef-order',
      name: 'chef-order',
      component: ChefOrdersView,
    },
    {
      path: '/report',
      name: 'report',
      component: ReportView,
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

export default router;