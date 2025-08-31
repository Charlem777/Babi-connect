<template>
  <div v-if="offres.length" class="mt-12">
    <h2 class="text-xl font-bold text-gray-800 mb-4">Suggestions pour vous</h2>
    <div class="overflow-x-auto hide-scrollbar">
      <div class="flex gap-6">
        <div
          v-for="offre in offres"
          :key="offre.id"
          class="min-w-[260px] max-w-[280px] bg-white rounded-xl shadow-sm relative"
        >
          <img
            :src="offre.image_url"
            alt="Image offre"
            class="h-40 w-full object-cover rounded-t-xl"
          />
          <div class="absolute top-2 left-2 bg-indigo-600 text-white text-xs px-2 py-1 rounded-full">
            Suggestion
          </div>
          <div class="p-4">
            <h3 class="text-sm font-semibold text-gray-900 truncate">{{ offre.titre }}</h3>
            <p class="text-xs text-gray-500">{{ offre.partenaire.nom }}</p>
            <div class="mt-2 text-xs text-gray-600">{{ offre.commune }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { api } from '@/api'

const props = defineProps({ secteurSlug: String })
const offres = ref([])

async function loadRecommandations() {
  if (!props.secteurSlug) return
  console.log("🔹 Chargement recommandations pour secteur:", props.secteurSlug)
  try {
    const { data } = await api.get(`/offres/recommandations?secteur=${props.secteurSlug}`)
    offres.value = data
    console.log("✅ Recommandations reçues:", offres.value)
  } catch (err) {
    console.error("❌ Erreur chargement recommandations:", err)
  }
}

onMounted(loadRecommandations)

// 🔥 Regarde si le slug change
watch(() => props.secteurSlug, (newSlug, oldSlug) => {
  console.log("🔄 Secteur changé:", oldSlug, "➡", newSlug)
  loadRecommandations()
})
</script>


<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
