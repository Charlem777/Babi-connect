<template>
  <section class="mt-16 px-4">
    <h3 class="text-3xl font-bold text-gray-800 mb-8 text-center">Galerie photos</h3>

    <div class="grid grid-cols-2 gap-4 sm:gap-6 max-w-5xl mx-auto">
      <img
        v-for="(photo, index) in visiblePhotos"
        :key="index"
        :src="photo"
        alt="Photo"
        class="rounded-lg object-cover h-28 sm:h-40 w-full shadow-md hover:scale-105 transition-transform duration-300"
      />
    </div>

    <div v-if="photos.length > 4" class="text-center mt-8">
      <button
        @click="toggleShowAll"
        class="px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition"
      >
        {{ showAll ? 'Réduire' : 'Voir plus' }}
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  photos: Array
})

const showAll = ref(false)
const toggleShowAll = () => (showAll.value = !showAll.value)

const visiblePhotos = computed(() =>
  showAll.value ? props.photos : props.photos.slice(0, 4)
)
</script>
