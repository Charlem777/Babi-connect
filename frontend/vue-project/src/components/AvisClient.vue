<template>
  <section class="mt-8 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
    <div class="text-center mb-12">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">Avis clients</h2>
      <div class="flex items-center justify-center gap-2 text-gray-600">
        <div class="flex items-center gap-1">
          <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
          <span class="font-semibold">{{ averageRating }}</span>
          <span class="text-sm">sur 5</span>
        </div>
        <span class="text-sm">•</span>
        <span class="text-sm">{{ avisClients.length }} avis</span>
      </div>
    </div>

    <transition-group name="stagger" tag="div" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="(avis, index) in visibleAvis"
        :key="avis.id || index"
        :style="{ animationDelay: `${index * 100}ms` }"
        class="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-xl border border-gray-100 hover:border-gray-200 transition-all duration-500 hover:-translate-y-1"
      >
        <!-- Header avec avatar et info -->
        <div class="flex items-center gap-4 mb-4">
          <div class="relative">
            <img
              :src="avis?.photo || defaultAvatar"
              :alt="`Avatar de ${avis.nom}`"
              class="w-12 h-12 rounded-full object-cover ring-2 ring-gray-100 group-hover:ring-gray-200 transition-all duration-300"
              @error="handleAvatarError"
            />
            <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white"></div>
          </div>
          
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-gray-900 truncate">{{ avis.nom }}</h3>
            <p class="text-sm text-gray-500">{{ formatDate(avis.date) }}</p>
          </div>
          
          <!-- Badge note -->
          <div class="flex items-center gap-1 bg-yellow-50 px-2 py-1 rounded-full">
            <svg class="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <span class="text-sm font-semibold text-yellow-700">{{ avis.note.toFixed(1) }}</span>
          </div>
        </div>

        <!-- Rating stars -->
        <div class="flex items-center gap-1 mb-4">
          <div class="flex">
            <svg
              v-for="n in 5"
              :key="n"
              :class="n <= Math.round(avis.note) ? 'text-yellow-400' : 'text-gray-200'"
              class="w-4 h-4 transition-colors duration-200"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </div>
          <span class="text-xs text-gray-400 ml-1">{{ getRatingText(avis.note) }}</span>
        </div>

        <!-- Commentaire -->
        <div class="relative">
          <p class="text-gray-700 leading-relaxed text-sm">
            "{{ avis.commentaire }}"
          </p>
          
          <!-- Quote decoration -->
          <div class="absolute -top-2 -left-2 text-4xl text-gray-200 font-serif leading-none">"</div>
        </div>

        <!-- Footer avec actions -->
        <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-50">
          <div class="flex items-center gap-2 text-xs text-gray-400">
            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
            </svg>
            <span>Utile</span>
          </div>
          
          <div class="flex items-center gap-1 text-xs text-gray-400">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"/>
            </svg>
            <span>Partager</span>
          </div>
        </div>
      </div>
    </transition-group>

    <!-- Bouton voir plus -->
    <div v-if="avisClients.length > 6" class="mt-12 text-center">
      <button
        @click="voirPlusAvis"
        class="group relative bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white px-8 py-3 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
      >
        <span class="relative z-10 flex items-center gap-2">
          {{ showAll ? 'Voir moins d\'avis' : 'Voir plus d\'avis' }}
          <svg 
            :class="{ 'rotate-180': showAll }" 
            class="w-4 h-4 transition-transform duration-300" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </span>
        
        <!-- Effet de brillance -->
        <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
        </div>
      </button>
    </div>

    <!-- Message si pas d'avis -->
    <div v-if="!avisClients || avisClients.length === 0" class="text-center py-12">
      <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
      </div>
      <h3 class="text-lg font-semibold text-gray-900 mb-2">Aucun avis pour le moment</h3>
      <p class="text-gray-500">Soyez le premier à laisser un avis sur ce partenaire.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  avisClients: {
    type: Array,
    default: () => []
  },
  formatDate: {
    type: Function,
    default: (date) => new Date(date).toLocaleDateString('fr-FR')
  }
})

const showAll = ref(false)
const defaultAvatar = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMjAiIGZpbGw9IiNGM0Y0RjYiLz4KPHN2ZyB4PSI4IiB5PSI4IiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+CjxwYXRoIGQ9Ik0xMiAxMkMxNC4yMDkxIDEyIDE2IDEwLjIwOTEgMTYgOEMxNiA1Ljc5MDg2IDE0LjIwOTEgNCAxMiA0QzkuNzkwODYgNCA4IDUuNzkwODYgOCA4QzggMTAuMjA5MSA5Ljc5MDg2IDEyIDEyIDEyWiIgZmlsbD0iIzlDQTNBRiIvPgo8cGF0aCBkPSJNMTIgMTRDOC4xMzQwMSAxNCA1IDE3LjEzNCA1IDIxSDMuNUMzLjUgMTYuMzA1NiA3LjMwNTU4IDEyLjUgMTIgMTIuNUMxNi42OTQ0IDEyLjUgMjAuNSAxNi4zMDU2IDIwLjUgMjFIMTlDMTkgMTcuMTM0IDE1Ljg2NiAxNCAxMiAxNFoiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+Cjwvc3ZnPgo='

const voirPlusAvis = () => {
  showAll.value = !showAll.value
}

const visibleAvis = computed(() => {
  if (!props.avisClients) return []
  return showAll.value ? props.avisClients : props.avisClients.slice(0, 6)
})

const averageRating = computed(() => {
  if (!props.avisClients || props.avisClients.length === 0) return '0.0'
  const sum = props.avisClients.reduce((acc, avis) => acc + avis.note, 0)
  return (sum / props.avisClients.length).toFixed(1)
})

const getRatingText = (note) => {
  if (note >= 4.5) return 'Excellent'
  if (note >= 4) return 'Très bien'
  if (note >= 3) return 'Bien'
  if (note >= 2) return 'Moyen'
  return 'Décevant'
}

const handleAvatarError = (event) => {
  event.target.src = defaultAvatar
}
</script>

<style scoped>
.stagger-enter-active {
  transition: all 0.6s ease-out;
}

.stagger-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
