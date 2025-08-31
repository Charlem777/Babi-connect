<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">💬 Avis reçus</h1>

    <div v-if="avis.length === 0" class="text-gray-500 italic">Aucun avis pour le moment.</div>

    <div
      v-for="a in avis"
      :key="a.id"
      class="bg-white rounded shadow p-4 space-y-2 hover:shadow-md transition"
    >
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-600">🗓️ {{ formatDate(a.date) }}</span>
        <span class="text-yellow-500 font-bold text-lg">★ {{ a.note }}</span>
      </div>
      <p class="text-gray-700 text-sm">{{ a.commentaire }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const avis = ref([])

onMounted(async () => {
  const { data } = await api.get('/partenaire/avis')
  avis.value = data
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
