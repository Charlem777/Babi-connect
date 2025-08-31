<template>
  <div class="relative bg-white rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden group h-96 transform hover:-translate-y-2">
    <!-- PromoOverlay -->
    <PromoOverlay :offre="offre" />
    
    <!-- Image avec overlay gradient -->
    <div class="relative h-48 overflow-hidden">
      <img 
        :src="offre.image_banniere || getDefaultImage()" 
        :alt="offre.titre"
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
        @error="handleImageError"
      />
      <!-- Gradient overlay pour menu -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
      
      <!-- Badge type menu -->
      <div class="absolute top-3 left-3 bg-gradient-to-r from-orange-500 to-red-500 text-white px-3 py-1 rounded-full text-xs font-semibold shadow-lg">
        🍽️ Menu
      </div>
      
      <!-- Prix en overlay -->
      <div class="absolute bottom-3 left-3 text-white">
        <div v-if="offre.is_promo && offre.prix_original" class="flex items-center space-x-2">
          <span class="text-lg font-bold">{{ formatPrice(offre.prix) }}</span>
          <span class="text-sm line-through opacity-75">{{ formatPrice(offre.prix_original) }}</span>
        </div>
        <div v-else class="text-lg font-bold">{{ formatPrice(offre.prix) }}</div>
        <div class="text-xs opacity-90">FCFA</div>
      </div>
    </div>

    <!-- Contenu -->
    <div class="p-4 h-48 flex flex-col">
      <!-- Header avec titre et partenaire -->
      <div class="mb-3">
        <h3 class="font-bold text-gray-900 text-lg mb-1 line-clamp-1 group-hover:text-orange-600 transition-colors">
          {{ offre.titre }}
        </h3>
        <div class="flex items-center text-sm text-gray-600">
          <div class="w-6 h-6 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center text-white text-xs font-bold mr-2">
            {{ getPartenaireInitials() }}
          </div>
          <span>{{ offre.partenaire?.nom }}</span>
        </div>
      </div>

      <!-- Description menu -->
      <p class="text-gray-600 text-sm line-clamp-2 mb-3 flex-grow">
        {{ offre.description }}
      </p>

      <!-- Ingrédients/Tags si disponibles -->
      <div v-if="offre.tags && offre.tags.length" class="mb-3">
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="tag in offre.tags.slice(0, 3)" 
            :key="tag.id"
            class="inline-block bg-orange-50 text-orange-600 text-xs px-2 py-1 rounded-full border border-orange-200"
          >
            {{ tag.nom }}
          </span>
          <span v-if="offre.tags.length > 3" class="text-xs text-gray-400">
            +{{ offre.tags.length - 3 }}
          </span>
        </div>
      </div>

      <!-- Footer avec actions -->
      <div class="flex items-center justify-between pt-2 border-t border-gray-100">
        <!-- Stats -->
        <div class="flex items-center space-x-3 text-xs text-gray-500">
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
            </svg>
            {{ offre.favoris_count || 0 }}
          </div>
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
            </svg>
            {{ offre.vues || 0 }}
          </div>
        </div>

        <!-- Boutons d'action -->
        <div class="flex items-center space-x-2">
          <FavoriteButton :offre="offre" size="sm" />
          <ContactPartenaireButton 
            :partenaire="offre.partenaire"
            variant="secondary"
            size="sm"
            class="text-xs"
          />
        </div>
      </div>
    </div>

    <!-- Effet shine au hover -->
    <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import PromoOverlay from './PromoOverlay.vue'
import FavoriteButton from './FavoriteButton.vue'
import ContactPartenaireButton from './chat/ContactPartenaireButton.vue'

const props = defineProps({
  offre: {
    type: Object,
    required: true
  }
})

const formatPrice = (price) => {
  if (!price) return 'Prix sur demande'
  return new Intl.NumberFormat('fr-FR').format(price)
}

const getPartenaireInitials = () => {
  if (!props.offre.partenaire?.nom) return '?'
  return props.offre.partenaire.nom
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .substring(0, 2)
    .toUpperCase()
}

const getDefaultImage = () => {
  return '/default-menu.jpg'
}

const handleImageError = (event) => {
  event.target.src = getDefaultImage()
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
