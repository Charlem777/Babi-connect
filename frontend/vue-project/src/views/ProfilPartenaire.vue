<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <!-- 🧑‍💼 Modern Header with Gradient Background -->
    <div class="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-blue-700">
      <!-- Background Pattern -->
      <div class="absolute inset-0 bg-black/10"></div>
      <div class="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent"></div>
      
      <!-- Content -->
      <div class="relative px-6 pt-16 pb-24 text-center">
        <!-- Logo with modern styling -->
        <div class="mb-8 flex justify-center">
          <div class="relative">
            <img
              :src="'http://localhost:5000/' + partenaire?.logo || '/default-logo.png'"
              alt="Logo"
              class="w-32 h-32 object-cover rounded-3xl border-4 border-white/20 shadow-2xl backdrop-blur-sm"
            />
            <div class="absolute inset-0 rounded-3xl bg-gradient-to-br from-white/10 to-transparent"></div>
          </div>
        </div>

        <!-- Partner Info -->
        <div class="space-y-4 mb-8">
          <h1 class="text-5xl font-bold text-white mb-2 tracking-tight">{{ partenaire?.nom }}</h1>
          <p class="text-blue-100 text-lg font-medium">{{ partenaire?.secteur }} • {{ partenaire?.ville }}</p>
        </div>

        <!-- Status Badge -->
        <div class="mb-8">
          <span
            class="inline-flex items-center px-6 py-3 rounded-full text-white text-sm font-semibold shadow-lg backdrop-blur-sm"
            :class="partenaire?.statut === 'premium' 
              ? 'bg-gradient-to-r from-emerald-400 to-green-500 border border-emerald-300/30' 
              : 'bg-gradient-to-r from-slate-400 to-gray-500 border border-slate-300/30'"
          >
            <svg v-if="partenaire?.statut === 'premium'" class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            {{ partenaire?.statut === 'premium' ? 'Partenaire Premium' : 'Partenaire Standard' }}
          </span>
        </div>

        <!-- CTA Buttons -->
        <div class="flex gap-4 justify-center">
          <ContactPartenaireButton 
            :partenaire="partenaire"
            variant="primary"
            size="base"
            class="inline-flex items-center px-8 py-4 text-lg font-semibold shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300"
          />
          <button
            @click="goToOffres"
            class="inline-flex items-center px-8 py-4 bg-white text-indigo-600 rounded-2xl text-lg font-semibold shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300 backdrop-blur-sm"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
            Voir les offres
          </button>
        </div>

      </div>

      <!-- Wave Separator -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" class="w-full h-16 text-slate-50">
          <path fill="currentColor" d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,64C960,75,1056,85,1152,80C1248,75,1344,53,1392,42.7L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"></path>
        </svg>
      </div>
    </div>

    <!-- Main Content -->
    <div class="relative -mt-8 z-10">
      <!-- About Section -->
      <section class="px-6 py-12 max-w-6xl mx-auto">
        <div class="bg-white rounded-3xl shadow-xl p-8 mb-8">
          <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">À propos de nous</h2>
            <div class="w-24 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mx-auto"></div>
          </div>
          
          <p class="text-gray-600 text-lg leading-relaxed text-center max-w-4xl mx-auto mb-8">
            {{ partenaire?.description }}
          </p>

          <!-- Info Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
            <!-- Contact Card -->
            <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100">
              <div class="flex items-center mb-3">
                <div class="w-10 h-10 bg-blue-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 ml-3">Contact</h3>
              </div>
              <p class="text-gray-600 text-sm">{{ partenaire?.contact || 'Non renseigné' }}</p>
            </div>

            <!-- Date Card -->
            <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-100">
              <div class="flex items-center mb-3">
                <div class="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 ml-3">Membre depuis</h3>
              </div>
              <p class="text-gray-600 text-sm">{{ formatDate(partenaire?.date_inscription) }}</p>
            </div>

            <!-- Website Card -->
            <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-100">
              <div class="flex items-center mb-3">
                <div class="w-10 h-10 bg-purple-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9"/>
                  </svg>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 ml-3">Site web</h3>
              </div>
              <a :href="partenaire?.url" target="_blank" class="text-purple-600 hover:text-purple-700 text-sm font-medium">
                Visiter le site
              </a>
            </div>

            <!-- Location Card -->
            <div class="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-6 border border-orange-100">
              <div class="flex items-center mb-3">
                <div class="w-10 h-10 bg-orange-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 ml-3">Localisation</h3>
              </div>
              <p class="text-gray-600 text-sm">{{ partenaire?.ville }}, {{ partenaire?.commune }}</p>
            </div>
          </div>

          <!-- Social Networks -->
          <div v-if="partenaire?.reseaux" class="mt-8 pt-8 border-t border-gray-100">
            <h3 class="text-center text-lg font-semibold text-gray-900 mb-6">Suivez-nous</h3>
            <div class="flex justify-center gap-4">
              <a v-for="(link, name) in partenaire?.reseaux" :key="name" :href="link" target="_blank" 
                 class="w-12 h-12 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl flex items-center justify-center hover:from-indigo-500 hover:to-purple-500 hover:text-white transition-all duration-300 hover:scale-110">
                <span class="text-sm font-medium">{{ name.charAt(0).toUpperCase() }}</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Gallery Section -->
      <section class="px-6 pb-12 max-w-6xl mx-auto">
        <Galerie :photos="visiblePhotos" />
      </section>

      <!-- Offers Section -->
      <section class="px-6 pb-12 max-w-6xl mx-auto" id="offres">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">Nos offres exclusives</h2>
          <div class="w-24 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mx-auto mb-6"></div>
          <p class="text-gray-600 text-lg max-w-2xl mx-auto">Découvrez notre sélection d'offres soigneusement préparées pour vous</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <OffreCard
            v-for="(offre, index) in visibleOffres"
            :key="index"
            :offre="offre"
            :minPrix="(options) => Math.min(...options.map(o => o.prix))"
            class="transform hover:scale-105 transition-all duration-300"
          />
        </div>

        <div v-if="visibleCount < partenaire?.offres?.length" class="mt-12 text-center">
          <button
            @click="voirPlus"
            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-2xl font-semibold shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
            Voir plus d'offres
          </button>
        </div>
      </section>

      <!-- Reviews Section -->
      <section class="px-6 pb-12 max-w-6xl mx-auto">
        <AvisClient :avisClients="avisClients" :formatDate="formatDate" />
      </section>

      <!-- Location Section -->
      <section class="px-6 pb-16 max-w-6xl mx-auto">
        <div class="bg-white rounded-3xl shadow-xl overflow-hidden">
          <div class="p-8">
            <div class="text-center mb-8">
              <h3 class="text-3xl font-bold text-gray-900 mb-4">Notre localisation</h3>
              <div class="w-24 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mx-auto mb-4"></div>
              <p class="text-gray-600">58 Rue 12, Casablanca, Maroc</p>
            </div>
          </div>
          
          <div class="h-80 bg-gray-100">
            <iframe
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3329.8123456789!2d-7.589843!3d33.573110!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xda7cd123456789%3A0xabcdef123456789!2s58%20Rue%2012%2C%20Casablanca%2C%20Maroc!5e0!3m2!1sfr!2sma!4v1690000000000"
              width="100%"
              height="100%"
              style="border:0;"
              allowfullscreen=""
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
              class="w-full h-full"
            ></iframe>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import OffreCard from '@/components/OffreCard.vue'
