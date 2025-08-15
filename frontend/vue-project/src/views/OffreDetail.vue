<template>
  <div>
    <!-- Image principale -->
    <BanniereOffre :offre="offre" />

   <!-- Carte Partenaire enrichie -->
<div v-if="offre && offre.partenaire" class="relative mt-6 bg-white rounded-xl shadow-md p-6 space-y-6">
  <!-- Logo + Infos -->
  <div class="flex items-center space-x-4">
    <div class="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center">
      <img src="../assets/depositphotos_723371862-stock-photo-sail-ship-logo-design-elements.jpg" alt="Logo partenaire" class="w-12 h-12 object-contain" />
    </div>
    <div>
      <h2 class="text-lg font-semibold text-gray-900">{{ offre.partenaire.nom }}</h2>
      <p class="text-sm text-gray-500">{{ offre.partenaire.secteur }}</p>
      <p class="text-sm text-gray-500">{{ offre.partenaire.ville }} · {{ offre.partenaire.commune }} · {{ offre.localisation }} </p>

    </div>
  </div>

  <!-- Abonné + Caméra -->
  <div class="absolute top-4 right-4 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold flex items-center space-x-1 shadow-sm transition-transform duration-300 hover:scale-105"
>
    <div class="flex items-center space-x-1 text-blue-600 font-medium">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"/>
      </svg>
      <span>Abonné</span>
    </div>
    <div class="text-blue-600">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M4 6h11a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2z"/>
      </svg>
    </div>
  </div>

  <!-- Description -->
  <div v-if="offre?.partenaire?.description" class="text-sm text-gray-600">
    <p>{{ offre.partenaire.description }}</p>
  </div>

  <!-- Avis -->
  <div class="flex items-center space-x-2">
    <div class="flex space-x-1 text-orange-400">
      <template v-for="i in 5">
        <svg v-if="i <= Math.round(offre.partenaire.note)" :key="i" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957h4.163c.969 0 1.371 1.24.588 1.81l-3.37 2.448 1.286 3.957c.3.921-.755 1.688-1.54 1.118L10 13.347l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.285-3.957-3.37-2.448c-.783-.57-.38-1.81.588-1.81h4.163l1.286-3.957z"/>
        </svg>
      </template>
    </div>
    <span class="font-semibold text-gray-800">{{ offre.partenaire.note }}</span>
    <span class="text-gray-500">(avis)</span>
  </div>

  <!-- Galerie partenaire -->
  <!-- Galerie partenaire responsive -->
<div v-if="images.length" class="mt-6">
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
<h3 class="text-md font-semibold mb-3 text-gray-800 flex items-center gap-2 mt-6">
  <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957h4.163c.969 0 1.371 1.24.588 1.81l-3.37 2.448 1.286 3.957c.3.921-.755 1.688-1.54 1.118L10 13.347l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.285-3.957-3.37-2.448c-.783-.57-.38-1.81.588-1.81h4.163l1.286-3.957z"/>
  </svg>
  Détails de l’offre
</h3>

<!-- Détails de l’offre -->
<div v-if="offre.details?.length" class="mt-8">
  <h3 class="text-md font-semibold mb-3 text-gray-800">Détails de l’offre</h3>
  <ul class="list-disc list-inside text-gray-700 text-sm space-y-1">
    <li v-for="detail in offre.details" :key="detail">{{ detail }}</li>
  </ul>
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
 
 <!-- Commentaires -->
    <!-- Section Commentaires enrichie -->
<div v-if="offre.participations?.length" class="mt-10">
  <h2 class="text-xl font-bold text-gray-800 mb-4">Commentaires</h2>

  <!-- Liste des commentaires -->
  <transition-group name="fade" tag="div" class="space-y-4">
    <div
      v-for="(commentaire, index) in offre.participations"
      :key="index"
      class="bg-white rounded-lg shadow-sm p-4 flex flex-col sm:flex-row sm:items-start gap-4"
    >
      <!-- Avatar -->
      <div class="flex-shrink-0 w-10 h-10 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center font-bold text-sm">
        {{ commentaire.utilisateur.nom.charAt(0).toUpperCase() }}
      </div>

      <!-- Contenu -->
      <div class="flex-1">
        <div class="flex justify-between items-center mb-1">
          <h3 class="text-sm font-semibold text-gray-900">{{ commentaire.utilisateur.nom }}</h3>
          <p class="text-xs text-gray-500">{{ formatDate(commentaire.date) }}</p>
        </div>
        <p class="text-gray-700 text-sm leading-relaxed mb-2">
          {{ commentaire.commentaire }}
        </p>

        <!-- Actions -->
        <div class="flex items-center gap-4 text-sm text-gray-500">
          <button @click="likeComment(index)" class="flex items-center gap-1 hover:text-blue-600 transition">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
            </svg>
            J’aime ({{ likes[index] }})
          </button>
          <button class="hover:text-blue-600 transition">Répondre</button>
        </div>

        <!-- Réponses (structure prête) -->
        <div v-if="commentaire.reponses?.length" class="mt-3 space-y-2 pl-4 border-l border-gray-200">
          <div
            v-for="(reponse, rIndex) in commentaire.reponses"
            :key="rIndex"
            class="text-sm text-gray-700"
          >
            <strong>{{ reponse.utilisateur.nom }} :</strong> {{ reponse.commentaire }}
          </div>
        </div>
      </div>
    </div>
  </transition-group>

  <!-- Ajout de commentaire -->
  <div class="mt-6 bg-gray-50 p-4 rounded-lg shadow-sm">
    <h3 class="text-md font-semibold text-gray-800 mb-2">Ajouter un commentaire</h3>
    <textarea v-model="nouveauCommentaire" rows="3" class="w-full p-2 border rounded-md text-sm" placeholder="Votre commentaire..."></textarea>
    <button @click="ajouterCommentaire" class="mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
      Envoyer
    </button>
  </div>
</div>

    </div>


</div>

  <!-- Détails de l’offre -->
  <div v-if="offre.details?.length" class="mt-6">
    <h3 class="text-md font-semibold mb-2 text-gray-800">Détails de l’offre</h3>
    <ul class="list-disc list-inside text-gray-700 text-sm">
      <li v-for="detail in offre.details" :key="detail">{{ detail }}</li>
    </ul>
  </div>
</div>    

]    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import BanniereOffre from '@/components/BanniereOffre.vue'

const route = useRoute()
const offre = ref({})

onMounted(async () => {
  const { data } = await axios.get(`http://localhost:5000/api/offres/${route.params.id}`)
  offre.value = data
  likes.value = data.participations?.map(() => 0) || []
  console.log('Offre chargée j:', offre.value)
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

function ajouterCommentaire() {
  if (!nouveauCommentaire.value.trim()) return
  const nouveau = {
    commentaire: nouveauCommentaire.value,
    date: new Date().toISOString(),
    utilisateur: { nom: 'Vous' },
    reponses: []
  }
  offre.value.participations.push(nouveau)
  likes.value.push(0)
  nouveauCommentaire.value = ''
}


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
</style>
