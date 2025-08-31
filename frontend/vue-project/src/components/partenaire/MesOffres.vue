<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">📦 Mes offres</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="offre in offres"
        :key="offre.id"
        class="bg-white rounded shadow p-4 space-y-2 hover:shadow-lg transition"
      >
        <img
          v-if="offre.image_banniere"
          :src="`http://localhost:5000${offre.image_banniere}`"
          class="w-full h-40 object-cover rounded"
          alt="Bannière"
        />
        <h2 class="text-lg font-semibold text-gray-800">{{ offre.titre }}</h2>
        <p class="text-sm text-gray-500">{{ offre.description }}</p>
        <div class="text-sm text-gray-600">📍 {{ offre.ville }} - {{ offre.commune }}</div>
        <div class="flex justify-between items-center text-xs text-gray-500 mt-2">
          <span>👁️ {{ offre.vues }} vues</span>
          <span>❤️ {{ offre.favoris_count }} favoris</span>
        </div>
        <div class="flex gap-2 mt-3">
          <button @click="edit(offre.id)" class="text-blue-600 hover:underline">Modifier</button>
          <button @click="supprimer(offre.id)" class="text-red-600 hover:underline">Supprimer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const offres = ref([])
const router = useRouter()

onMounted(async () => {
  const { data } = await api.get('/partenaire/offres')
  offres.value = data
  console.log("🔍 Offres:", offres.value)
})

function edit(id) {
  router.push(`/partenaire/offres/${id}`)
}

async function supprimer(id) {
  if (confirm("Supprimer cette offre ?")) {
    await api.delete(`/partenaire/offres/${id}`)
    offres.value = offres.value.filter(o => o.id !== id)
  }
}
</script>
