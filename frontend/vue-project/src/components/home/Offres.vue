<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header Section -->
    <div class="bg-white border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div class="space-y-2">
            <h1 class="text-3xl font-bold text-gray-900">
              {{ getPageTitle() }}
            </h1>
            <div class="flex flex-wrap items-center gap-2 text-sm text-gray-600">
              <span v-if="!loading" class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
                {{ pagination.total || offres.length }} {{ (pagination.total || offres.length) === 1 ? 'offre trouvée' : 'offres trouvées' }}
              </span>
              <div v-if="hasActiveFilters()" class="flex flex-wrap items-center gap-2">
                <span class="text-gray-400">•</span>
                <div class="flex flex-wrap gap-2">
                  <span v-if="secteurSlug" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                    Secteur: {{ secteurSlug }}
                  </span>
                  <span v-if="categorieSlug" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Catégorie: {{ categorieSlug }}
                  </span>
                  <span v-if="locationFilters.ville" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    Ville: {{ locationFilters.ville }}
                  </span>
                  <span v-if="locationFilters.commune" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    Commune: {{ locationFilters.commune }}
                  </span>
                  <span v-if="searchQuery" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    Recherche: "{{ searchQuery }}"
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Sort and Filter Options -->
          <div class="flex items-center gap-3">
            <select v-model="sortBy" @change="loadOffres" class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500">
              <option value="recent">Plus récentes</option>
              <option value="price_asc">Prix croissant</option>
              <option value="price_desc">Prix décroissant</option>
              <option value="popularity">Plus populaires</option>
            </select>
            <button @click="toggleViewMode" class="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <svg v-if="viewMode === 'grid'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
              </svg>
            </button>
            <button 
              v-if="hasActiveFilters()" 
              @click="clearAllFilters"
              class="px-3 py-2 text-sm text-orange-600 hover:text-orange-700 font-medium border border-orange-200 rounded-lg hover:bg-orange-50 transition-colors"
            >
              Effacer filtres
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar with LocationFilter -->
        <div class="lg:w-80 space-y-6">
          <LocationFilter @filter-change="onLocationFilterChange" />
        </div>

        <!-- Main Content -->
        <div class="flex-1">
          <!-- Loading State -->
          <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="i in 6" :key="i" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden animate-pulse">
              <div class="h-48 bg-gray-200"></div>
              <div class="p-4 space-y-3">
                <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                <div class="h-6 bg-gray-200 rounded w-1/4"></div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="offres.length === 0" class="text-center py-16">
            <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
              <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Aucune offre trouvée</h3>
            <p class="text-gray-600 mb-6">{{ getEmptyStateMessage() }}</p>
            <button 
              @click="clearAllFilters"
              class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-orange-500 to-green-500 text-white rounded-lg hover:from-orange-600 hover:to-green-600 transition-all"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Voir toutes les offres
            </button>
          </div>

          <!-- Offers Grid -->
          <div v-else>
            <div :class="getGridClasses()">
              <div 
                v-for="(offre, index) in offres" 
                :key="offre.id"
                class="animate-slideInUp"
                :style="{ animationDelay: `${index * 0.1}s` }"
              >
                <OffreCardAdapter :offre="offre" />
              </div>
            </div>

            <!-- Load More Button -->
            <div v-if="pagination.page < pagination.pages" class="text-center mt-12">
              <button 
                @click="loadMoreOffres"
                :disabled="loadingMore"
                class="inline-flex items-center px-8 py-3 bg-gradient-to-r from-orange-500 to-green-500 text-white rounded-xl hover:from-orange-600 hover:to-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105"
              >
                <svg v-if="loadingMore" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ loadingMore ? 'Chargement...' : 'Charger plus d\'offres' }}
                <svg v-if="!loadingMore" class="ml-2 w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import OffreCardAdapter from '../OffreCardAdapter.vue'
import LocationFilter from '../LocationFilter.vue'

