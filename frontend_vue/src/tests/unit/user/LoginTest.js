import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import LoginView from '@/views/user/LoginView.vue';
import { useAuthStore } from '@/store/AuthStore';
import { createTestingPinia } from '@pinia/testing';
import { createRouter, createWebHistory } from 'vue-router';
import Toast from 'vue-toastification';
import axios from 'axios';

// Mocking router
const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/place-order', name: 'place-order' }]
});

// Mock axios
vi.mock('axios');

describe('LoginView.vue', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = mount(LoginView, {
      global: {
        plugins: [createTestingPinia(), router, Toast]
      }
    });
  });

  it('renders login form', () => {
    expect(wrapper.find('v-card-title').text()).toBe('Login');
    expect(wrapper.find('v-text-field[label="Username"]').exists()).toBe(true);
    expect(wrapper.find('v-text-field[label="Password"]').exists()).toBe(true);
  });

  it('shows an error if fields are empty', async () => {
    await wrapper.find('form').trigger('submit.prevent');
    expect(wrapper.vm.$toast.error).toHaveBeenCalledWith('Please fill all fields');
  });

  it('calls API and redirects on successful login', async () => {
    const mockResponse = {
      status: 200,
      data: {
        access_token: 'mockAccessToken',
        refresh_token: 'mockRefreshToken',
        user: { id: 1, uname: 'testuser' }
      }
    };
    axios.post.mockResolvedValue(mockResponse);

    wrapper.vm.form.uname = 'testuser';
    wrapper.vm.form.psw = 'password';
    await wrapper.find('form').trigger('submit.prevent');

    expect(axios.post).toHaveBeenCalledWith('api/login', { username: 'testuser', password: 'password' });
    expect(useAuthStore().setTokens).toHaveBeenCalled();
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/place-order');
  });

  it('shows error on login failure', async () => {
    axios.post.mockRejectedValue({ response: { status: 401, data: { message: 'Invalid credentials' } } });

    wrapper.vm.form.uname = 'wronguser';
    wrapper.vm.form.psw = 'wrongpassword';
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.vm.$toast.error).toHaveBeenCalledWith('Invalid credentials');
  });
});
