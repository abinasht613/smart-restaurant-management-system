<script setup>
import { ref, onMounted } from "vue";
import { usetypeStore } from "@/store/item/typeStore";
import { useToast } from "vue-toastification";

const typeStore = usetypeStore();
const toast = useToast();

const dialog = ref(false);
const isEditing = ref(false);
const editedtype = ref({ id: null, sname: "" });

onMounted(() => {
  typeStore.fetchtypes();
});

const openDialog = (type = null) => {
  isEditing.value = !!type;
  editedtype.value = type ? { ...type } : { id: null, tname: "" };
  dialog.value = true;
};

const savetype = async () => {
  if (isEditing.value) {
    await typeStore.updatetype(editedtype.value.id, editedtype.value);
    toast.success("type updated successfully!");
  } else {
    await typeStore.addtype(editedtype.value);
    toast.success("type added successfully!");
  }
  dialog.value = false;
};

const removetype = async (id) => {
  await typeStore.deletetype(id);
  toast.error("type deleted!");
};
</script>

<template>
  <v-container>
    <v-btn color="primary" @click="openDialog()">Add type</v-btn>

    <v-data-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>type Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="type in typeStore.types" :key="type.id">
          <td>{{ type.id }}</td>
          <td>{{ type.tname }}</td>
          <td>
            <v-btn color="blue" variant="outlined" @click="openDialog(type)">Edit</v-btn>
            <v-btn color="red" variant="outlined" @click="removetype(type.id)">Delete</v-btn>
          </td>
        </tr>
      </tbody>
    </v-data-table>

    <!-- Dialog for Create/Edit -->
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title>{{ isEditing ? "Edit type" : "Add type" }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="editedtype.tname" label="type Name"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="gray" @click="dialog = false">Cancel</v-btn>
          <v-btn color="green" @click="savetype">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
