<template>
    <div>
        <h2>Login Form</h2>
        <form @submit.prevent="handleSubmit">
        <div class="imgcontainer">
            <!-- <img src="img_avatar2.png" alt="Avatar" class="avatar"> -->
        </div>

        <div class="container">
            <label for="fname"><b>First Name</b></label>
            <input type="text" placeholder="Enter First Name" name="fname" v-model="form.fname" required>

            <label for="lname"><b>Last Name</b></label>
            <input type="text" placeholder="Enter Last Name" name="lname" v-model="form.lname" required>

            <label for="uname"><b>Username</b></label>
            <input type="text" placeholder="Enter Username" name="uname" v-model="form.uname" required>

            <label for="psw"><b>Password</b></label>
            <input type="password" placeholder="Enter Password" name="psw" v-model="form.psw" required>

            <label for="userrole"><b>Role</b></label>
            <select name="role" id="userrole" v-model="form.role" required>
              <option value="chef">Chef</option>
              <option value="cashier">Cashier</option>
              <option value="manager">Manager</option>
              <option value="waiter">Waiter</option>
            </select>
                
            <button type="submit">Register</button>
        </div>
        </form>

        

    </div>
</template>
<script setup>

import {reactive} from 'vue';
import axios from 'axios';

const form = reactive({
    fname: '',
    lname: '',
    uname: '',
    psw: '',
    role: 'manager',
});

const handleSubmit = async() => {
  const newForm = {
    fname: form.fname,
    lname: form.lname,
    username: form.uname,
    password: form.psw,
    role: form.role,
  }
  console.log(newForm);

  try {
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