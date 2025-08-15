<template>
  <section class="mt-5 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
    <h2 class="text-2xl font-semibold text-neutral-800 mb-8 tracking-tight">Avis clients</h2>

    <transition-group name="fade" tag="div" class="space-y-8">
      <div
        v-for="(avis, index) in visibleAvis"
        :key="index"
        class="flex flex-col sm:flex-row sm:items-start gap-4 border-b border-neutral-200 pb-6"
      >
        <img
          :src="avis?.photo || '/default-user.png'"
          alt="Avatar"
          class="w-12 h-12 rounded-full object-cover shadow-sm"
        />

        <div class="flex flex-col flex-grow">
          <div class="flex items-center justify-between mb-1">
            <span class="text-base font-semibold text-neutral-800">{{ avis.nom }}</span>
            <span class="text-xs text-neutral-400">{{ formatDate(avis.date) }}</span>
          </div>

          <div class="flex items-center gap-1 mb-2">
            <span
              v-for="n in 5"
              :key="n"
              class="text-yellow-400 text-sm"
            >
              {{ n <= Math.round(avis.note) ? '★' : '☆' }}
            </span>
            <span class="text-sm text-neutral-500 ml-2">{{ avis.note.toFixed(1) }}/5</span>
          </div>

          <p class="text-sm text-neutral-600 leading-relaxed">
            {{ avis.commentaire }}
          </p>
        </div>
      </div>
    </transition-group>

    <div v-if="avisClients.length > 5" class="mt-8 text-center">
      <button
        @click="voirPlusAvis"
        class="bg-gray-100 hover:bg-gray-200 text-gray-800 px-6 py-2 rounded-full text-sm transition"
      >
        Voir plus d’avis
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  avisClients: Array,
  formatDate: Function
})

const showAll = ref(false)
const voirPlusAvis = () => (showAll.value = !showAll.value)

const visibleAvis = computed(() =>
  showAll.value ? props.avisClients : props.avisClients.slice(0, 5)
)
</script>
