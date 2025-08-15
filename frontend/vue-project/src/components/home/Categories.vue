<template>
  <section class="py-16 bg-white">
    <div class="text-center mb-10">
      <h2 class="text-3xl font-bold text-indigo-700">Secteurs d’activités</h2>
      <p class="text-gray-600 mt-2">Explore ce que BABI_CONNECT peut t’offrir</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 max-w-6xl mx-auto px-6">
      <div v-for="category in categories" :key="category.name" class="flex flex-col items-center text-center p-6 border rounded-lg hover:shadow-lg transition">
        <component :is="category.icon" class="w-10 h-10 text-indigo-600 mb-4" />
        <h3 class="text-xl font-semibold text-gray-800 mb-2">{{ category.name }}</h3>
        <p class="text-gray-500 text-sm">{{ category.description }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { BuildingStorefrontIcon, HeartIcon, WrenchScrewdriverIcon } from '@heroicons/vue/24/solid'

const categories = [
  {
    name: 'Restauration',
    description: 'Restaurants, snacks, food-trucks…',
    icon: BuildingStorefrontIcon,
  },
  {
    name: 'Bien-être',
    description: 'Spas, coiffure, soins naturels…',
    icon: HeartIcon,
  },
  {
    name: 'Services',
    description: 'Réparation, maintenance, assistance…',
    icon: WrenchScrewdriverIcon,
  },
]
</script>
