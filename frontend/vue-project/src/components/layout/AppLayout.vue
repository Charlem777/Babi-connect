<template>
  <!-- Top Navigation Bar - Sticky comme Shein -->
  <nav class="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center h-12 lg:h-16">
        <!-- Logo et marque - Position fixe à gauche -->
        <div class="flex items-center gap-2 lg:gap-3 flex-shrink-0">
          <div class="text-lg lg:text-2xl">🐘</div>
          <div class="flex items-center">
            <h1 class="text-lg lg:text-xl xl:text-2xl font-bold">
              <span class="text-orange-600">Babi</span>
              <span class="text-green-600">Connect</span>
            </h1>
            <span class="ml-1 lg:ml-2 text-xs bg-orange-100 text-orange-600 px-1.5 lg:px-2 py-0.5 lg:py-1 rounded-full font-medium">🇨🇮</span>
          </div>
        </div>

        <!-- Section centrale - Recherche et sélecteur -->
        <div class="flex-1 flex items-center justify-center px-4 lg:px-8">
          <!-- Sélecteur de secteur et recherche - Desktop -->
          <div class="hidden lg:flex items-center gap-4 w-full max-w-4xl">
            <div class="w-48 flex-shrink-0">
              <SectorSelect
                v-model="filters.secteur_slug"
                @change="onSecteurChange"
              />
            </div>
            <div class="flex-1 min-w-0">
              <SearchSuggest />
            </div>
          </div>
        </div>

        <!-- Actions utilisateur - Largeur fixe -->
        <div class="flex items-center gap-3 lg:gap-4 flex-shrink-0">
          <!-- Boutons d'action principaux -->
          

          <!-- Navigation Desktop uniquement -->
          <div class="hidden lg:flex items-center gap-2 border-l border-gray-200 pl-4">
            <!-- Messages -->
            <div class="relative group" v-if="isUserAuthenticated">
              <RouterLink 
                to="/messages" 
                class="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-orange-600 transition-colors rounded-lg hover:bg-orange-50 relative"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
                <span class="hidden xl:inline">Messages</span>
                <!-- Badge de notification -->
                <span class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">3</span>
              </RouterLink>
              
              <!-- Dropdown Messages Preview -->
              <div class="absolute right-0 top-full mt-2 w-80 bg-white rounded-xl shadow-xl border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-[60]">
                <div class="p-4 border-b border-gray-100">
                  <h3 class="font-semibold text-gray-900">Messages récents</h3>
                </div>
                <div class="max-h-64 overflow-y-auto">
                  <div class="p-3 hover:bg-gray-50 border-b border-gray-100 cursor-pointer">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                        <span class="text-orange-600 font-semibold">JD</span>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">Jean Dupont</p>
                        <p class="text-xs text-gray-500 truncate">Merci pour votre service...</p>
                      </div>
                      <div class="text-xs text-gray-400">2min</div>
                    </div>
                  </div>
                  <div class="p-3 hover:bg-gray-50 border-b border-gray-100 cursor-pointer">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                        <span class="text-green-600 font-semibold">AM</span>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">Aya Mensah</p>
                        <p class="text-xs text-gray-500 truncate">Disponible demain ?</p>
                      </div>
                      <div class="text-xs text-gray-400">1h</div>
                    </div>
                  </div>
                </div>
                <div class="p-3 text-center border-t border-gray-100">
                  <RouterLink to="/messages" class="text-sm text-orange-600 hover:text-orange-700 font-medium">
                    Voir tous les messages
                  </RouterLink>
                </div>
              </div>
            </div>

            <!-- Messages pour invités - demande connexion -->
            <button 
              v-else
              @click="showLoginRequired"
              class="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-orange-600 transition-colors rounded-lg hover:bg-orange-50 relative"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
              <span class="hidden xl:inline">Messages</span>
            </button>

            <!-- Favoris -->
            <RouterLink 
              to="/favoris" 
              class="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-orange-600 transition-colors rounded-lg hover:bg-orange-50"
              v-if="isUserAuthenticated"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
              <span class="hidden xl:inline">Favoris</span>
            </RouterLink>

            <!-- Séparateur -->
            <div class="w-px h-6 bg-gray-200 mx-2"></div>

            <!-- Profil avec dropdown -->
            <div class="relative group" v-if="isUserAuthenticated">
              <button class="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-orange-600 transition-colors rounded-lg hover:bg-orange-50">
                <div class="w-8 h-8 bg-gradient-to-br from-orange-500 to-green-500 rounded-full flex items-center justify-center mr-2">
                  <span class="text-white font-semibold text-sm">{{ getInitials() }}</span>
                </div>
                <span class="hidden xl:inline">{{ getUserName() }}</span>
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>
              
              <!-- Dropdown Profil -->
              <div class="absolute right-0 top-full mt-2 w-64 bg-white rounded-xl shadow-xl border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-[60]">
                <div class="p-4 border-b border-gray-100">
                  <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-gradient-to-br from-orange-500 to-green-500 rounded-full flex items-center justify-center">
                      <span class="text-white font-semibold">{{ getInitials() }}</span>
                    </div>
                    <div>
                      <p class="font-semibold text-gray-900">{{ getUserName() }}</p>
                      <p class="text-sm text-gray-500">{{ currentUser.email }}</p>
                    </div>
                  </div>
                </div>
                <div class="py-2">
                  <RouterLink to="/profile" class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                    Mon Profil
                  </RouterLink>
                  <RouterLink to="/settings" class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    Paramètres
                  </RouterLink>
                  <div class="border-t border-gray-100 my-2"></div>
                  <button class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50" @click="handleLogout">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                    </svg>
                    Déconnexion
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Connexion (visible si non connecté) -->
          <RouterLink 
            to="/login" 
            class="hidden lg:flex items-center px-4 py-2 text-sm font-medium text-gray-700 hover:text-orange-600 transition-colors rounded-lg hover:bg-orange-50 border-l border-gray-200 pl-4"
            v-if="!isUserAuthenticated"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Connexion
          </RouterLink>

          <!-- Menu mobile -->
          <button class="lg:hidden p-1.5 text-gray-600 hover:text-orange-600 rounded-lg hover:bg-gray-100">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Sélecteur et recherche mobile/tablet -->
      <div class="lg:hidden pb-2 lg:pb-3 space-y-2 lg:space-y-3">
        <SectorSelect
          v-model="filters.secteur_slug"
          @change="onSecteurChange"
        />
        <SearchSuggest />
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class=" hero-bg bg-gradient-to-br from-orange-50 via-green-50 to-yellow-50 py-4 lg:py-8 xl:py-12">
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-4 lg:mb-8 xl:mb-12 animate-fadeInUp">
        <h2 class="text-xl lg:text-2xl xl:text-4xl 2xl:text-5xl font-bold text-gray-900 mb-2 lg:mb-4 xl:mb-6">
          Découvrez les meilleurs 
          <span class="relative inline-block text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-green-600 shimmer-text">
            services ivoiriens
          </span>
        </h2>
        <p class="text-sm lg:text-base xl:text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Connectez-vous avec des professionnels de confiance partout en Côte d'Ivoire
        </p>
      </div>

      <!-- Stats rapides -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4 xl:gap-8 max-w-5xl mx-auto">
        <div class="text-center p-3 lg:p-4 xl:p-6 bg-white/70 backdrop-blur-sm rounded-xl border border-white/30 hover:bg-white/80 transition-all duration-300">
          <div class="text-lg lg:text-xl xl:text-3xl font-bold text-orange-600 mb-0.5 lg:mb-1">1000+</div>
          <div class="text-xs lg:text-sm text-gray-600 font-medium">Partenaires</div>
        </div>
        <div class="text-center p-3 lg:p-4 xl:p-6 bg-white/70 backdrop-blur-sm rounded-xl border border-white/30 hover:bg-white/80 transition-all duration-300">
          <div class="text-lg lg:text-xl xl:text-3xl font-bold text-green-600 mb-0.5 lg:mb-1">5000+</div>
          <div class="text-xs lg:text-sm text-gray-600 font-medium">Services</div>
        </div>
        <div class="text-center p-3 lg:p-4 xl:p-6 bg-white/70 backdrop-blur-sm rounded-xl border border-white/30 hover:bg-white/80 transition-all duration-300">
          <div class="text-lg lg:text-xl xl:text-3xl font-bold text-yellow-600 mb-0.5 lg:mb-1">50+</div>
          <div class="text-xs lg:text-sm text-gray-600 font-medium">Villes</div>
        </div>
        <div class="text-center p-3 lg:p-4 xl:p-6 bg-white/70 backdrop-blur-sm rounded-xl border border-white/30 hover:bg-white/80 transition-all duration-300">
          <div class="text-lg lg:text-xl xl:text-3xl font-bold text-orange-600 mb-0.5 lg:mb-1">4.8★</div>
          <div class="text-xs lg:text-sm text-gray-600 font-medium">Satisfaction</div>
        </div>
      </div>
    </div>
  </section>
  
  <!-- CategoryNav reste sticky -->
  <CategoryNav
    :secteurSlug="filters.secteur_slug"
    v-model="filters.categorie_slug"
    @change="onCategorieChange"
  />

  <!-- Contenu principal -->
  <main class="min-h-screen bg-gray-50">
    <slot :filters="filters" />
  </main>

  <!-- Footer professionnel -->
  <footer class="bg-white border-t border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Marque -->
        <div class="md:col-span-1">
          <div class="flex items-center gap-2 mb-4">
            <div class="text-2xl">🐘</div>
            <h3 class="text-xl font-bold">
              <span class="text-orange-600">Babi</span>
              <span class="text-green-600">Connect</span>
            </h3>
          </div>
          <p class="text-gray-600 text-sm mb-4">
            🇨🇮 La plateforme qui unit les Ivoiriens et valorise l'expertise locale.
          </p>
          <RouterLink 
            to="/devenir-partenaire" 
            class="flex items-center px-3 lg:px-4 py-1.5 lg:py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white text-xs lg:text-sm font-semibold rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all shadow-sm hover:shadow-md"
          >
            <svg class="w-3 lg:w-4 h-3 lg:h-4 mr-1 lg:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span class="hidden sm:inline">Devenir </span>Partenaire
          </RouterLink>
          <div class="flex gap-3">
            <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 text-sm">f</div>
            <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 text-sm">t</div>
            <div class="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center text-yellow-600 text-sm">i</div>
          </div>
        </div>

        <!-- Services -->
        <div>
          <h4 class="font-semibold text-gray-900 mb-4">Services</h4>
          <ul class="space-y-2 text-sm text-gray-600">
            <li><a href="#" class="hover:text-orange-600">Événementiel</a></li>
            <li><a href="#" class="hover:text-orange-600">Beauté & Bien-être</a></li>
            <li><a href="#" class="hover:text-orange-600">Restauration</a></li>
            <li><a href="#" class="hover:text-orange-600">Services Pro</a></li>
          </ul>
        </div>

        <!-- Support -->
        <div>
          <h4 class="font-semibold text-gray-900 mb-4">Support</h4>
          <ul class="space-y-2 text-sm text-gray-600">
            <li><a href="#" class="hover:text-orange-600">Centre d'aide</a></li>
            <li><a href="#" class="hover:text-orange-600">Contact</a></li>
            <li><a href="#" class="hover:text-orange-600">Conditions</a></li>
            <li><a href="#" class="hover:text-orange-600">Confidentialité</a></li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="font-semibold text-gray-900 mb-4">Contact</h4>
          <div class="space-y-2 text-sm text-gray-600">
            <p>📧 contact@babiconnect.ci</p>
            <p>📞 +225 XX XX XX XX</p>
            <p>📍 Abidjan, Côte d'Ivoire</p>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-200 mt-8 pt-8 text-center text-sm text-gray-500">
        <p>© 2025 <span class="font-semibold text-orange-600">BABI CONNECT</span> - Tous droits réservés</p>
      </div>
    </div>
  </footer>
  
  <BottomNav/>
