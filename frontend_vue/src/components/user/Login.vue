<template>
  <v-container class="d-flex justify-center align-center" style="height: 100vh;">
    <v-card class="pa-5" width="400">
      <v-card-title class="text-center text-h5">Login</v-card-title>

      <v-form @submit.prevent="handleSubmit">
        <v-text-field 
          v-model="form.uname"
          label="Username"
          outlined
          required
        ></v-text-field>

        <v-text-field 
          v-model="form.psw"
          label="Password"
          type="password"
          outlined
          required
        ></v-text-field>

        <v-checkbox v-model="rememberMe" label="Remember me"></v-checkbox>

        <v-btn type="submit" color="primary" block class="mt-3">Login</v-btn>

        <v-btn color="error" block class="mt-2" @click="clearForm">Cancel</v-btn>

        <v-card-text class="text-center mt-3">
          <a href="#">Forgot password?</a>
        </v-card-text>
      </v-form>
    </v-card>
  </v-container>
</template>
<script setup>
import axios from 'axios';
import { reactive } from 'vue';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/store/AuthStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const form = reactive({
    uname: '',
    psw: '',
});

const toast = useToast();

const handleSubmit = async () => {
    const formData = {
        username: form.uname,
        password: form.psw,
    };
    try {
        if (!form.uname || !form.psw) {
            toast.error('Please fill all fields');
            return;
        }
        const response = await axios.post('api/login', formData);
        if (response.status === 200) {
            // console.log(response.data.access_token);
            // console.log(response.data.refresh_token);
            toast.success('Login Successfully');
            // ✅ Store tokens after successful logi
            authStore.setTokens({
                access: response.data.access_token,
                refresh: response.data.refresh_token,
                user: response.data.user,
            });
            // console.log(response.data.access_token);
            // console.log(response.data.refresh_token);
            console.log("Access Token:", authStore.accessToken);
            console.log("auth-user",authStore.user);

            // ✅ Redirect to dashboard
            setTimeout(() => {
                router.push('/place-order'); // ✅ Force navigation
            }, 100); // Small delay to ensure state updates
        }
        
    }
    catch (error) {
        if (error.status === 401) {
            console.log("catch error");
            console.log(error.response.data.message);
            // alert(error.response.data.message);
            toast.error(error.response.data.message);
            // toast.error("Invalid");
        }
    }
};

</script>
<style>


</style>