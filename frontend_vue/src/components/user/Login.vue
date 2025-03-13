<template>
    <div>
        <h2>Login Form</h2>
        <form @submit.prevent="handleSubmit">
        <div class="imgcontainer">
            <!-- <img src="img_avatar2.png" alt="Avatar" class="avatar"> -->
        </div>

        <div class="container">
            <label for="uname"><b>Username</b></label>
            <input type="text" placeholder="Enter Username" v-model="form.uname" name="uname" required>

            <label for="psw"><b>Password</b></label>
            <input type="password" placeholder="Enter Password" v-model="form.psw" name="psw" required>
                
            <button type="submit">Login</button>
            <label>
            <input type="checkbox" checked="checked" name="remember"> Remember me
            </label>
        </div>

        <div class="container" style="background-color:#f1f1f1">
            <button type="button" class="cancelbtn">Cancel</button>
            <span class="psw">Forgot <a href="#">password?</a></span>
        </div>
        </form>

        

    </div>
</template>
<script setup>
import axios from 'axios';
import { reactive } from 'vue';
import { useToast } from 'vue-toastification';

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
        const response = await axios.post('api/login', formData);
        if (response.status === 200) {
            console.log("200");
            toast.success('Login Successfully');
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