</template>

<script setup>
import { reactive, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from '@/stores/auth';
import { useChatStore } from '@/stores/chat';
import SectorSelect from "@/components/SectorSelect.vue";
import CategoryNav from "@/components/CategoryNav.vue";
import BottomNav from "../BottomNav.vue";
import SearchSuggest from "../SearchSuggest.vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const chatStore = useChatStore();

const filters = reactive({
  secteur_slug: route.query.secteur_slug || null,
  categorie_slug: route.query.categorie_slug || null,
});

// Force reactive computed properties
const isUserAuthenticated = computed(() => {
  const result = authStore.isAuthenticated
  console.log('🔄 AppLayout - isUserAuthenticated computed:', result, 'role:', authStore.role)
  return result
})

const currentUser = computed(() => {
  const user = authStore.user
  console.log('🔄 AppLayout - currentUser computed:', user?.nom || user?.name)
  return user
})

const userRole = computed(() => {
  const role = authStore.role
  console.log('🔄 AppLayout - userRole computed:', role)
  return role
})

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

const handleLogout = async () => {
  try {
    await authStore.logout()
    showToast('Déconnexion réussie', 'success')
  } catch (error) {
    console.error('Erreur lors de la déconnexion:', error)
    showToast('Erreur lors de la déconnexion', 'error')
  }
  router.push('/')
}

const getInitials = () => {
  const user = currentUser.value
  if (user) {
    const nom = user.nom || user.name
    return nom.charAt(0).toUpperCase()
  }
  return 'U'
}

const getUserName = () => {
  const user = currentUser.value
  if (user) {
    return user.nom || user.name
  }
  return 'Utilisateur'
}

// Debug: surveiller les changements d'état d'authentification
watch(() => isUserAuthenticated.value, (newValue, oldValue) => {
  console.log('🔄 AppLayout - Auth state changed:', {
    from: oldValue,
    to: newValue,
    role: userRole.value,
    user: currentUser.value?.nom || currentUser.value?.name,
    token: !!authStore.token
  })
  
  if (newValue && !oldValue && currentUser.value) {
    const userName = currentUser.value.nom || currentUser.value.name || 'Utilisateur'
    showToast(`Bienvenue ${userName} !`, 'success')
  }
})

function onSecteurChange(slug) {
  filters.secteur_slug = slug;
  filters.categorie_slug = null;

  if (route.path !== "/offres") {
    router.push({
      path: "/offres",
      query: { secteur_slug: slug }
    });
  } else {
    updateUrl();
  }
}

function onCategorieChange(slug) {
  filters.categorie_slug = slug;

  router.push({
    path: "/offres",
    query: {
      secteur_slug: filters.secteur_slug || undefined,
      categorie_slug: slug || undefined
    }
  }).then(() => {
    window.scrollTo({ top: 0, behavior: "smooth" })
  });
}

function updateUrl() {
  router.replace({
    path: route.path,
    query: {
      secteur_slug: filters.secteur_slug || undefined,
      categorie_slug: filters.categorie_slug || undefined,
    },
  });
}

function showLoginRequired() {
  showToast('Veuillez vous connecter pour accéder à cette fonctionnalité', 'info')
}
</script>
<style>
@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fadeInUp {
  animation: fadeInUp 0.8s ease-out forwards;
}
.shimmer-text::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 200%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s infinite;
}
@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  100% { background-position: 100% 50%; }
}
.hero-bg {
  background: linear-gradient(270deg, #f6ad55, #68d391, #f6e05e);
  background-size: 600% 600%;
  animation: gradientShift 15s ease infinite;
}


</style>
