import { defineStore } from "pinia";
import { ref } from 'vue';
import api from '@/api';

export const useSizeStore = defineStore("size", {
  state: () => ({
    sizes: [],
  }),

  actions: {
    async fetchSizes() {
      try {
        const response = await api.get("/sizes");
        this.sizes = response.data;
      } catch (error) {
        console.error("Error fetching sizes:", error);
      }
    },

    async addSize(size) {
      try {
        const response = await api.post("/sizes", size);
        let myresponse =  response.data;
        this.sizes.push({ id: myresponse.id, sname: myresponse.size });
      } catch (error) {
        console.error("Error adding size:", error);
      }
    },

    async updateSize(id, updatedSize) {
      try {
        await api.put(`/sizes/${id}`, updatedSize);
        const index = this.sizes.findIndex((size) => size.id === id);
        if (index !== -1) this.sizes[index] = updatedSize;
      } catch (error) {
        console.error("Error updating size:", error);
      }
    },

    async deleteSize(id) {
      try {
        await api.delete(`/sizes/${id}`);
        this.sizes = this.sizes.filter((size) => size.id !== id);
      } catch (error) {
        console.error("Error deleting size:", error);
      }
    },
  },
});
