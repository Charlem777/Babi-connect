<template>
    <!-- 🧑‍💼 Header Partenaire -->
    <div class="relative w-full bg-neutral-800 border-b border-gray-300 px-6 pt-8 pb-16 text-center flex flex-col items-center gap-4">
      <img
        :src="partenaire?.logo || '/default-logo.png'"
        alt="Logo"
        class="w-24 h-24 object-cover rounded-full border-4 border-blue-100 shadow-md"
      />

      <div>
        <h1 class="text-4xl text-white mb-1">{{ partenaire?.nom }}</h1>
        <p class="text-gray-300 text-sm">{{ partenaire?.secteur }} à {{ partenaire?.ville }}</p>
      </div>

      <span
        class="px-5 py-2 rounded-full text-white text-sm font-semibold shadow-sm"
        :class="partenaire?.statut === 'premium' ? 'bg-gradient-to-r from-green-400 to-green-600' : 'bg-gray-400'"
      >
        {{ partenaire?.statut === 'premium' ? 'Abonné actif' : 'Standard' }}
      </span>

      <button
        @click="goToOffres"
        class="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 bg-blue-500 hover:bg-blue-700 text-white px-6 py-3 rounded-full text-lg font-medium shadow-md transition duration-200"
      >
        Voir les offres
      </button>
    </div>

    <!-- 📝 À propos -->
    <div class="px-6 py-10 rounded-xl  mx-auto">
      <h2 class="text-3xl text-gray-800 mb-4">À propos de nous</h2>
      <p class="text-gray-500 text-lg leading-relaxed mx-auto">
        {{ partenaire?.description }}
      </p>

      <!-- 📍 Infos pratiques -->
      <div class="w-full mt-10 px-4">
        <div class="grid grid-cols-2 gap-4 text-gray-800 text-lg">
          <div class="flex flex-col gap-2">
            <div class="flex items-center gap-2">
              <span>📞</span>
              <span>{{ partenaire?.contact || 'Contact non renseigné' }}</span>
            </div>
            <div class="flex items-center gap-2">
              <span>📅</span>
              <span>{{ formatDate(partenaire?.date_inscription) }}</span>
            </div>
          </div>
          <div class="flex flex-col gap-2 items-end">
            <div class="flex items-center gap-2">
              <span>🌐</span>
              <a :href="partenaire?.url" target="_blank" class="hover:underline">www.siteweb.com</a>
            </div>
            <div class="flex items-center gap-2">
              <span>📍</span>
              <span>{{ partenaire?.ville }} {{ partenaire?.commune }}</span>
            </div>
          </div>
        </div>

        <!-- 🔗 Réseaux sociaux -->
        <div class="mt-6 flex justify-center gap-6">
          <a v-for="(link, name) in partenaire?.reseaux" :key="name" :href="link" target="_blank" class="text-gray-400 hover:text-white">
            <span>{{ name }}</span>
          </a>
        </div>
      </div>

   <!-- 🖼️ Galerie -->
<Galerie :photos="photos" />


    <!-- 🎯 Offres -->
<section class="px-4 py-10 sm:px-6 lg:px-8 max-w-5xl mx-auto" id="offres">
    <h2 class="text-2xl sm:text-3xl font-semibold text-gray-800 mb-6 text-center">Nos offres</h2>

    <div class="grid grid-cols-2 gap-4 sm:gap-6">
      <OffreCard
   v-for="(offre, index) in partenaire?.offres"
      :key="index"
      :offre="offre"
      :minPrix="(options) => Math.min(...options.map(o => o.prix))"
/>
    </div>

    <div v-if="visibleCount < partenaire?.offres?.length" class="mt-8 text-center">
      <button
        @click="voirPlus"
        class="bg-gray-100 hover:bg-gray-200 text-gray-800 px-6 py-2 rounded-full text-sm transition"
      >
        Voir plus
      </button>
    </div>
  </section>

  <AvisClient :avisClients="avisClients" :formatDate="formatDate" />


   
<section class="mt-16 px-6 py-8 max-w-4xl mx-auto bg-white border border-gray-200 rounded-lg">
  <h3 class="text-xl font-semibold text-gray-800 mb-4">📍 Localisation</h3>

  <div class="mb-4">
    <p class="text-gray-700 text-sm">58 Rue 12, Casablanca, Maroc</p>
  </div>

  <div class="w-full h-64 rounded-lg overflow-hidden shadow-sm">
    <iframe
      src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3329.8123456789!2d-7.589843!3d33.573110!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xda7cd123456789%3A0xabcdef123456789!2s58%20Rue%2012%2C%20Casablanca%2C%20Maroc!5e0!3m2!1sfr!2sma!4v1690000000000"
      width="100%"
      height="100%"
      style="border:0;"
      allowfullscreen=""
      loading="lazy"
      referrerpolicy="no-referrer-when-downgrade"
    ></iframe>
  </div>
</section>


  </div>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import OffreCard from '@/components/OffreCard.vue'
import Galerie from '@/components/Galerie.vue'
import AvisClient from '@/components/AvisClient.vue'
import beer from '/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer2.jpeg'
const route = useRoute()
const router = useRouter()
const partenaire = ref(null)
const avisClients = computed(() => {
  return partenaire.value?.avis?.map(a => ({
    nom: a.utilisateur?.nom || 'Anonyme',
    photo: a.utilisateur?.photo || '/default-user.png',
    commentaire: a.commentaire,
    date: a.date,
    note: a.note
  })) || []
})
const photos = [
  new URL('/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer2.jpeg', import.meta.url).href,
  new URL('/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer2.jpeg', import.meta.url).href,
  new URL('/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer2.jpeg', import.meta.url).href,
  new URL('/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer2.jpeg', import.meta.url).href,
    new URL('/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer2.jpeg', import.meta.url).href,

]

const loading = ref(true)
const error = ref(null)
const visibleCount = ref(6)

const visibleOffres = computed(() => {
  return partenaire.value?.offres?.slice(0, visibleCount.value) || []
})

const voirPlus = () => {
  visibleCount.value += 6
}

const goToOffres = () => {
  const el = document.getElementById('offres')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}


const goToOffre = (id) => { router.push(`/offres/${id}`) }

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const minPrix = (options) => {
  return Math.min(...options.map(opt => opt.prix))
}

onMounted(async () => {
  try {
const res = await fetch(`http://localhost:5000/api/partenaires/${route.params.slug}`)    
if (!res.ok) {
      const data = await res.json()
      error.value = data.error || 'Partenaire introuvable'
    } else {
      partenaire.value = await res.json()
      
      console.log('Données partenaire:', partenaire.value)
    }
  } catch (err) {
    error.value = 'Erreur de connexion au serveur'
  } finally {
    loading.value = false
  }
})
const showAll = ref(false)
const visiblePhotos = computed(() => showAll.value ? photos : photos.slice(0, 4))
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}
</style>
