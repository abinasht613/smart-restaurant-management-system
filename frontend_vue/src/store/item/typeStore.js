import { defineStore } from "pinia";
import { ref } from 'vue';
import api from '@/api';

export const usetypeStore = defineStore("type", {
  state: () => ({
    types: [],
  }),

  actions: {
    async fetchtypes() {
      try {
        const response = await api.get("/types");
        this.types = response.data;
      } catch (error) {
        console.error("Error fetching types:", error);
      }
    },

    async addtype(type) {
      try {
        const response = await api.post("/types", type);
        let myresponse =  response.data;
        this.types.push({ id: myresponse.id, tname: myresponse.type });
      } catch (error) {
        console.error("Error adding type:", error);
      }
    },

    async updatetype(id, updatedtype) {
      try {
        await api.put(`/types/${id}`, updatedtype);
        const index = this.types.findIndex((type) => type.id === id);
        if (index !== -1) this.types[index] = updatedtype;
      } catch (error) {
        console.error("Error updating type:", error);
      }
    },

    async deletetype(id) {
      try {
        await api.delete(`/types/${id}`);
        this.types = this.types.filter((type) => type.id !== id);
      } catch (error) {
        console.error("Error deleting type:", error);
      }
    },
  },
});
