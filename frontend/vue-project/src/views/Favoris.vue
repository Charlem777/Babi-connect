<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Mes Favoris</h1>
            <p class="text-gray-600 mt-1">{{ favoris.length }} offre{{ favoris.length > 1 ? 's' : '' }} enregistrée{{ favoris.length > 1 ? 's' : '' }}</p>
          </div>
          <div class="flex items-center text-red-500">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
        <p class="text-gray-600 mt-4">Chargement de vos favoris...</p>
      </div>

      <!-- Empty state -->
      <div v-else-if="favoris.length === 0" class="text-center py-16">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Aucun favori pour le moment</h3>
        <p class="text-gray-600 mb-6">Explorez nos offres et ajoutez vos préférées à vos favoris</p>
        <router-link 
          to="/offres" 
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-orange-500 to-green-500 text-white rounded-lg hover:from-orange-600 hover:to-green-600 transition-all"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          Découvrir les offres
        </router-link>
      </div>

      <!-- Favoris grid -->
      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="(offre, index) in favoris" 
            :key="offre.id"
            class="animate-slideInUp"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <OffreCardAdapter :offre="offre" @favorite-removed="removeFavorite" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { api } from '@/api'
import OffreCardAdapter from '@/components/OffreCardAdapter.vue'

const authStore = useAuthStore()
const router = useRouter()
const favoris = ref([])
const loading = ref(true)

const loadFavoris = async () => {
  console.log('🔄 Favoris - loadFavoris called')
  console.log('🔄 Favoris - isAuthenticated:', authStore.isAuthenticated)
  console.log('🔄 Favoris - token:', authStore.token ? 'present' : 'missing')
  
  if (!authStore.isAuthenticated) {
    console.log('❌ Favoris - Not authenticated, redirecting to login')
    router.push('/login')
    return
  }

  try {
    loading.value = true
    console.log('🔄 Favoris - Making API call to /offres/favoris')
    const { data } = await api.get('/offres/favoris')
    console.log('✅ Favoris - API response:', data)
    favoris.value = data.offres || []
  } catch (error) {
    console.error('❌ Favoris - Error loading favoris:', error)
    if (error.response?.status === 401) {
      console.log('❌ Favoris - 401 error, redirecting to login')
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

const removeFavorite = (offreId) => {
  favoris.value = favoris.value.filter(offre => offre.id !== offreId)
}

onMounted(() => {
  loadFavoris()
})
</script>

<style scoped>
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideInUp {
  animation: slideInUp 0.6s ease-out forwards;
  opacity: 0;
}
</style>
