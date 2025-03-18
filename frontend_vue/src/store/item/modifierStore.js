import { defineStore } from "pinia";
import { ref } from 'vue';
import api from '@/api';

export const usemodifierStore = defineStore("modifier", {
  state: () => ({
    modifiers: [],
  }),

  actions: {
    async fetchmodifiers() {
      try {
        const response = await api.get("/modifiers");
        this.modifiers = response.data;
      } catch (error) {
        console.error("Error fetching modifiers:", error);
      }
    },

    async addmodifier(modifier) {
      try {
        const response = await api.post("/modifiers", modifier);
        let myresponse =  response.data;
        this.modifiers.push({ id: myresponse.modifier.id, mname: myresponse.modifier.name, price: myresponse.modifier.price });
      } catch (error) {
        console.error("Error adding modifier:", error);
      }
    },

    async updatemodifier(id, updatedmodifier) {
      try {
        await api.put(`/modifiers/${id}`, updatedmodifier);
        const index = this.modifiers.findIndex((modifier) => modifier.id === id);
        if (index !== -1) this.modifiers[index] = updatedmodifier;
      } catch (error) {
        console.error("Error updating modifier:", error);
      }
    },

    async deletemodifier(id) {
      try {
        await api.delete(`/modifiers/${id}`);
        this.modifiers = this.modifiers.filter((modifier) => modifier.id !== id);
      } catch (error) {
        console.error("Error deleting modifier:", error);
      }
    },
  },
});
