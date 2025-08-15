<template>
  <nav
    class="fixed bottom-0 w-full flex justify-around items-center shadow-lg bg-cover bg-center border-t border-white/20"
    :style="navStyle"
  >
    <!-- Overlay glass -->
    <div class="absolute inset-0 bg-black/20 backdrop-blur-md"></div>

    <!-- Liens -->
    <div class="relative z-10 flex justify-around w-full">
      <router-link
        v-for="item in menuItems"
        :key="item.name"
        :to="item.route"
        :aria-label="item.name"
        class="flex flex-col items-center p-2 rounded-xl transition-all duration-300"
        :class="isActive(item.route)
          ? 'text-yellow-400 scale-110 bg-white/10 shadow-md'
          : 'text-white hover:text-yellow-300 hover:bg-white/5'"
        :aria-current="isActive(item.route) ? 'page' : null"
      >
        <!-- Icône seulement -->
        <component :is="item.icon" class="w-7 h-7" />
        <!-- Si tu veux garder du texte masqué pour l’accessibilité, dé-commente la ligne suivante -->
        <!-- <span class="sr-only">{{ item.name }}</span> -->
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'
import bgPattern from '@/assets/bground.jpg'

// Icônes Heroicons (solid)
import {
  HomeIcon,
  HeartIcon,
  GlobeAltIcon,
  UserIcon
} from '@heroicons/vue/24/solid'

const route = useRoute()
const isActive = (path) => route.path === path

// Même image de fond que le header + safe area iPhone
const navStyle = {
  backgroundImage: `url(${bgPattern})`,
  paddingTop: '8px',
  paddingBottom: 'calc(8px + env(safe-area-inset-bottom))'
}

const menuItems = [
  { name: 'Accueil',  route: '/',          icon: HomeIcon },
  { name: 'Explorer', route: '/explore',   icon: GlobeAltIcon },

  { name: 'Favoris',  route: '/favorites', icon: HeartIcon },
  { name: 'Profil',   route: '/profile',   icon: UserIcon }
]
</script>

<style scoped>
nav { height: 64px; }
</style>

