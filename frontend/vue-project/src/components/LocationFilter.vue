<template>
  <div class="location-filter bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-gradient-to-r from-orange-500 to-green-500 rounded-xl flex items-center justify-center">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-bold text-gray-900">Localisation</h3>
          <p class="text-sm text-gray-500">Trouvez des offres près de chez vous</p>
        </div>
      </div>
      <button 
        v-if="hasActiveFilters"
        @click="clearFilters"
        class="text-sm text-orange-600 hover:text-orange-700 font-medium"
      >
        Effacer
      </button>
    </div>

    <!-- Search Inputs -->
    <div class="space-y-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Ville</label>
        <div class="relative">
          <input
            v-model="selectedVille"
            @input="onVilleInput"
            @focus="showVilleSuggestions = true"
            type="text"
            placeholder="Entrez une ville..."
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
          />
          <div class="absolute inset-y-0 right-0 flex items-center pr-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          
          <!-- Ville Suggestions -->
          <div 
            v-if="showVilleSuggestions && villeSuggestions.length > 0"
            class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-xl shadow-lg max-h-48 overflow-y-auto"
          >
            <div
              v-for="ville in villeSuggestions"
              :key="ville.nom"
              @click="selectVille(ville)"
              class="px-4 py-3 hover:bg-gray-50 cursor-pointer flex items-center justify-between"
            >
              <span class="text-gray-900">{{ ville.nom }}</span>
              <span class="text-xs text-gray-500">{{ ville.offres_count }} offres</span>
            </div>
          </div>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Commune</label>
        <div class="relative">
          <input
            v-model="selectedCommune"
            @input="onCommuneInput"
            @focus="showCommuneSuggestions = true"
            type="text"
            placeholder="Entrez une commune..."
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
          />
          <div class="absolute inset-y-0 right-0 flex items-center pr-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          
          <!-- Commune Suggestions -->
          <div 
            v-if="showCommuneSuggestions && communeSuggestions.length > 0"
            class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-xl shadow-lg max-h-48 overflow-y-auto"
          >
            <div
              v-for="commune in communeSuggestions"
              :key="commune.nom"
              @click="selectCommune(commune)"
              class="px-4 py-3 hover:bg-gray-50 cursor-pointer flex items-center justify-between"
            >
              <span class="text-gray-900">{{ commune.nom }}</span>
              <span class="text-xs text-gray-500">{{ commune.offres_count }} offres</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Popular Locations -->
    <div v-if="!hasActiveFilters && popularLocations.villes?.length > 0">
      <h4 class="text-sm font-medium text-gray-700 mb-3">Villes populaires</h4>
      <div class="flex flex-wrap gap-2 mb-4">
        <button
          v-for="ville in popularLocations.villes.slice(0, 6)"
          :key="ville.nom"
          @click="selectVille(ville)"
          class="px-3 py-2 bg-orange-50 text-orange-700 rounded-lg text-sm hover:bg-orange-100 transition-colors"
        >
          {{ ville.nom }}
        </button>
      </div>
    </div>

    <div v-if="!hasActiveFilters && popularLocations.communes?.length > 0">
      <h4 class="text-sm font-medium text-gray-700 mb-3">Communes populaires</h4>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="commune in popularLocations.communes.slice(0, 6)"
          :key="commune.nom"
          @click="selectCommune(commune)"
          class="px-3 py-2 bg-green-50 text-green-700 rounded-lg text-sm hover:bg-green-100 transition-colors"
        >
          {{ commune.nom }}
        </button>
      </div>
    </div>

    <!-- Active Filters Display -->
    <div v-if="hasActiveFilters" class="mt-6 pt-4 border-t border-gray-100">
      <div class="flex flex-wrap gap-2">
        <div v-if="selectedVille" class="flex items-center bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          </svg>
          {{ selectedVille }}
          <button @click="selectedVille = ''; applyFilters()" class="ml-2 hover:text-orange-900">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div v-if="selectedCommune" class="flex items-center bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H3m2 0h4"/>
          </svg>
          {{ selectedCommune }}
          <button @click="selectedCommune = ''; applyFilters()" class="ml-2 hover:text-green-900">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

export default {
  name: 'LocationFilter',
  emits: ['filter-change'],
  setup(props, { emit }) {
    const selectedVille = ref('')
    const selectedCommune = ref('')
    const popularLocations = ref({ villes: [], communes: [] })
    const villeSuggestions = ref([])
    const communeSuggestions = ref([])
    const showVilleSuggestions = ref(false)
    const showCommuneSuggestions = ref(false)

    const hasActiveFilters = computed(() => {
      return selectedVille.value || selectedCommune.value
    })

    const loadPopularLocations = async () => {
      try {
        const response = await axios.get('/api/locations/popular')
        popularLocations.value = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des localisations populaires:', error)
      }
    }

    const onVilleInput = () => {
      if (selectedVille.value) {
        villeSuggestions.value = popularLocations.value.villes.filter(v => 
          v.nom.toLowerCase().includes(selectedVille.value.toLowerCase())
        )
      } else {
        villeSuggestions.value = popularLocations.value.villes.slice(0, 5)
      }
      showVilleSuggestions.value = true
    }

    const onCommuneInput = () => {
      if (selectedCommune.value) {
        communeSuggestions.value = popularLocations.value.communes.filter(c => 
          c.nom.toLowerCase().includes(selectedCommune.value.toLowerCase())
        )
      } else {
        communeSuggestions.value = popularLocations.value.communes.slice(0, 5)
      }
      showCommuneSuggestions.value = true
    }

    const selectVille = (ville) => {
      selectedVille.value = ville.nom
      showVilleSuggestions.value = false
      applyFilters()
    }

    const selectCommune = (commune) => {
      selectedCommune.value = commune.nom
      showCommuneSuggestions.value = false
      applyFilters()
    }

    const applyFilters = () => {
      emit('filter-change', {
        ville: selectedVille.value,
        commune: selectedCommune.value
      })
    }

    const clearFilters = () => {
      selectedVille.value = ''
      selectedCommune.value = ''
      applyFilters()
    }

    // Close suggestions when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.location-filter')) {
        showVilleSuggestions.value = false
        showCommuneSuggestions.value = false
      }
    }

    onMounted(() => {
      loadPopularLocations()
      document.addEventListener('click', handleClickOutside)
    })

    watch([selectedVille, selectedCommune], () => {
      applyFilters()
    })

    return {
      selectedVille,
      selectedCommune,
      popularLocations,
      villeSuggestions,
      communeSuggestions,
      showVilleSuggestions,
      showCommuneSuggestions,
      hasActiveFilters,
      onVilleInput,
      onCommuneInput,
      selectVille,
      selectCommune,
      applyFilters,
      clearFilters
    }
  }
}
</script>

<style scoped>
.location-filter {
  animation: slideInUp 0.3s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
