<template>
  <div class="relative w-full">
    <!-- Icône de recherche -->
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <!-- Input de recherche -->
    <input
      v-model="query"
      @input="debouncedFetch"
      @focus="show = true"
      @blur="hide"
      type="search"
      placeholder="Rechercher une offre ou un partenaire..."
      class="w-full pl-10 pr-4 py-2.5 text-sm text-gray-900 border border-gray-300 rounded-lg
             bg-white placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 focus:outline-none
             transition-colors duration-200"
    />

    <!-- Indicateur de chargement -->
    <div v-if="isLoading" class="absolute inset-y-0 right-0 pr-3 flex items-center">
      <svg class="w-4 h-4 text-orange-500 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <!-- Dropdown des résultats -->
    <Transition name="fade-slide">
      <div
        v-if="show && (results.length > 0 || (query.length >= 2 && results.length === 0))"
        class="absolute top-full left-0 right-0 z-[70] mt-1 bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden"
      >
        <!-- Résultats -->
        <ul v-if="results.length > 0" class="max-h-80 overflow-y-auto">
          <li
            v-for="item in results"
            :key="item.id"
            @mousedown.prevent="select(item)"
            class="flex items-center gap-3 px-4 py-3 text-sm hover:bg-orange-50 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors"
          >
            <!-- Image -->
            <div class="flex-shrink-0">
              <img
                :src="getImageUrl(item)"
                :alt="item.label"
                class="w-12 h-12 rounded-lg object-cover border border-gray-200"
                @error="handleImageError"
              />
            </div>
            
            <!-- Contenu -->
            <div class="flex-grow min-w-0">
              <div class="font-semibold text-gray-900 truncate">{{ item.label }}</div>
              <div class="flex items-center gap-2 mt-1">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                      :class="item.type === 'offre' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'">
                  {{ item.type === 'offre' ? '🎯 Offre' : '👤 Partenaire' }}
                </span>
                <span v-if="item.secteur" class="text-xs text-gray-500">{{ item.secteur }}</span>
              </div>
            </div>

            <!-- Icône de navigation -->
            <div class="flex-shrink-0">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </li>
        </ul>

        <!-- Aucun résultat -->
        <div v-else-if="query.length >= 2 && results.length === 0 && !isLoading" 
             class="px-4 py-6 text-center text-gray-500">
          <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-sm font-medium">Aucun résultat trouvé</p>
          <p class="text-xs mt-1">Essayez avec d'autres mots-clés</p>
        </div>

        <!-- Footer avec suggestion -->
        <div v-if="results.length > 0" class="px-4 py-2 bg-gray-50 border-t border-gray-100">
          <p class="text-xs text-gray-500 text-center">
            Appuyez sur <kbd class="px-1 py-0.5 bg-white border border-gray-200 rounded text-xs">Entrée</kbd> pour voir tous les résultats
          </p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const query = ref('')
const results = ref([])
const show = ref(false)
const isLoading = ref(false)
const router = useRouter()

function hide() {
  setTimeout(() => show.value = false, 200)
}

function select(item) {
  show.value = false
  query.value = item.label
  if (item.type === 'offre') {
    router.push(`/offres/${item.id}`)
  } else if (item.type === 'partenaire') {
    router.push(`/partenaires/${item.slug}`)
  }
}

let timeout
function debouncedFetch() {
  clearTimeout(timeout)
  if (query.value.length < 2) {
    results.value = []
    show.value = false
    return
  }
  timeout = setTimeout(fetchSuggestions, 300)
}

async function fetchSuggestions() {
  isLoading.value = true
  try {
    const { data } = await axios.get('/api/search/suggestions', {
      params: { q: query.value }
    })
    results.value = data
    show.value = true
  } catch (err) {
    results.value = []
  } finally {
    isLoading.value = false
  }
}

function getImageUrl(item) {
  return item.image ? `http://localhost:5000/${item.image}` : '/src/assets/parten.jpg'
}

function handleImageError(event) {
  event.target.src = '/src/assets/parten.jpg'
}
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

kbd {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
}
</style>
