<template>
    <div>
        <h2>Order</h2>
        <form @submit.prevent="handleSubmit">
            
            Customer Name: <input type="text" v-model="newOrder.customer_name" name="customer_name">
            Customer Phone: <input type="text" v-model="newOrder.customer_mobile" name="customer_mobile" required>

            Input Order: <input type="text" v-model="newOrder.order_text" name="order_text" class="order-input" 
             autocomplete="off" required>
            <!-- Speech-to-Text Button -->
            <v-btn color="primary" @click="startSpeechRecognition">
              🎤 Speak
            </v-btn>
            <div v-if="orderStore.error">{{ orderStore.error }}</div>
            <button v-if="authStore.isAuthenticated" @click="placeNewOrder">Place Order</button>

            <div v-if="orderStore.loading">Loading...</div>
                

        <div class="imgcontainer">
            <!-- <img src="img_avatar2.png" alt="Avatar" class="avatar"> -->
        </div>
        </form>

        <!-- Open Menu Button -->
        <!-- <v-btn color="primary" ref="menuButton"> Show Suggestions </v-btn> -->

        <!-- Popup Menu -->
        <v-menu v-model="menu" :close-on-content-click="false" activator="parent">
          <v-card>
            <v-list>
              <v-list-item v-for="(correctWord, wrongWord) in corrections" :key="wrongWord">
                <v-list-item-title>
                  <strong>{{ wrongWord }}</strong> → <span style="color: green">{{ correctWord }}</span>
                </v-list-item-title>

                <template v-slot:append>
                  <v-icon color="green" @click="replaceWord(wrongWord, correctWord)">mdi-check</v-icon>
                  <v-icon color="red" @click="removeCorrection(wrongWord)">mdi-close</v-icon>
                </template>
              </v-list-item>
            </v-list>


            <h3>Size Missing</h3>
            <v-list>
              <v-list-item v-for="(sizes, item) in sizeMissingMap" :key="item">
                <v-list-item-content>
                  <v-list-item-title>
                    {{ item }} → 
                    <span 
                      v-for="size in sizes" 
                      :key="size" 
                      @click="replaceItemWithSize(item, size)" 
                      class="size-pill">
                      {{ size }}
                    </span>
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>  

          </v-card>
        </v-menu>

    </div>
</template>
<script setup>
import { ref,onMounted, computed } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { useOrderStore } from '@/store/order/OrderStore';
import { useToast } from "vue-toastification";

const menu = ref(false);
const corrections = ref({});
const sizeMissing = ref([]);

const authStore = useAuthStore();
const orderStore = useOrderStore();
const toast = useToast();

onMounted(() => {
  if (authStore.isAuthenticated) {
    // console.log(authStore.isAuthenticated)
    // console.log(authStore.accessToken)
    // console.log(authStore.refreshToken)
    // console.log(authStore.user)
    // console.log("Stored Token:", JSON.stringify(authStore.accessToken, null, 2));
    // orderStore.fetchOrders();
    console.log("Access Token:", authStore.accessToken);
    console.log("auth-user",authStore.user);
  }
});

const newOrder = ref({
    // order_text: "Two large chicken pepperoni pizzas extra cheese, one caesar salad, and two diet kok",
    order_text: "",
    "customer_mobile":"N/A",
    "customer_name":"N/A"
});


// Convert API response to a usable map
const sizeMissingMap = computed(() => {
  let map = {};
  sizeMissing.value.forEach(obj => {
    const key = Object.keys(obj)[0]; // Extract item name
    map[key] = obj[key]; // Assign sizes
  });
  return map;
});

async function placeNewOrder () {
  const response  = await orderStore.placeOrder(newOrder.value);
  console.log("my res",response);

  if (response.error){
    console.log(response.error);
    const correctionArray = response.invalid_words; // Extract `invalid_words`
    // Convert [{ wrong: right }, { wrong: right }] into { wrong: right }
    corrections.value = correctionArray.reduce((acc, obj) => {
      const wrongWord = Object.keys(obj)[0]; // Extract key (wrong word)
      const correctWord = obj[wrongWord]; // Extract value (correct word)
      acc[wrongWord] = correctWord;
      return acc;
    }, {});

    sizeMissing.value = response.size_missing;

    menu.value = true; // Open menu after fetching
  }

};


// Replace incorrect word in input
const replaceWord = (wrongWord, correctWord) => {
  console.log("Replace", wrongWord, "with", correctWord, "in", newOrder.value.order_text);
  newOrder.value.order_text = newOrder.value.order_text.replace(new RegExp(`${wrongWord}`, "gi"), correctWord);
  // newOrder.value.order_text = newOrder.value.order_text.replace(new RegExp(`\\b${wrongWord}\\b`, "gi"), correctWord);
  removeCorrection(wrongWord)
};

// Remove correction from the menu
const removeCorrection = (wrongWord) => {
  delete corrections.value[wrongWord];
};

// Function to replace item with selected size
const replaceItemWithSize = (item, size) => {
  console.log(`Replacing ${item} with ${size} ${item}`);
  newOrder.value.order_text = newOrder.value.order_text.replace(new RegExp(`\\b${item}\\b`, "gi"), `${size} ${item}`);

  // Remove from missing size list
  sizeMissing.value = sizeMissing.value.filter(obj => !obj[item]);
};

// Speech-to-Text Function
const startSpeechRecognition = () => {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      
      if (!SpeechRecognition) {
        alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onresult = (event) => {
        // newOrder.value.order_text += event.results[0][0].transcript;
        newOrder.value.order_text += (newOrder.value.order_text ? ' ' : '') + event.results[0][0].transcript; // Append to existing value
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        alert(`Speech recognition error: ${event.error}`);
      };

      recognition.start();
    };

    const submitOrder = async () => {
      console.log('Order Submitted:', orderInput.value);
      alert(`Order Submitted: ${orderInput.value}`);
    };

</script>

<style>
.order-input {
  width: 100%;
  height: 100px; /* Adjust as needed */
  padding: 10px;
  font-size: 16px;
}

.size-pill {
  display: inline-block;
  padding: 6px 12px;
  margin: 4px;
  background-color: #1976D2;
  color: white;
  border-radius: 15px; /* Pill shape */
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.size-pill:hover {
  background-color: #1565C0;
}

</style>
