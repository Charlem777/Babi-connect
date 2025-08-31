<template>
  <div class="relative bg-gradient-to-br from-purple-600 via-pink-600 to-orange-500 rounded-2xl overflow-hidden shadow-2xl group-hover:shadow-3xl transition-all duration-500 transform hover:-translate-y-2 cursor-pointer min-h-[420px]"
       @click="handleCardClick">
    
    <!-- Background avec effet parallax -->
    <div class="absolute inset-0 opacity-30">
      <img
        :src="imageUrl"
        :alt="offre.titre"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        @error="handleImageError"
      />
    </div>
    
    <!-- Glassmorphisme overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent backdrop-blur-sm"></div>
    
    <!-- Contenu événementiel -->
    <div class="relative z-10 p-6 h-full flex flex-col justify-between text-white">
      <!-- Header avec date et prix -->
      <div class="flex justify-between items-start mb-4">
        <div class="bg-white/20 backdrop-blur-md rounded-xl px-4 py-2 border border-white/30">
          <div class="text-xs font-medium opacity-90">{{ formatEventDate() }}</div>
          <div class="text-lg font-bold">{{ formatPrice(offre.prix) }}</div>
        </div>
        <div class="bg-gradient-to-r from-yellow-400 to-orange-500 text-black px-3 py-1 rounded-full text-xs font-bold">
          🎉 ÉVÉNEMENT
        </div>
      </div>
      
      <!-- Titre principal -->
      <div class="flex-1 flex flex-col justify-center text-center mb-6">
        <h3 class="text-2xl font-black mb-2 leading-tight drop-shadow-lg">
          {{ offre.titre }}
        </h3>
        <p class="text-sm opacity-90 line-clamp-2">{{ offre.description }}</p>
      </div>
      
      <!-- Footer avec organisateur et action -->
      <div class="space-y-4">
        <div class="flex items-center gap-3 bg-white/10 backdrop-blur-md rounded-xl p-3 border border-white/20">
          <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <img 
              v-if="offre.partenaire?.logo" 
              :src="'http://localhost:5000' + offre.partenaire.logo" 
              :alt="offre.partenaire.nom"
              class="w-full h-full object-cover rounded-full"
              @error="handleLogoError"
            />
            <span v-else class="text-sm font-bold">{{ getPartnerInitial() }}</span>
          </div>
          <div class="flex-1">
            <div class="font-semibold text-sm">{{ offre.partenaire?.nom || 'Organisateur' }}</div>
            <div class="text-xs opacity-75">📍 {{ offre.partenaire?.ville || offre.ville }}</div>
          </div>
        </div>
        
        <!-- Bouton d'action événementiel -->
        <div class="flex gap-2" @click.stop>
          <button class="flex-1 bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg">
            🎫 Réserver
          </button>
          <FavoriteButton :offre-id="offre.id" size="lg" class="bg-white/20 backdrop-blur-md border border-white/30 rounded-xl" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/api'
import FavoriteButton from '@/components/FavoriteButton.vue'

const props = defineProps({
  offre: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const handleCardClick = async () => {
  try {
    await api.post(`/offres/${props.offre.id}/view`)
  } catch (error) {
    console.error('Erreur lors de l\'incrémentation des vues:', error)
  }
  
  router.push(`/offres/${props.offre.id}`)
}

const imageUrl = computed(() => {
  if (props.offre.image_banniere) {
    return 'http://localhost:5000' + props.offre.image_banniere
  }
  return '/default-evenement.jpg'
})

const formatEventDate = () => {
  if (props.offre.expire_le) {
    const date = new Date(props.offre.expire_le)
    return date.toLocaleDateString('fr-FR', { 
      day: 'numeric', 
      month: 'short' 
    })
  }
  return 'Bientôt'
}

const formatPrice = (price) => {
  if (!price) return 'Gratuit'
  if (price < 1000) return `${price} FCFA`
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'XOF',
    minimumFractionDigits: 0
  }).format(price).replace('XOF', 'FCFA')
}

const handleImageError = (event) => {
  event.target.src = '/default-evenement.jpg'
}

const handleLogoError = (event) => {
  event.target.style.display = 'none'
  event.target.nextElementSibling.style.display = 'block'
}

const getPartnerInitial = () => {
  const nom = props.offre.partenaire?.nom || 'O'
  return nom.charAt(0).toUpperCase()
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

.backdrop-blur-md {
  backdrop-filter: blur(12px);
}

.shadow-3xl {
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
}

@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.bg-gradient-to-br {
  background-size: 200% 200%;
  animation: gradient-shift 6s ease infinite;
}
</style>
