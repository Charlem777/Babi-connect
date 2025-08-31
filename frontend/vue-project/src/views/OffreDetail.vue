<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Image principale -->
    <BanniereOffre :offre="offre" />
    
    <!-- Barre de navigation sticky moderne -->
    <nav class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <ul class="flex overflow-x-auto scrollbar-hide text-sm font-medium text-gray-600">
          <li 
            v-for="section in sections" 
            :key="section.id" 
            class="px-6 py-4 cursor-pointer whitespace-nowrap transition-all duration-300 hover:text-blue-600 relative group" 
            :class="{ 'text-blue-600': activeSection === section.id }"
            @click="scrollToSection(section.id)"
          >
            {{ section.label }}
            <div 
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 transform transition-transform duration-300"
              :class="activeSection === section.id ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-50'"
            ></div>
          </li>
        </ul>
      </div>
    </nav>

    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <transition name="fade-slide" mode="out-in">
        <!-- Carte Partenaire enrichie -->
        <div v-if="offre && offre.partenaire" class="relative mt-6 bg-white rounded-xl shadow-md p-6 space-y-6">
          <!-- Logo + Infos -->
          <router-link :to="`/partenaires/${offre.partenaire?.url}`" class="block hover:shadow-lg transition">
            <div  class="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center">
              <img :src="'http://localhost:5000/' + offre.partenaire.logo" />
            </div>
            <div>
              <h2 class="text-lg font-semibold text-gray-900 mt-2">{{ offre.partenaire.nom }}</h2>
              <p class="text-sm text-gray-500">{{ offre.partenaire.secteur }}</p>
              <p class="text-sm text-gray-500">{{ offre.partenaire.ville }} · {{ offre.partenaire.commune }} · {{ offre.localisation }}</p>
            </div>
          </router-link>

          <!-- Abonné + Caméra -->
          <div  id="partenaire" class="absolute top-4 right-4 bg-green-300 text-green-800 px-3 py-1 rounded-full text-xs font-semibold flex items-center space-x-1 shadow-sm transition-transform duration-300 hover:scale-105">
            <div class="flex items-center space-x-1 text-green-800 font-medium">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"/>
              </svg>
              <span>Abonné</span>
            </div>
            <div class="text-green-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M4 6h11a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2z"/>
              </svg>
            </div>
          </div>
          <!-- Avis -->
          <!-- Avis enrichis -->
          <div v-if="offre.partenaire.avis?.length" class="flex items-center gap-2 mt-2 text-sm text-gray-700">
            <!-- Icônes étoiles -->
            <div class="flex space-x-1 text-yellow-400">
              <template v-for="i in 5" :key="i">
                <svg
                  class="w-4 h-4"
                  :class="{ 'opacity-100': i <= Math.round(moyenneAvis), 'opacity-30': i > Math.round(moyenneAvis) }"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957h4.163c.969 0 1.371 1.24.588 1.81l-3.37 2.448 1.286 3.957c.3.921-.755 1.688-1.54 1.118L10 13.347l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.285-3.957-3.37-2.448c-.783-.57-.38-1.81.588-1.81h4.163l1.286-3.957z"/>
                </svg>
              </template>
            </div>

            <!-- Note moyenne -->
            <span class="font-semibold text-gray-900">{{ moyenneAvis }}/5</span>

            <!-- Nombre d’avis -->
            <span  class="flex items-center gap-1 text-gray-500">
              <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M18 10c0 3.866-3.582 7-8 7s-8-3.134-8-7 3.582-7 8-7 8 3.134 8 7zm-8 4a4 4 0 100-8 4 4 0 000 8z"/>
              </svg>
              {{ offre.partenaire.avis.length }} avis
            </span>
          </div>
          <!-- Description -->
          <div  v-if="offre?.partenaire?.description" class="text-sm text-gray-600">
            <p>{{ offre.partenaire.description }}</p>
          </div>

          <!-- Galerie partenaire -->
          <!-- Galerie partenaire responsive -->
          <div id="galerie" v-if="images.length" class="mt-6">
            <h3 class="text-md font-semibold mb-2 text-gray-800">Galerie du partenaire</h3>

            <!-- Scroll horizontal sur mobile, grille sur desktop -->
            <div class="flex overflow-x-auto space-x-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:overflow-visible snap-x snap-mandatory">
              <div
                v-for="(image, index) in images"
                :key="index"
                class="flex-shrink-0 w-64 sm:w-full h-40 rounded-lg shadow-md overflow-hidden snap-start"
              >
                <img
                  :src="image"
                  alt="Image partenaire"
                  class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                />
              </div>
            </div>
            <div id="details"  class="mt-6 min-h-[200px]" >
              <h3 class="text-md font-semibold mb-3 text-gray-800 flex items-center gap-2 mt-6">
                <svg class="w-4 h-4 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957h4.163c.969 0 1.371 1.24.588 1.81l-3.37 2.448 1.286 3.957c.3.921-.755 1.688-1.54 1.118L10 13.347l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.285-3.957-3.37-2.448c-.783-.57-.38-1.81.588-1.81h4.163l1.286-3.957z"/>
                </svg>
                Détails de l’offre
              </h3>
              <div v-if="offre.description?.length" class="mt-6">
                <p class="text-gray-700 text-sm">{{ offre.description }}</p>
              </div>
              <!-- Détails de l’offre -->
              <div v-if="offre.details?.length" class="mt-5">
                <h3 class="text-md font-semibold mb-3 text-gray-800">Détails de l’offre</h3>
                <ul class="list-disc list-inside text-gray-700 text-sm space-y-1">
                  <li v-for="detail in offre.details" :key="detail">{{ detail }}</li>
                </ul>
              </div>
              <div v-if="offre.participations?.length" class="mt-6">
                <h2 class="text-xl font-bold text-gray-800 mb-4">Commentaires</h2>
              </div>
              <!-- Liste des commentaires -->
              <!-- Section commentaires intégrée -->
              <div id="commentaires" class="mt-6">
                <OffreComments v-if="offre.id" :offre-id="offre.id" />
              </div>
              <!-- Ajout de commentaire -->
              <div class="mt-6 bg-gray-50 p-4 rounded-lg shadow-sm">
                <h3 class="text-md font-semibold text-gray-800 mb-2">Ajouter un commentaire</h3>
                <textarea v-model="nouveauCommentaire" rows="3" class="w-full p-2 border rounded-md text-sm" placeholder="Votre commentaire..."></textarea>
                <button @click="ajouterCommentaire" class="mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                  Envoyer
                </button>
              </div>
            </div>

            <!-- Tags -->
            <div v-if="offre.tags?.length" class="mt-6">
              <h3 class="text-md font-semibold mb-3 text-gray-800">Tags associés</h3>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in offre.tags"
                  :key="tag"
                  class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium hover:bg-blue-200 transition"
                >
                  #{{ tag }}
                </span>
              </div>

            </div>
            <!-- Recommandations -->

            <div :id="'recommandations'" class="mt-6">

              <div v-if="recommandations.length" class="mt-10">
                <h2 class="text-xl font-bold text-gray-800 mb-4">Vous pourriez aussi aimer</h2>
                <div class="overflow-x-auto hide-scrollbar">
                  <div class="flex gap-6">
                    <div
                      v-for="offre in recommandations"
                      :key="offre.id"
                      class="min-w-[260px] max-w-[280px] bg-white rounded-xl shadow-sm relative"
                    >
                      <router-link :to="`/offres/${offre.id}`" class="block">

                        <img
                          :src="offre.image_url"
                          alt="Image offre"
                          class="h-40 w-full object-cover rounded-t-xl"
                        />
                        <div class="absolute top-2 left-2 bg-indigo-600 text-white text-xs px-2 py-1 rounded-full">
                          Similaire
                        </div>
                        <div class="p-4">
                          <h3 class="text-sm font-semibold text-gray-900 truncate">{{ offre.titre }}</h3>
                          <p class="text-xs text-gray-500">{{ offre.partenaire.nom }}</p>
                          <div class="mt-2 text-xs text-gray-600">{{ offre.commune }}</div>
                        </div>
                      </router-link>

                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </transition>
    </div>
  </div>
