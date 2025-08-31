<template>
  <!-- Bottom Navigation - Mobile uniquement -->
  <nav
    class="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-xl border-t border-gray-200/50 shadow-2xl"
    :style="{ paddingBottom: 'calc(12px + env(safe-area-inset-bottom))' }"
  >
    <!-- Indicateur de page active -->
    <div 
      class="absolute top-0 h-1 bg-gradient-to-r from-orange-500 to-green-500 transition-all duration-500 ease-out rounded-full"
      :style="{ 
        width: `${100 / menuItems.length}%`, 
        left: `${activeIndex * (100 / menuItems.length)}%` 
      }"
    ></div>

    <!-- Menu Items -->
    <div class="flex justify-around items-center px-2 pt-2 pb-3">
      <router-link
        v-for="(item, index) in menuItems"
        :key="item.name"
        :to="item.route"
        :aria-label="item.name"
        class="relative flex flex-col items-center p-3 rounded-2xl transition-all duration-300 group min-w-0 flex-1"
        :class="isActive(item.route)
          ? 'text-orange-600 scale-105'
          : 'text-gray-500 hover:text-orange-500 active:scale-95'"
        @click="setActiveIndex(index)"
      >
        <!-- Badge de notification -->
        <div 
          v-if="item.badge" 
          class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center animate-pulse"
        >
          {{ item.badge }}
        </div>

        <!-- Indicateur d'activité -->
        <div 
          class="absolute -top-1 w-2 h-2 bg-orange-500 rounded-full transition-all duration-300"
          :class="isActive(item.route) ? 'opacity-100 scale-100' : 'opacity-0 scale-0'"
        ></div>

        <!-- Icône avec animation -->
        <div 
          class="relative p-2 rounded-xl transition-all duration-300"
          :class="isActive(item.route) 
            ? 'bg-orange-100 text-orange-600 shadow-lg' 
            : 'group-hover:bg-gray-100 group-active:bg-gray-200'"
        >
          <component 
            :is="item.icon" 
            class="w-6 h-6 transition-all duration-300"
            :class="isActive(item.route) ? 'scale-110' : 'group-hover:scale-105'"
          />
        </div>

        <!-- Label avec animation -->
        <span 
          class="text-xs font-medium mt-1 transition-all duration-300 truncate max-w-full"
          :class="isActive(item.route) 
            ? 'text-orange-600 font-semibold' 
            : 'text-gray-500 group-hover:text-gray-700'"
        >
          {{ item.name }}
        </span>

        <!-- Effet de ripple au clic -->
        <div 
          v-if="rippleIndex === index"
          class="absolute inset-0 bg-orange-500/20 rounded-2xl animate-ping"
          @animationend="rippleIndex = -1"
        ></div>
      </router-link>
    </div>

    <!-- Indicateur de connexion -->
    <div class="absolute top-1 right-4 flex items-center gap-2">
      <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
      <span class="text-xs text-gray-500 font-medium">En ligne</span>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

// Icônes Heroicons
import {
  HomeIcon,
  HeartIcon,
  FireIcon,
  UserIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/vue/24/outline'

import {
  HomeIcon as HomeIconSolid,
  HeartIcon as HeartIconSolid,
  FireIcon as FireIconSolid,
  UserIcon as UserIconSolid,
  ChatBubbleLeftRightIcon as ChatBubbleLeftRightIconSolid
} from '@heroicons/vue/24/solid'

const route = useRoute()
const activeIndex = ref(0)
const rippleIndex = ref(-1)

const isActive = (path) => {
  if (path === '/' && route.path === '/') return true
  if (path !== '/' && route.path.startsWith(path)) return true
  return false
}

const setActiveIndex = (index) => {
  activeIndex.value = index
  rippleIndex.value = index
}

// Menu items avec icônes dynamiques et badges
const menuItems = computed(() => [
  { 
    name: 'Accueil', 
    route: '/', 
    icon: isActive('/') ? HomeIconSolid : HomeIcon,
    badge: null
  },
  { 
    name: 'À la une', 
    route: '/tendances', 
    icon: isActive('/tendances') ? FireIconSolid : FireIcon,
    badge: null
  },
  { 
    name: 'Messages', 
    route: '/messages', 
    icon: isActive('/messages') ? ChatBubbleLeftRightIconSolid : ChatBubbleLeftRightIcon,
    badge: 3 // Exemple de badge
  },
  { 
    name: 'Favoris', 
    route: '/favoris', 
    icon: isActive('/favorites') ? HeartIconSolid : HeartIcon,
    badge: null
  },
  { 
    name: 'Profil', 
    route: '/profile', 
    icon: isActive('/profile') ? UserIconSolid : UserIcon,
    badge: null
  }
])

// Mettre à jour l'index actif quand la route change
watch(() => route.path, () => {
  const currentIndex = menuItems.value.findIndex(item => isActive(item.route))
  if (currentIndex !== -1) {
    activeIndex.value = currentIndex
  }
}, { immediate: true })
</script>

<style scoped>
/* Animation pour l'effet glassmorphism */
nav {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* Animation de pulsation pour les badges */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Effet de brillance au survol */
.group:hover .shine {
  animation: shine 0.6s ease-in-out;
}

@keyframes shine {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Amélioration de l'accessibilité */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
