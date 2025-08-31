<template>
    <div class="relative bg-white rounded-xl overflow-hidden shadow-lg group-hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
      
      <!-- Image de fond -->
      <div class="relative h-32 sm:h-40 overflow-hidden">
        <img
          :src="imageUrl"
          :alt="offre.titre"
          class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          @error="handleImageError"
        />
        
        <!-- Gradient overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent"></div>
        
        <!-- Badge secteur -->
        <div :class="sectorBadgeClass" class="absolute top-2 left-2 px-2 py-1 rounded-full text-xs font-bold">
          {{ sectorIcon }} {{ offre.secteur }}
        </div>
        
        <!-- Prix badge -->
        <div class="absolute bottom-2 right-2 bg-white text-gray-900 px-2 py-1 rounded-lg font-bold text-xs shadow-md">
          {{ formatPrice(offre.prix) }}
        </div>
      </div>
      
      <!-- Contenu de la carte -->
      <div class="p-3 sm:p-4">
        <!-- Titre et description -->
        <div class="mb-3">
          <h3 class="text-sm sm:text-base font-bold text-gray-900 leading-tight mb-1 line-clamp-2">
            {{ offre.titre }}
          </h3>
          <p class="text-xs sm:text-sm text-gray-600 line-clamp-2 leading-relaxed">
            {{ offre.description }}
          </p>
        </div>
        
        <!-- Partenaire info -->
        <div class="flex items-center gap-2 mb-3">
          <div class="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center overflow-hidden">
            <img 
              v-if="offre.partenaire?.logo" 
              :src="'http://localhost:5000' + offre.partenaire.logo" 
              :alt="offre.partenaire.nom"
              class="w-full h-full object-cover"
              @error="handleLogoError"
            />
            <span v-else class="text-xs font-bold text-gray-600">{{ getPartnerInitial() }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <span class="text-xs text-gray-700 font-medium block truncate">{{ offre.partenaire?.nom || 'Partenaire' }}</span>
            <span class="text-xs text-gray-500">{{ offre.partenaire?.ville || offre.ville }}</span>
          </div>
        </div>
        
        <!-- Stats et actions -->
        <div class="flex items-center justify-between">
          <!-- Stats -->
          <div class="flex items-center space-x-3 text-xs">
            <div class="flex items-center text-yellow-500">
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              <span class="font-medium">{{ offre.note_moyenne || 'N/A' }}</span>
            </div>
            
            <div class="flex items-center text-gray-500">
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
              </svg>
              <span>{{ offre.favoris_count || 0 }}</span>
            </div>
            
            <div class="flex items-center text-gray-500">
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
              </svg>
              <span>{{ offre.vues || 0 }}</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center space-x-1">
            <router-link :to="`/offres/${offre.id}`" class="block group">

            <ContactPartenaireButton 
              :partenaire="offre.partenaire"
              variant="secondary"
              size="xs"
            />
          </router-link>

            <FavoriteButton :offre-id="offre.id" size="sm" />
          </div>
       

        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ContactPartenaireButton from '@/components/chat/ContactPartenaireButton.vue'
import FavoriteButton from '@/components/FavoriteButton.vue'

const props = defineProps({
  offre: {
    type: Object,
    required: true
  }
})

const imageUrl = computed(() => {
  if (props.offre.image_banniere) {
    return 'http://localhost:5000' + props.offre.image_banniere
  }
  return getSectorDefaultImage()
})

const getSectorDefaultImage = () => {
  const defaultImages = {
    'Restaurant': '/default-restaurant.jpg',
    'Service': '/default-service.jpg',
    'Mode': '/default-mode.jpg',
    'Bien-être': '/default-bienetre.jpg',
    'Logement': '/default-logement.jpg',
    'Tourisme': '/default-tourisme.jpg',
    'Événement': '/default-evenement.jpg'
  }
  return defaultImages[props.offre.secteur] || '/default-offer.jpg'
}

const sectorIcon = computed(() => {
  const icons = {
    'Restaurant': '🍽️',
    'Service': '🔧',
    'Mode': '👗',
    'Bien-être': '💆',
    'Logement': '🏠',
    'Tourisme': '🏖️',
    'Événement': '🎉'
  }
  return icons[props.offre.secteur] || '🏢'
})

const sectorBadgeClass = computed(() => {
  const classes = {
    'Restaurant': 'bg-red-500/90 text-white',
    'Service': 'bg-blue-500/90 text-white',
    'Mode': 'bg-pink-500/90 text-white',
    'Bien-être': 'bg-green-500/90 text-white',
    'Logement': 'bg-purple-500/90 text-white',
    'Tourisme': 'bg-cyan-500/90 text-white',
    'Événement': 'bg-yellow-500/90 text-black'
  }
  return classes[props.offre.secteur] || 'bg-gray-500/90 text-white'
})

const formatPrice = (price) => {
  if (!price) return 'Sur demande'
  if (price < 1000) return `${price} FCFA`
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'XOF',
    minimumFractionDigits: 0
  }).format(price).replace('XOF', 'FCFA')
}

const handleImageError = (event) => {
  event.target.src = getSectorDefaultImage()
}

const handleLogoError = (event) => {
  event.target.style.display = 'none'
  event.target.nextElementSibling.style.display = 'block'
}

const getPartnerInitial = () => {
  const nom = props.offre.partenaire?.nom || 'P'
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
</style>
