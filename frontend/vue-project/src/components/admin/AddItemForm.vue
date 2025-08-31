<template>
  <form @submit.prevent="handleSubmit" class="space-y-3">
    <!-- Nom -->
    <input
      v-model="nom"
      :placeholder="placeholder"
      class="border rounded px-3 py-2 w-full"
    />

    <!-- Description -->
    <textarea
      v-model="description"
      placeholder="Description"
      class="border rounded px-3 py-2 w-full"
    />

    <!-- Sélection du secteur -->
    <select
      v-model="secteurId"
      class="border rounded px-3 py-2 w-full bg-white"
    >
      <option disabled value="">Sélectionnez un secteur</option>
      <option
        v-for="secteur in secteurs"
        required
        :key="secteur.id"
        :value="secteur.id"
      >
        {{ secteur.nom }}
      </option>
    </select>

    <!-- Bouton -->
    <button class="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700">
      ➕ Ajouter
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  placeholder: String,
  secteurs: Array // ← liste des secteurs passée depuis le parent
})

const emit = defineEmits(['submit'])

const nom = ref('')
const description = ref('')
const secteurId = ref('')

function handleSubmit() {
  if (nom.value.trim() && secteurId.value) {
    emit('submit', {
      nom: nom.value.trim(),
      description: description.value.trim(),
      secteur_id: secteurId.value
    })
    nom.value = ''
    description.value = ''
    secteurId.value = ''
  }
console.log(secteurId.value)
}
</script>
