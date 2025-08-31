<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-white to-orange-100 flex font-sans relative">
    <!-- Backdrop mobile -->
    <div
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-black bg-opacity-30 z-30 md:hidden"
    ></div>

    <!-- Toggle button mobile -->
    <button
      @click="sidebarOpen = !sidebarOpen"
      class="md:hidden fixed top-4 left-4 z-50 bg-white p-2 rounded-full shadow"
    >
      <span class="text-xl">☰</span>
    </button>

    <!-- Sidebar -->
    <aside
      :class="[
        'bg-white shadow-xl p-6 space-y-8 border-r border-orange-100 fixed top-0 left-0 h-full z-40 transition-transform duration-300',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'md:relative md:translate-x-0 md:flex md:flex-col md:w-72'
      ]"
    >
      <!-- Partenaire info -->
      <div class="space-y-4 pt-10">
        <div class="flex items-center gap-4">
          <img
            v-if="partenaire.logo"
            :src="'http://localhost:5000/' + partenaire.logo"
            class="w-12 h-12 object-cover rounded-full border border-blacck-300"
            alt="Logo"
          />
          <div>
            <h2 class="text-xl font-bold text-gray-800">{{ partenaire.nom }}</h2>
            <p class="text-xs text-black-400 uppercase tracking-wide">Partenaire</p>
          </div>
        </div>

        <!-- Navigation -->
        <nav class="space-y-3 text-sm">
          <RouterLink to="/partenaire/dashboard" class="nav-link">🏠 <span>Tableau de bord</span></RouterLink>
          <RouterLink to="/partenaire/profil" class="nav-link">🖊️ <span>Profil</span></RouterLink>
          <RouterLink to="/partenaire/offres" class="nav-link">📦 <span>Mes offres</span></RouterLink>
          <RouterLink to="/partenaire/offres/nouvelle" class="nav-link">➕ <span>Nouvelle offre</span></RouterLink>
          <RouterLink to="/partenaire/messages" class="nav-link">💬 <span>Messages</span></RouterLink>
          <RouterLink to="/partenaire/avis" class="nav-link">⭐ <span>Avis</span></RouterLink>
          <RouterLink to="/partenaire/stats" class="nav-link">📊 <span>Statistiques</span></RouterLink>
        </nav>
      </div>

      <!-- Footer -->
      <div class="text-xs text-gray-400 text-center">
        &copy; Babi Connect {{ new Date().getFullYear() }}
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-4 md:p-8 overflow-y-auto transition-all duration-300">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const partenaire = ref({})
const sidebarOpen = ref(false)

onMounted(async () => {
  const { data } = await api.get('/partenaire/me')
  partenaire.value = data
})
</script>

<style scoped>
.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  border-radius: 0.5rem;
  color: #444;
  font-weight: 500;
  transition: all 0.2s ease-in-out;
}
.nav-link:hover {
  background-color: #fef3c7;
  color: #d97706;
}
.nav-link.router-link-exact-active {
  background-color: #fde68a;
  color: #b45309;
  font-weight: 600;
}
</style>
