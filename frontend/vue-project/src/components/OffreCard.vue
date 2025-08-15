<template>
  <div
    class="bg-white rounded-xl shadow-md w-full overflow-hidden flex flex-row sm:flex-col hover:scale-[1.01] transition-transform duration-300"
  >
    <!-- Image -->
    <img
      src="/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer4.jpeg"
      alt="Image offre"
      class="h-32 w-23 object-cover object-center sm:w-full sm:h-40"
    />

    <!-- Infos -->
    <div class="p-4 flex flex-col justify-between flex-grow w-1/2 sm:w-full">
      <h3 class="text-base font-semibold text-gray-800 mb-1">{{ offre.titre }}</h3>

      <div class="text-sm text-gray-700">
        <span v-if="offre.options?.length">
          À partir de
          <span class="font-semibold text-indigo-600">
            {{ minPrix(offre.options) }} CFA
          </span>
        </span>
        <span v-else class="font-semibold text-indigo-600">{{ offre.prix }} MAD</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  offre: Object,
  minPrix: Function
})
</script>
