<template>
  <section class="py-16 bg-gray-50">
    <div class="text-center mb-10">
      <h2 class="text-3xl font-bold text-indigo-700">Nos partenaires locaux</h2>
      <p class="text-gray-600 mt-2">Des professionnels passionnés qui enrichissent Abidjan</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 px-6 max-w-6xl mx-auto">
      <div
        v-for="partner in partners"
        :key="partner.id"
        :class="[
          'relative p-6 flex flex-col items-center text-center rounded-xl transition-all duration-300',
          partner.premium
            ? 'bg-white/70 backdrop-blur-md border border-yellow-300 shadow-xl hover:shadow-2xl hover:-translate-y-1'
            : 'bg-white border border-gray-200 shadow-sm hover:shadow-md'
        ]"
      >
        <!-- Badge -->
        <div
          :class="[
            'absolute top-4 right-4 flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold shadow-sm',
            partner.premium ? 'bg-yellow-400 text-white premium-glow' : 'bg-gray-300 text-gray-800'
          ]"
        >
          <span v-if="partner.premium">⭐</span>
          <span v-else>🧊</span>
          <span>{{ partner.type }}</span>
        </div>

        <!-- Avatar -->
        <img
          :src="partner.image"
          :alt="partner.name"
          class="w-20 h-20 rounded-full mb-4 object-cover border-4"
          :class="partner.premium ? 'border-yellow-200' : 'border-gray-100'"
        />

        <!-- Infos -->
        <h3 class="text-lg font-semibold text-gray-800">{{ partner.name }}</h3>
        <p class="text-sm text-indigo-600 font-medium mb-1">{{ partner.category }}</p>
        <p class="text-sm text-gray-500 leading-relaxed">{{ partner.description }}</p>

        <!-- CTA -->
        <router-link
          :to="`/partenaires/${partner.slug}`"
          class="mt-4 inline-block bg-indigo-50 text-indigo-700 px-4 py-2 rounded-full text-sm font-medium hover:bg-indigo-100 transition"
        >
          Voir le profil
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const partners = ref([])

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5000/api/partenaires-actifs')
    const data = await res.json()
    partners.value = data.map(p => ({
      id: p.id,
      name: p.nom,
      description: p.description,
      category: p.secteur,
      image: p.logo || '/assets/partners/default.png',
      slug: p.nom.toLowerCase().replace(/\s+/g, '-'),
      premium: p.statut === 'premium',
      type: p.statut
    }))
  } catch (err) {
    console.error('Erreur API :', err)
  }
})

</script>

<style scoped>
.premium-glow {
  animation: glow 2s infinite ease-in-out;
}

@keyframes glow {
  0% { box-shadow: 0 0 0px rgba(255, 193, 7, 0.4); }
  50% { box-shadow: 0 0 8px rgba(255, 193, 7, 0.6); }
  100% { box-shadow: 0 0 0px rgba(255, 193, 7, 0.4); }
}
</style>
