<template>
  

<header
    class="relative text-white px-4 py-6"
    :style="{ backgroundImage: `url(${bgPattern})` }"
  >
    <!-- Overlay foncé pour améliorer la lisibilité -->
    <div class="absolute inset-0 bg-black/20"></div>

    <!-- Contenu -->
    <div class="relative z-10 flex flex-col items-center">
      <!-- Titre -->
      <h1 class="text-5xl font-bold ">
        <span class="text-white">Babi</span>
        <span class="text-yellow-400">Connect</span>
      </h1>    
    </div>
     <div v-if="route.path === '/offres'" class="w-full max-w-xl mt-6">
        <SectorCategorySelect @change="onBannerFiltersChange" />

      </div>
     <form
    @submit.prevent="onSearch"
    class="max-w-md mx-auto mt-10"
  >
    <label
      for="default-search"
      class="mb-2 text-sm font-medium text-gray-900 sr-only"
    >
      Search
    </label>
    <div class="relative">
      <!-- Icône loupe -->
      <div
        class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none"
      >
        <svg
          class="w-4 h-4 text-white"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 20 20"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
          />
        </svg>
      </div>

      <!-- Input -->
      <input
        v-model="search"
        type="search"
        id="default-search"
        class="block w-full p-4 ps-10 text-sm text-white border border-orange-500 rounded-lg bg-orange-500 placeholder-white focus:ring-orange-600 focus:border-orange-600"
        placeholder="Rechercher..."
        required
      />

      <!-- Bouton -->
      <button
        type="submit"
        class="text-white absolute end-2.5 bottom-2.5 bg-orange-600 hover:bg-orange-700 focus:ring-4 focus:outline-none focus:ring-orange-300 font-medium rounded-lg text-sm px-4 py-2"
      >
        Rechercher
      </button>
    </div>
  </form>
  </header>

  <!-- Contenu principal -->
  <main class="flex-grow px-4 sm:px-6 py-6">
    <slot />
  </main>

  <!-- Footer -->
  <footer class="bg-white border-t p-4 text-center text-xs sm:text-sm text-gray-500"  >
    © 2025 BABI CONNECT • Tous droits réservés
  </footer>
  <BottomNav/>
</template>

<script setup>
import { createRouter, createWebHistory,useRoute } from 'vue-router'
import Accueil from '@/views/Home.vue'
import Partenaires from '@/views/PartenairesView.vue'
import Offres from '@/views/OffresView.vue'
import Filtres from '@/views/FiltresView.vue'
import { ref,onMounted,watch } from 'vue'
import BottomNav from '../BottomNav.vue'
// Import de l'image depuis assets
import bgPattern from "@/assets/bground.jpg"
import SectorCategorySelect from '../SectorCategorySelect.vue'
const tabs = [
  { name: 'A ', route: '/' },
  { name: 'Partenaires', route: '/partenaires' },
  { name: 'Offres', route: '/offres' },
  { name: 'Filtres', route: '/filtres' }
]


const routes = [
  { path: '/', component: Accueil },
  { path: '/partenaires', component: Partenaires },
  { path: '/offres', component: Offres },
  { path: '/filtres', component: Filtres }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      showSearch.value = false
    }
  })
})

const showSearch = ref(false)

function toggleSearch() {
  showSearch.value = !showSearch.value
}
function onBannerFiltersChange(payload) {
  const nextQuery = {
    secteur_slug: payload?.secteur_slug || undefined,
    categorie_slug: payload?.categorie_slug || undefined,
  }
  router.replace({ path: route.path, query: nextQuery })
}

const route = useRoute()
const bannerFilters = ref({
  secteur_slug: route.query.secteur_slug ?? null,
  categorie_slug: route.query.categorie_slug ?? null,
})

// si l’URL change (ex: back/forward), on met à jour l’UI
watch(
  () => route.query,
  (q) => {
    bannerFilters.value = {
      secteur_slug: q.secteur_slug ?? null,
      categorie_slug: q.categorie_slug ?? null,
    }
  }
)
</script>



<style scoped>
/* Masquer la scrollbar pour un look clean */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
