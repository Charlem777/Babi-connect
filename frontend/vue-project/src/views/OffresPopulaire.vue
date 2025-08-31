<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import OffreCardAdapter from '@/components/OffreCardAdapter.vue'

const offres = ref([])

onMounted(async () => {
  try {
    const { data } = await api.get('/offres/populaires')
    offres.value = data
    console.log('pop:', offres.value)
  } catch (err) {
    console.error('Erreur chargement offres populaires :', err)
  }
})

</script>

<template>
  <section class="px-6 py-10">
    <h2 class="text-2xl font-bold mb-6 text-orange-700">🔥 Offres les plus aimées</h2>
    <div class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <OffreCardAdapter v-for="offre in offres" :key="offre.id" :offre="offre" />
    </div>
  </section>
</template>
