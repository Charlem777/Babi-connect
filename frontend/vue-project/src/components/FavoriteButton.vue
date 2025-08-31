<template>
  <button
    @click.stop="toggleFavorite"
    :disabled="isLoading"
    :class="[
      'inline-flex items-center justify-center p-2 rounded-full transition-all duration-200',
      isFavorite 
        ? 'bg-red-100 text-red-600 hover:bg-red-200' 
        : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
      isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 active:scale-95'
    ]"
    :title="isFavorite ? 'Retirer des favoris' : 'Ajouter aux favoris'"
  >
    <svg 
      class="w-5 h-5" 
      :fill="isFavorite ? 'currentColor' : 'none'" 
      stroke="currentColor" 
      viewBox="0 0 24 24"
    >
      <path 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        stroke-width="2" 
        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
      />
    </svg>
  </button>

  <!-- Toast notification -->
  <div 
    v-if="showToast" 
    class="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-bounce"
  >
    {{ toastMessage }}
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api'

const props = defineProps({
  offreId: {
    type: Number,
    required: true
  }
})

const authStore = useAuthStore()
const isFavorite = ref(false)
const isLoading = ref(false)
const showToast = ref(false)
const toastMessage = ref('')

const checkFavoriteStatus = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const { data } = await api.get(`/offres/${props.offreId}/favoris/status`)
    isFavorite.value = data.is_favori
  } catch (error) {
    console.error('Erreur lors de la vérification du statut favori:', error)
  }
}

const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const toggleFavorite = async (event) => {
  // Empêcher la propagation vers le router-link parent
  event.preventDefault()
  event.stopPropagation()

  if (!authStore.isAuthenticated) {
    showToastMessage('Connectez-vous pour ajouter aux favoris')
    return
  }

  if (isLoading.value) return

  try {
    isLoading.value = true
    const { data } = await api.post(`/offres/${props.offreId}/favoris`)
    isFavorite.value = data.is_favori
    
    // Afficher le message de confirmation
    if (data.is_favori) {
      showToastMessage('✅ Offre enregistrée dans vos favoris')
    } else {
      showToastMessage('❌ Offre supprimée de vos favoris')
    }
  } catch (error) {
    console.error('Erreur lors de la modification des favoris:', error)
    showToastMessage('❌ Erreur lors de la modification des favoris')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  checkFavoriteStatus()
})
</script>
