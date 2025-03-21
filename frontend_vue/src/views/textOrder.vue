<template>
    <v-container>
      <!-- Order Input Field -->
      <v-text-field
        v-model="orderInput"
        label="Enter your order or use voice input"
        @input="handleInput"
        autocomplete="off"
      ></v-text-field>
  
      <!-- Speech-to-Text Button -->
      <v-btn color="primary" @click="startSpeechRecognition">
        🎤 Speak
      </v-btn>
  
      <!-- Suggestions List -->
      <v-list v-if="suggestions.length">
        <v-list-item
          v-for="(suggestion, index) in suggestions"
          :key="index"
          @click="applyCorrection(suggestion)"
        >
          {{ suggestion }}
        </v-list-item>
      </v-list>
  
      <!-- Submit Button -->
      <v-btn color="success" @click="submitOrder">Submit Order</v-btn>
    </v-container>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useMenuStore } from '@/store/menuNameStore';
  import Fuse from 'fuse.js';
  
  export default {
    setup() {
      const orderInput = ref('');
      const menuStore = useMenuStore();
      const suggestions = ref([]);
      let fuse = null;
  
      // Fetch menu on mount
      onMounted(async () => {
        await menuStore.fetchMenu();
        fuse = new Fuse(menuStore.menuItems, { includeScore: true, threshold: 0.4 });
      });
  
      // Speech-to-Text Function
      const startSpeechRecognition = () => {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
  
        recognition.onresult = (event) => {
          orderInput.value = event.results[0][0].transcript;
          handleInput(); // Auto-correct after speech input
        };
  
        recognition.onerror = (event) => {
          console.error('Speech recognition error:', event);
        };
  
        recognition.start();
      };
  
      // Auto-correct and suggest words
      const handleInput = () => {
        if (!fuse) return;
  
        const words = orderInput.value.split(' ');
        const correctedWords = words.map(word => {
          const result = fuse.search(word);
          return result.length > 0 ? result[0].item : word;
        });
  
        orderInput.value = correctedWords.join(' ');
  
        // Show suggestions only for incorrect words
        suggestions.value = correctedWords
          .filter(word => !menuStore.menuItems.includes(word))
          .map(word => `Did you mean: ${word}?`);
      };
  
      const applyCorrection = (suggestion) => {
        orderInput.value = suggestion.replace('Did you mean: ', '');
        suggestions.value = [];
      };
  
      const submitOrder = async () => {
        
      };
  
      return { orderInput, suggestions, handleInput, applyCorrection, startSpeechRecognition, submitOrder };
    }
  };
  </script>
  