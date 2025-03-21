<template>
  <v-container>
  <v-card class="pa-5" max-width="600px">
    <v-card-title class="text-h5">Add New Item</v-card-title>
    <v-form @submit.prevent="submitItem">
      <v-text-field
        v-model="item.iname"
        label="Item Name"
        outlined
        required
      ></v-text-field>

      <v-divider class="my-4"></v-divider>

      <v-card-subtitle class="text-subtitle-1">Variants</v-card-subtitle>

      <v-row v-for="(variant, index) in item.variants" :key="index">
        <v-col cols="3">
          <v-select
            v-model="variant.size_id"
            :items="sizes"
            item-value="id"
            item-title="sname"
            label="Size"
            outlined
            required
          ></v-select>
        </v-col>
        <v-col cols="3">
          <v-select
            v-model="variant.type_id"
            :items="types"
            item-value="id"
            item-title="tname"
            label="Type"
            outlined
          ></v-select>
        </v-col>
        <v-col cols="2">
          <v-text-field
            v-model.number="variant.price"
            type="number"
            label="Price"
            outlined
            required
          ></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field
            v-model.number="variant.qty"
            type="number"
            label="Stock"
            outlined
            required
          ></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-btn color="error" icon @click="removeVariant(index)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-btn color="primary" @click="addVariant">+ Add Variant</v-btn>

      <v-divider class="my-4"></v-divider>

      <v-btn color="success" type="submit">Save Item</v-btn>
    </v-form>
  </v-card>
</v-container>

</template>

<script>
import { ref, onMounted } from "vue";
import api from '@/api';
import { useToast } from "vue-toastification";

export default {
  setup() {
    const item = ref({
      iname: "",
      variants: [],
    });

    const sizes = ref([]);
    const types = ref([]);
    const toast = useToast();
    const fetchSizes = async () => {
      try {
        const response = await api.get("/sizes");
        sizes.value = response.data;
      } catch (error) {
        console.error("Error fetching sizes:", error);
      }
    };

    const fetchTypes = async () => {
      try {
        const response = await api.get("/types");
        types.value = response.data;
      } catch (error) {
        console.error("Error fetching types:", error);
      }
    };

    const addVariant = () => {
      item.value.variants.push({ size_id: null, type_id: null, price: 0, qty: 0 });
    };

    const removeVariant = (index) => {
      item.value.variants.splice(index, 1);
    };

    const submitItem = async () => {
      try {
        const response = await api.post("/item-and-item-details", item.value);
        // alert(response.data.message);
        resetForm();
        toast.success("Item saved successfully!");
      } catch (error) {
        console.error("Error saving item:", error);
        // alert("Failed to save item.");
        if (error.status === 400) {
          console.log("catch error");
          console.log(error.response.data.error);
          // alert(error.response.data.error);
          toast.error(error.response.data.error)
        }
      }
    };

    const resetForm = () => {
      item.value = { iname: "", variants: [] };
    };

    onMounted(() => {
      fetchSizes();
      fetchTypes();
    });

    return {
      item,
      sizes,
      types,
      addVariant,
      removeVariant,
      submitItem,
    };
  },
};
</script>

<style scoped>
.v-container {
  max-width: 600px;
}
</style>