</template>

<script setup> 
import { ref, onMounted,onUnmounted, computed,watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import BanniereOffre from '@/components/BanniereOffre.vue'
import OffreCardAdapter from '@/components/OffreCardAdapter.vue'
import RecommandationsSlider from '@/components/RecommandationsSlider.vue'
import OffreComments from '@/components/OffreComments.vue'
const recommandations = ref([])

const route = useRoute()
const offre = ref({
  participations: [],
  partenaire: {},
  details: [],
  tags: []
})
const sections = [
  { id: 'partenaire', label: 'Partenaire' },
  { id: 'galerie', label: 'Galerie' },
  { id: 'details', label: 'Détails' },
  { id: 'commentaires', label: 'Commentaires' },
  { id: 'recommandations', label: 'recommandations' }

]

watch(() => route.params.id, async (newId) => {
  window.scrollTo({ top: 0, behavior: 'smooth' })

  await chargerOffre(newId)

})
const chargerOffre = async (id) => {
  try {
    const { data } = await axios.get(`http://localhost:5000/api/offres/${id}`)
    offre.value = data
    // recharge aussi les recommandations si besoin
    const recoRes = await axios.get(`http://localhost:5000/api/offres/${id}/recommandations`)
    recommandations.value = recoRes.data
  } catch (error) {
    console.error("Erreur lors du chargement de l'offre :", error)
  }
}

onMounted(async () => {
  await chargerOffre(route.params.id)
})

// Images locales (pas besoin de les charger depuis la base de données)
const images = [
  new URL('../assets/images (1).jpeg', import.meta.url).href,
  new URL('../assets/360_F_187293579_mPGjfd0YI3lAICz473ORPEPJ3rpFcPIE.jpg', import.meta.url).href,
  new URL('../assets/images.jpeg', import.meta.url).href
]

const currentIndex = ref(0)

function next() {
  currentIndex.value = (currentIndex.value + 1) % images.length
}

function prev() {
  currentIndex.value = (currentIndex.value - 1 + images.length) % images.length
}

const nouveauCommentaire = ref('')

const likes = ref([])

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

function likeComment(index) {
  likes.value[index]++
}

const commentairesAffiches = ref(2)
const voirTout = ref(false)

const toggleCommentaires = () => {
  commentairesAffiches.value = voirTout.value
  ? (offre.value.participations?.length || 0)
  : 2
}

const commentairesVisibles = computed(() => {
  return offre.value.participations?.slice(0, commentairesAffiches.value) || []
})

const moyenneAvis = computed(() => {
  const avis = offre.value?.partenaire?.avis || []
  if (!avis.length) return 0
  const total = avis.reduce((sum, a) => sum + a.note, 0)
  return (total / avis.length).toFixed(1)
})

const activeSection = ref('partenaire')

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const handleScroll = () => {
  for (const section of sections) {
    const el = document.getElementById(section.id)
    if (el) {
      const rect = el.getBoundingClientRect()
      if (rect.top <= 120 && rect.bottom >= 120) {
        activeSection.value = section.id
        break
      }
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

</script>
<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.4s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
[id] {
  scroll-margin-top: 80px;
}
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

</style>
