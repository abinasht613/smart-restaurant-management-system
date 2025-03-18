<script setup>
import { ref, onMounted } from "vue";
import { useSizeStore } from "@/store/item/sizeStore";
import { useToast } from "vue-toastification";

const sizeStore = useSizeStore();
const toast = useToast();

const dialog = ref(false);
const isEditing = ref(false);
const editedSize = ref({ id: null, sname: "" });

onMounted(() => {
  sizeStore.fetchSizes();
});

const openDialog = (size = null) => {
  isEditing.value = !!size;
  editedSize.value = size ? { ...size } : { id: null, sname: "" };
  dialog.value = true;
};

const saveSize = async () => {
  if (isEditing.value) {
    await sizeStore.updateSize(editedSize.value.id, editedSize.value);
    toast.success("Size updated successfully!");
  } else {
    await sizeStore.addSize(editedSize.value);
    toast.success("Size added successfully!");
  }
  dialog.value = false;
};

const removeSize = async (id) => {
  await sizeStore.deleteSize(id);
  toast.error("Size deleted!");
};
</script>

<template>
  <v-container>
    <v-btn color="primary" @click="openDialog()">Add Size</v-btn>

    <v-data-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Size Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="size in sizeStore.sizes" :key="size.id">
          <td>{{ size.id }}</td>
          <td>{{ size.sname }}</td>
          <td>
            <v-btn color="blue" variant="outlined" @click="openDialog(size)">Edit</v-btn>
            <v-btn color="red" variant="outlined" @click="removeSize(size.id)">Delete</v-btn>
          </td>
        </tr>
      </tbody>
    </v-data-table>

    <!-- Dialog for Create/Edit -->
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title>{{ isEditing ? "Edit Size" : "Add Size" }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="editedSize.sname" label="Size Name"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="gray" @click="dialog = false">Cancel</v-btn>
          <v-btn color="green" @click="saveSize">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
