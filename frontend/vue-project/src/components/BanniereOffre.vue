<template>
  <div class="relative w-full h-64 md:h-80 overflow-hidden shadow-lg">
    <!-- Image de fond -->
    <img
      src="/Users/mac/Babi_connect/frontend/vue-project/src/assets/beau.jpg"
      alt="Attiéké Poisson"
      class="w-full h-full object-cover"
    />

    <!-- Overlay dégradé -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/30 to-transparent"></div>

    <!-- Contenu -->
    <div class="absolute inset-0 px-6 md:px-12 py-4 text-white z-10 flex flex-col justify-between">
      
      <!-- Ligne du haut -->
      <div></div>

      <!-- Ligne du bas -->
      <div>
        <!-- Titre + localisation + prix -->
        <div class="flex justify-between items-end mb-2">
          <div>
            <h1 class="text-lg md:text-xl font-bold leading-tight drop-shadow-md">
              {{ offre.titre }}
            </h1>
            <p class="text-sm md:text-base font-medium drop-shadow-sm">
              {{ offre.partenaire?.commune }},
              {{ offre.localisation }}
            </p>
          </div>

          <!-- Prix -->
          <div class="text-sm md:text-base font-semibold bg-black/40 px-3 py-1 rounded shadow">
            <span v-if="!hasOptions">Prix : {{ formatPrix(offre.prix) }}</span>
            <span v-else>À partir de {{ formatPrix(prixMinimum) }}</span>
          </div>
        </div>

        <!-- Bouton -->
        <button
          @click="hasOptions ? showModal = true : confirmParticipation()"
          class="w-full bg-green-500 hover:bg-green-600 active:scale-95 transition transform px-4 py-3 rounded-lg font-semibold shadow-md text-center"
        >
          {{ hasOptions ? 'Voir les options' : 'Confirmer ma participation' }}
        </button>
      </div>
    </div>

   <!-- Modal des options -->
<div
  v-if="showModal"
  class="fixed inset-0 bg-black/70 z-50 flex items-center justify-center"
>
  <div class="bg-white rounded-lg p-6 w-11/12 max-w-md text-black shadow-xl">
    <h2 class="text-lg font-bold mb-4">Choisissez une option</h2>
    <ul class="space-y-2">
      <li
        v-for="option in offre.options"
        :key="option.id"
        class="flex justify-between items-center border-b pb-2"
      >
        <div>
          <p class="font-semibold">{{ option.nom }}</p>
          <p class="text-sm text-gray-600">{{ option.description }} – {{ option.duree }}</p>
        </div>
        <span class="text-green-600 font-bold">{{ formatPrix(option.prix) }}</span>
      </li>
    </ul>
    <button
      @click="showModal = false"
      class="mt-4 w-full bg-gray-800 text-white py-2 rounded hover:bg-gray-700"
    >
      Fermer
    </button>
  </div>
</div>

  </div>
</template>
<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  offre: {
    type: Object,
    required: true
  }
})
console.log(props.offre.localisation)

const showModal = ref(false)

const hasOptions = computed(() => Array.isArray(props.offre.options) && props.offre.options.length > 0)

const prixMinimum = computed(() => {
  if (!hasOptions.value) return props.offre.prix
  return Math.min(...props.offre.options.map(opt => opt.prix))
})

function formatPrix(prix) {
  if (typeof prix !== 'number') return '—'
  return `${prix.toLocaleString()} FCFA`
}


function confirmParticipation() {
  alert("Participation confirmée !")
}
</script>
