<template>
  <section class="px-6 pb-12 max-w-6xl mx-auto">
    <!-- Modern Header -->
    <div class="text-center mb-12">
      <h3 class="text-4xl font-bold text-gray-900 mb-4">Galerie photos</h3>
      <div class="w-24 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mx-auto mb-6"></div>
      <p class="text-gray-600 text-lg max-w-2xl mx-auto">Découvrez notre univers à travers ces images</p>
    </div>

    <!-- Modern Gallery Grid -->
    <div class="bg-white rounded-3xl shadow-xl p-8 overflow-hidden">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div
          v-for="(photo, index) in visiblePhotos"
          :key="index"
          class="group relative overflow-hidden rounded-2xl cursor-pointer"
          :class="getImageClass(index)"
          @click="openLightbox(index)"
        >
          <img
            :src="photo"
            :alt="`Photo ${index + 1}`"
            class="w-full h-full object-cover transition-all duration-500 group-hover:scale-110"
          />
          
          <!-- Overlay with hover effect -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300">
            <div class="absolute bottom-4 left-4 right-4">
              <div class="flex items-center justify-between">
                <span class="text-white text-sm font-medium">Photo {{ index + 1 }}</span>
                <div class="w-8 h-8 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Loading shimmer effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 animate-pulse" v-if="!imageLoaded[index]"></div>
        </div>
      </div>

      <!-- Show More Button -->
      <div v-if="photos.length > 8" class="text-center mt-8 pt-8 border-t border-gray-100">
        <button
          @click="toggleShowAll"
          class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-2xl font-semibold shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="showAll ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'"/>
          </svg>
          {{ showAll ? 'Voir moins' : `Voir ${photos.length - 8} photos de plus` }}
        </button>
      </div>
    </div>

    <!-- Lightbox Modal -->
    <Teleport to="body">
      <div
        v-if="lightboxOpen"
        class="fixed inset-0 z-[9999] bg-black/90 backdrop-blur-sm flex items-center justify-center p-4"
        @click="closeLightbox"
      >
        <!-- Modal Content -->
        <div class="relative max-w-4xl max-h-full" @click.stop>
          <!-- Close Button -->
          <button
            @click="closeLightbox"
            class="absolute -top-12 right-0 w-10 h-10 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center text-white hover:bg-white/20 transition-all duration-300 z-10"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>

          <!-- Navigation Buttons -->
          <button
            v-if="currentImageIndex > 0"
            @click="previousImage"
            class="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center text-white hover:bg-white/20 transition-all duration-300 z-10"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>

          <button
            v-if="currentImageIndex < photos.length - 1"
            @click="nextImage"
            class="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center text-white hover:bg-white/20 transition-all duration-300 z-10"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>

          <!-- Main Image -->
          <div class="bg-white rounded-2xl overflow-hidden shadow-2xl">
            <img
              :src="photos[currentImageIndex]"
              :alt="`Photo ${currentImageIndex + 1}`"
              class="w-full h-auto max-h-[80vh] object-contain"
            />
            
            <!-- Image Info -->
            <div class="p-6 bg-gradient-to-r from-gray-50 to-white">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-lg font-semibold text-gray-900">Photo {{ currentImageIndex + 1 }}</h4>
                  <p class="text-gray-600 text-sm">{{ currentImageIndex + 1 }} sur {{ photos.length }}</p>
                </div>
                <div class="flex gap-2">
                  <button class="w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-xl flex items-center justify-center transition-colors">
                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                    </svg>
                  </button>
                  <button class="w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-xl flex items-center justify-center transition-colors">
                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Thumbnails -->
          <div class="flex justify-center mt-6 gap-2 overflow-x-auto pb-2">
            <button
              v-for="(photo, index) in photos"
              :key="`thumb-${index}`"
              @click="currentImageIndex = index"
              class="flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-all duration-300"
              :class="currentImageIndex === index ? 'border-indigo-500 shadow-lg' : 'border-white/20 hover:border-white/40'"
            >
              <img :src="photo" :alt="`Thumbnail ${index + 1}`" class="w-full h-full object-cover" />
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  photos: {
    type: Array,
    default: () => []
  }
})

const showAll = ref(false)
const lightboxOpen = ref(false)
const currentImageIndex = ref(0)
const imageLoaded = ref({})

const toggleShowAll = () => (showAll.value = !showAll.value)

const visiblePhotos = computed(() =>
  showAll.value ? props.photos : props.photos.slice(0, 8)
)

// Masonry-style grid classes
const getImageClass = (index) => {
  const classes = [
    'h-48', // Default height
    'h-64', // Taller
    'h-48', // Default
    'h-56', // Medium
    'h-48', // Default
    'h-64', // Taller
    'h-52', // Medium-small
    'h-48', // Default
  ]
  
  // Special layout for first few images
  if (index === 0) return 'h-64 sm:col-span-2'
  if (index === 1) return 'h-48'
  if (index === 2) return 'h-56'
  if (index === 3) return 'h-48 sm:col-span-2'
  
  return classes[index % classes.length]
}

const openLightbox = (index) => {
  currentImageIndex.value = index
  lightboxOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeLightbox = () => {
  lightboxOpen.value = false
  document.body.style.overflow = 'auto'
}

const nextImage = () => {
  if (currentImageIndex.value < props.photos.length - 1) {
    currentImageIndex.value++
  }
}

const previousImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  }
}

// Keyboard navigation
const handleKeydown = (event) => {
  if (!lightboxOpen.value) return
  
  switch (event.key) {
    case 'Escape':
      closeLightbox()
      break
    case 'ArrowRight':
      nextImage()
      break
    case 'ArrowLeft':
      previousImage()
      break
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  
  // Preload images
  props.photos.forEach((photo, index) => {
    const img = new Image()
    img.onload = () => {
      imageLoaded.value[index] = true
    }
    img.src = photo
  })
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = 'auto'
})
</script>

<style scoped>
/* Custom scrollbar for thumbnails */
.overflow-x-auto::-webkit-scrollbar {
  height: 4px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
