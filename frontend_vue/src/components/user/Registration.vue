<template>
  <v-container class="d-flex justify-center align-center" style="height: 100vh;">
    <v-card class="pa-5" width="400">
      <v-card-title class="text-center text-h5">Register</v-card-title>

      <v-form @submit.prevent="handleSubmit">
        <v-text-field 
          v-model="form.fname"
          label="First Name"
          outlined
          required
        ></v-text-field>

        <v-text-field 
          v-model="form.lname"
          label="Last Name"
          outlined
          required
        ></v-text-field>

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

        <v-select
          v-model="form.role"
          label="Select Role"
          :items="['Chef', 'Cashier', 'Manager', 'Waiter']"
          outlined
          required
        ></v-select>

        <v-btn type="submit" color="primary" block class="mt-3">Register</v-btn>

        <v-btn color="error" block class="mt-2" @click="clearForm">Cancel</v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>
<script setup>

import {reactive} from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';

const form = reactive({
    fname: '',
    lname: '',
    uname: '',
    psw: '',
    role: 'manager',
});

const toast = useToast();

const handleSubmit = async() => {
  const newForm = {
    fname: form.fname,
    lname: form.lname,
    username: form.uname,
    password: form.psw,
    role: form.role,
  }
  // console.log(newForm);

  try {
    if(!form.fname || !form.lname || !form.uname || !form.psw) {
      toast.error('Please fill all fields');
      return;
    }
    const response = await axios.post('api/register', newForm);
    if (response.status === 201) {
      console.log("201");
    }
  }
  catch (error) {
    if (error.status === 401) {
      console.log("catch error");
      console.log(error.response.data.message);
      alert(error.response.data.message);
    }
  }

}

</script>
<style>
body {font-family: Arial, Helvetica, sans-serif;}
form {border: 3px solid #f1f1f1;}

input[type=text], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

button {
  background-color: #04AA6D;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}

button:hover {
  opacity: 0.8;
}

.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;
}

.imgcontainer {
  text-align: center;
  margin: 24px 0 12px 0;
}

img.avatar {
  width: 40%;
  border-radius: 50%;
}

.container {
  padding: 16px;
}

span.psw {
  float: right;
  padding-top: 16px;
}

/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
  span.psw {
     display: block;
     float: none;
  }
  .cancelbtn {
     width: 100%;
  }
}
</style>