// import './assets/main.css';
// import 'primeicons/primeicons.css';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import router from './router';
import { createPinia } from 'pinia';
import vuetify from './plugins/vuetify';

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VUE_APP_API_URL || 'http://localhost:5000';
const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(Toast);
app.use(pinia);
app.use(vuetify);

app.mount('#app');