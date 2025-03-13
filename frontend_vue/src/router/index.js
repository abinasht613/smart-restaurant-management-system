import { createRouter, createWebHistory } from 'vue-router';
import NotFoundView from '@/views/NotFoundView.vue';
import DummyView from '@/views/demo/DummyView.vue';
import LoginView from '@/views/user/LoginView.vue';
import RegistrationView from '@/views/user/RegistrationView.vue';


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
    // {
    //   path: '/jobs/:id',
    //   name: 'job',
    //   component: JobView,
    // },
    // {
    //   path: '/jobs/add',
    //   name: 'add-job',
    //   component: AddJobView,
    // },
    // {
    //   path: '/jobs/edit/:id',
    //   name: 'edit-job',
    //   component: EditJobView,
    // },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
});

export default router;