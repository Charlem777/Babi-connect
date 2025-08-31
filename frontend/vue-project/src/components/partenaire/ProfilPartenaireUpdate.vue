<template>
  <div class="p-6 max-w-3xl mx-auto space-y-8 bg-white rounded-xl shadow-md">
    <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
      🖊️ Modifier mon profil
    </h1>

    <form @submit.prevent="submit" class="space-y-6">
      <!-- Nom -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Nom du partenaire</label>
        <input
          v-model="profil.nom"
          class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
          placeholder="Nom du partenaire"
          required
        />
      </div>

      <!-- Description -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
        <textarea
          v-model="profil.description"
          class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
          placeholder="Description"
          rows="4"
        />
      </div>

      <!-- Localisation -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ville</label>
          <input
            v-model="profil.ville"
            class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
            placeholder="Ville"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Commune</label>
          <input
            v-model="profil.commune"
            class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
            placeholder="Commune"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Localisation précise</label>
          <input
            v-model="profil.localisation"
            class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
            placeholder="Ex: Rue 12, Quartier X"
          />
        </div>
      </div>

      <!-- URL -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Site web ou lien externe</label>
        <input
          v-model="profil.url"
          class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
          placeholder="https://..."
        />
      </div>

      <!-- Logo -->
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">Logo</label>
        <input
          type="file"
          @change="handleUpload"
          class="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-orange-100 file:text-orange-700 hover:file:bg-orange-200"
        />
        <img
          v-if="profil.logo"
          :src="'http://localhost:5000/' + profil.logo"
          alt="Logo partenaire"
          class="w-20 h-20 object-cover rounded-full border shadow"
        />
      </div>

      <!-- Bouton -->
      <button
        type="submit"
        class="bg-orange-500 text-white py-2 px-6 rounded-md hover:bg-orange-600 transition w-full md:w-auto"
      >
        💾 Sauvegarder
      </button>

      <!-- Message -->
      <p v-if="message" class="text-green-600 text-sm text-center">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const profil = ref({})
const message = ref('')

onMounted(async () => {
  const { data } = await api.get('/partenaire/me')
  profil.value = data
  console.log(profil.value)

})

async function handleUpload(e) {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('image', file)

  const { data } = await api.post('/partenaire/upload/logo-partenaire', formData)
  profil.value.logo = data.url
}

async function submit() {
  await api.put('/partenaire/me', profil.value)
  message.value = "✅ Profil mis à jour avec succès"
  console.log(profil.value)
  setTimeout(() => (message.value = ""), 3000)
}
</script>
