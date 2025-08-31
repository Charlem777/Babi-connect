<template>
  <div class="flex h-screen bg-gray-100 relative">
    <!-- Sidebar (responsive) -->
    <aside
      :class="[
        'fixed top-0 left-0 h-full w-64 bg-gray-900 text-white p-6 space-y-6 z-40 transition-transform duration-500 ease-in-out',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'md:static md:translate-x-0'
      ]"
    >
      <h1 class="text-xl font-bold tracking-wide">🛠️ Admin Panel</h1>
      <nav class="space-y-4">
        <NavItem to="/admin/dashboard" icon="📊" label="Dashboard" />
        <NavItem to="/admin/offres" icon="🎁" label="Offres" />
        <NavItem to="/admin/partenaires" icon="🤝" label="Partenaires" />
        <NavItem to="/admin/abonnements" icon="📫" label="Abonnements" />
        <NavItem to="/admin/categories" icon="📂" label="Catégories" />
        <NavItem to="/admin/secteurs" icon="⭐️" label="Secteurs" />
      </nav>
    </aside>

    <!-- Overlay for mobile -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden"
      @click="sidebarOpen = false"
    ></div>

    <!-- Main content -->
    <main class="flex-1 p-6 overflow-y-auto">
      <!-- Mobile header -->
      <div class="md:hidden flex items-center justify-between mb-4">
        <button @click="sidebarOpen = true" class="text-gray-700 text-2xl">
          ☰
        </button>
        <h2 class="text-lg font-semibold">Admin Panel</h2>
      </div>

      <slot />
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavItem from './NavItem.vue'

const sidebarOpen = ref(false)
</script>