import Galerie from '@/components/Galerie.vue'
import AvisClient from '@/components/AvisClient.vue'
import ContactPartenaireButton from '@/components/chat/ContactPartenaireButton.vue'
import beer from '/Users/mac/Babi_connect/frontend/vue-project/src/assets/beer2.jpeg'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()
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
console.log('avisClients:', avisClients)
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

const handleContact = async () => {
  // Vérifier si l'utilisateur est connecté
  if (!authStore.isAuthenticated) {
    showToast('Veuillez vous connecter pour contacter ce partenaire', 'info')
    return
  }
  
  // Vérifier si c'est un client (pas un partenaire qui contacte un autre partenaire)
  if (authStore.role !== 'client') {
    showToast('Seuls les clients peuvent contacter les partenaires', 'info')
    return
  }
  
  try {
    // Créer ou récupérer une conversation avec ce partenaire
    const conversation = await chatStore.createConversation(
      partenaire.value.id,
      `Contact avec ${partenaire.value.nom}`,
      `Bonjour, j'aimerais en savoir plus sur vos services. Pouvez-vous me contacter ?`
    )
    
    // Rediriger vers la conversation
    router.push(`/messages/${conversation.id}`)
    showToast('Conversation créée avec succès', 'success')
    
  } catch (error) {
    console.error('Erreur lors de la création de la conversation:', error)
    showToast('Erreur lors de la création de la conversation', 'error')
  }
}

// Fonction pour afficher les messages toast
const showToast = (message, type = 'info') => {
  const toast = document.createElement('div')
  toast.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg text-white font-medium transition-all duration-300 ${
    type === 'success' ? 'bg-green-500' : 
    type === 'error' ? 'bg-red-500' : 'bg-blue-500'
  }`
  toast.textContent = message
  
  document.body.appendChild(toast)
  
  setTimeout(() => {
    toast.style.transform = 'translateX(0)'
    toast.style.opacity = '1'
  }, 100)
  
  setTimeout(() => {
    toast.style.transform = 'translateX(100%)'
    toast.style.opacity = '0'
    setTimeout(() => {
      if (document.body.contains(toast)) {
        document.body.removeChild(toast)
      }
    }, 300)
  }, 3000)
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
