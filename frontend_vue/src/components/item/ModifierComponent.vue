<script setup>
import { ref, onMounted } from "vue";
import { usemodifierStore } from "@/store/item/modifierStore";
import { useToast } from "vue-toastification";

const modifierStore = usemodifierStore();
const toast = useToast();

const dialog = ref(false);
const isEditing = ref(false);
const editedmodifier = ref({ id: null, mname: "", price: 0 });

onMounted(() => {
  modifierStore.fetchmodifiers();
});

const openDialog = (modifier = null) => {
  isEditing.value = !!modifier;
  editedmodifier.value = modifier ? { ...modifier } : { id: null, mname: "", price: 0 };
  dialog.value = true;
};

const savemodifier = async () => {
  if (isEditing.value) {
    await modifierStore.updatemodifier(editedmodifier.value.id, editedmodifier.value);
    toast.success("modifier updated successfully!");
  } else {
    await modifierStore.addmodifier(editedmodifier.value);
    toast.success("modifier added successfully!");
  }
  dialog.value = false;
};

const removemodifier = async (id) => {
  await modifierStore.deletemodifier(id);
  toast.error("modifier deleted!");
};
</script>

<template>
  <v-container>
    <v-btn color="primary" @click="openDialog()">Add modifier</v-btn>

    <v-data-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="modifier in modifierStore.modifiers" :key="modifier.id">
          <td>{{ modifier.id }}</td>
          <td>{{ modifier.mname }}</td>
          <td>{{ modifier.price }}</td>
          <td>
            <v-btn color="blue" variant="outlined" @click="openDialog(modifier)">Edit</v-btn>
            <v-btn color="red" variant="outlined" @click="removemodifier(modifier.id)">Delete</v-btn>
          </td>
        </tr>
      </tbody>
    </v-data-table>

    <!-- Dialog for Create/Edit -->
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title>{{ isEditing ? "Edit modifier" : "Add modifier" }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="editedmodifier.mname" label="modifier Name"></v-text-field>
        </v-card-text>
        <v-card-text>
          Price
          <v-text-field v-model="editedmodifier.price" label="modifier Price"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="gray" @click="dialog = false">Cancel</v-btn>
          <v-btn color="green" @click="savemodifier">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
