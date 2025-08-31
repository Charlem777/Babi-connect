<template>
  <section>
      <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">Derniers Offres</h2>
      <RouterLink to="/admin/offres" class="text-sm text-orange-600 hover:underline">Voir tout</RouterLink>
    </div>
    
    <ul class="space-y-2">
      <li v-for="offre in offres" :key="offre.id" class="bg-white p-4 rounded shadow">
        <h3 class="font-semibold">{{ offre.titre }}</h3>
        <p class="text-sm text-gray-500">{{ offre.partenaire.nom }} — {{ offre.ville }}</p>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const offres = ref([])

onMounted(async () => {
  const { data } = await api.get('/admin/offres/recentes')
  offres.value = data
})
</script>
