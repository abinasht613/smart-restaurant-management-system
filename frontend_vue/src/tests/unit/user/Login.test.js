import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Login from '@/components/user/Login.vue';
import axios from 'axios';
import { createTestingPinia } from '@pinia/testing';
import { useAuthStore } from '@/store/AuthStore';
import { createRouter, createWebHistory } from 'vue-router';
import { nextTick } from 'vue';

// ✅ Mock Axios correctly
vi.mock('axios', async () => {
  const actualAxios = await vi.importActual('axios');
  return {
    ...actualAxios,
    default: {
      create: vi.fn(() => ({
        post: vi.fn(),
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        },
        defaults: { headers: { common: {} } }
      }))
    }
  };
});

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/place-order', name: 'PlaceOrder' }],
});

describe('Login.vue', () => {
  let wrapper;
  let authStore;
  let mockAxios;

  beforeEach(async () => {
    // Retrieve the mockAxios instance
    mockAxios = axios.default.create();

    wrapper = mount(Login, {
      global: {
        plugins: [createTestingPinia(), router],
      },
    });

    authStore = useAuthStore();
    await nextTick(); // ✅ Wait for rendering
  });

  it('calls API and redirects on successful login', async () => {
    // ✅ Mock API response
    mockAxios.post.mockResolvedValue({
      status: 200,
      data: {
        access_token: 'test-token',
        refresh_token: 'refresh-test-token',
        user: { username: 'testuser' },
      },
    });

    const usernameInput = wrapper.find('[data-test="username"] input');
    const passwordInput = wrapper.find('[data-test="password"] input');

    expect(usernameInput.exists()).toBe(true);
    expect(passwordInput.exists()).toBe(true);

    await usernameInput.setValue('testuser');
    await passwordInput.setValue('password');

    await wrapper.find('button[type="submit"]').trigger('click');

    expect(mockAxios.post).toHaveBeenCalledWith('/api/login', {
      username: 'testuser',
      password: 'password',
    });

    expect(authStore.accessToken).toBe('test-token');
    await router.isReady();
    expect(wrapper.vm.$route.path).toBe('/place-order');
  });
});