export default {
  name: 'Offres',
  components: {
    OffreCardAdapter,
    LocationFilter
  },
  setup() {
    const route = useRoute()
    const offres = ref([])
    const loading = ref(true)
    const loadingMore = ref(false)
    const viewMode = ref('grid')
    const sortBy = ref('recent')
    const locationFilters = ref({ ville: '', commune: '' })
    const pagination = ref({ page: 1, pages: 1, total: 0, per_page: 20 })

    const secteurSlug = computed(() => route.query.secteur_slug || '')
    const categorieSlug = computed(() => route.query.categorie_slug || '')
    const searchQuery = computed(() => route.query.q || '')

    const buildApiUrl = (page = 1) => {
      const params = new URLSearchParams()
      
      if (secteurSlug.value) params.append('secteur_slug', secteurSlug.value)
      if (categorieSlug.value) params.append('categorie_slug', categorieSlug.value)
      if (locationFilters.value.ville) params.append('ville', locationFilters.value.ville)
      if (locationFilters.value.commune) params.append('commune', locationFilters.value.commune)
      if (sortBy.value) params.append('sort', sortBy.value)
      
      params.append('page', page.toString())
      params.append('per_page', pagination.value.per_page.toString())
      
      return `/api/offres?${params.toString()}`
    }

    const loadOffres = async (resetPagination = true) => {
      try {
        loading.value = true
        if (resetPagination) {
          pagination.value.page = 1
          offres.value = []
          console.log('offres.value', offres.value)
        }
        
        const response = await axios.get(buildApiUrl(pagination.value.page))
        console.log('API Response:', response.data) // Debug log
        
        // Handle both old and new API response formats
        let offresData = []
        let paginationData = { page: 1, pages: 1, total: 0, per_page: 20 }
        
        if (Array.isArray(response.data)) {
          // Old format: direct array
          offresData = response.data
          paginationData.total = response.data.length
        } else if (response.data.offres) {
          // New format: object with offres and pagination
          offresData = response.data.offres
          paginationData = response.data.pagination || paginationData
        }
        
        console.log('Processed offres:', offresData) // Debug log
        
        if (resetPagination) {
          offres.value = offresData
        } else {
          offres.value.push(...offresData)
        }
        
        pagination.value = paginationData
      } catch (error) {
        console.error('Erreur lors du chargement des offres:', error)
        offres.value = []
      } finally {
        loading.value = false
        loadingMore.value = false
      }
    }

    const loadMoreOffres = async () => {
      if (pagination.value.page >= pagination.value.pages) return
      
      loadingMore.value = true
      pagination.value.page += 1
      await loadOffres(false)
    }

    const onLocationFilterChange = (filters) => {
      locationFilters.value = filters
      loadOffres()
    }

    const hasActiveFilters = () => {
      return secteurSlug.value || categorieSlug.value || searchQuery.value || 
             locationFilters.value.ville || locationFilters.value.commune
    }

    const clearAllFilters = () => {
      locationFilters.value = { ville: '', commune: '' }
      // Reset route query params would need router navigation
      loadOffres()
    }

    const getPageTitle = () => {
      if (locationFilters.value.ville && locationFilters.value.commune) {
        return `Offres à ${locationFilters.value.commune}, ${locationFilters.value.ville}`
      } else if (locationFilters.value.ville) {
        return `Offres à ${locationFilters.value.ville}`
      } else if (locationFilters.value.commune) {
        return `Offres à ${locationFilters.value.commune}`
      } else if (secteurSlug.value) {
        return `Offres ${secteurSlug.value}`
      } else if (categorieSlug.value) {
        return `Offres ${categorieSlug.value}`
      }
      return 'Toutes les offres'
    }

    const getEmptyStateMessage = () => {
      if (hasActiveFilters()) {
        return 'Essayez de modifier vos critères de recherche ou votre localisation.'
      }
      return 'Aucune offre disponible pour le moment. Revenez plus tard !'
    }

    const getGridClasses = () => {
      if (viewMode.value === 'list') {
        return 'space-y-4'
      }
      return 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-6'
    }

    const toggleViewMode = () => {
      viewMode.value = viewMode.value === 'grid' ? 'list' : 'grid'
    }

    // Watch for route changes
    watch(() => route.query, () => {
      loadOffres()
    }, { deep: true })

    onMounted(() => {
      loadOffres()
    })

    return {
      offres,
      loading,
      loadingMore,
      viewMode,
      sortBy,
      locationFilters,
      pagination,
      secteurSlug,
      categorieSlug,
      searchQuery,
      loadOffres,
      loadMoreOffres,
      onLocationFilterChange,
      hasActiveFilters,
      clearAllFilters,
      getPageTitle,
      getEmptyStateMessage,
      getGridClasses,
      toggleViewMode
    }
  }
}
</script>

<style scoped>
.animate-slideInUp {
  animation: slideInUp 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes slideInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
