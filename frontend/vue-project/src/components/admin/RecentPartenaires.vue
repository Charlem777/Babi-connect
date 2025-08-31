<template>
  <section>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">Derniers Partenaires</h2>
      <RouterLink to="/admin/partenaires" class="text-sm text-orange-600 hover:underline">Voir tout</RouterLink>
    </div>
    <ul class="space-y-2">
      <li v-for="p in partenaires" :key="p.id" class="bg-white p-4 rounded shadow flex items-center gap-4">
        <img :src="p.logo" alt="Logo" class="w-12 h-12 rounded-full object-cover" v-if="p.logo" />
        <div>
          <h3 class="font-semibold text-gray-800">{{ p.nom }}</h3>
          <p class="text-sm text-gray-500">
            {{ p.ville }} — <span class="font-medium">{{ p.secteur?.nom || 'Secteur inconnu' }}</span><br>
            Catégorie : <span class="italic">{{ p.categorie?.nom || 'N/A' }}</span>
          </p>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const partenaires = ref([])

onMounted(async () => {
  const { data } = await api.get('/admin/partenaires/recent')
  partenaires.value = data
})
</script>
