<template>
  <div v-if="offre.is_promo" class="absolute top-0 left-0 right-0 z-10">
    <!-- Badge promo principal -->
    <div class="relative">
      <!-- Badge coin supérieur droit -->
      <div class="absolute -top-1 -right-1 bg-gradient-to-br from-red-500 via-red-600 to-red-700 text-white px-3 py-1 rounded-bl-2xl rounded-tr-2xl shadow-lg transform rotate-3 animate-pulse">
        <div class="flex items-center space-x-1">
          <span class="text-xs font-bold">🔥 PROMO</span>
        </div>
      </div>
      
      <!-- Badge pourcentage si disponible -->
      <div v-if="offre.pourcentage_reduction" 
           class="absolute top-3 right-3 bg-gradient-to-br from-orange-400 to-red-500 text-white rounded-full w-12 h-12 flex items-center justify-center shadow-lg transform -rotate-12 animate-bounce">
        <span class="text-xs font-black">-{{ offre.pourcentage_reduction }}%</span>
      </div>
    </div>
    
    <!-- Barre flash en bas -->
    <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-red-400 via-orange-400 to-red-400 animate-pulse"></div>
  </div>
</template>

<script setup>
const props = defineProps({
  offre: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
@keyframes flash {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.animate-flash {
  animation: flash 1.5s infinite;
}
</style>
