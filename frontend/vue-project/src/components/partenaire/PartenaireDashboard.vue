<template>
    
  <div class="p-6 space-y-8 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <img
        v-if="partenaire.logo"
        :src="'http://localhost:5000/' + partenaire.logo"
        class="w-16 h-16 object-cover rounded-full shadow"
        alt="Logo partenaire"
      />
      <div class="ml-5">
        <h1 class="text-2xl font-bold text-gray-800  " > Tableau de bord </h1>
        <p class="text-sm text-gray-500">Bienvenue, {{ partenaire.nom }} — gérez vos offres, votre profil et votre performance.</p>
      </div>
      
    </div>

    <!-- Abonnement -->
<AbonnementBadge v-if="partenaire.abonnement" :abonnement="partenaire.abonnement" />

    <!-- Statistiques -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard label="Offres actives" :value="stats.offres" icon="📦" />
      <StatCard label="Vues totales" :value="stats.vues" icon="👁️" />
      <StatCard label="Clics" :value="stats.clics" icon="🖱️" />
      <StatCard label="Favoris" :value="stats.favoris" icon="❤️" />
    </div>

    <!-- Actions rapides -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <ActionCard
        title="Créer une offre"
        description="Ajoutez une nouvelle offre avec photos, prix et options"
        icon="➕"
        @click="goTo('/partenaire/offres/nouvelle')"
      />
      <ActionCard
        title="Modifier mon profil"
        description="Logo, description, réseaux sociaux, localisation"
        icon="🖊️"
        @click="goTo('/partenaire/profil')"
      />
      <ActionCard
        title="Voir les commentaires des offres"
        description="Consultez les retours des utilisateurs sur vos offres"
        icon="💬"
        @click="goTo('/partenaire/commentaires')"
      />
      <ActionCard
        title="Voir mes avis"
        description="Consultez les retours des utilisateurs"
        icon="💬"
        @click="goTo('/partenaire/avis')"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import PartenaireLayout from './PartenaireLayout.vue'
import AbonnementBadge from './AbonnementBadge.vue'
import StatCard from './StatCard.vue'
import ActionCard from './ActionCard.vue'

const partenaire = ref({})
const stats = ref({})
const router = useRouter()

onMounted(async () => {
  const { data: profil } = await api.get('/partenaire/me')
  partenaire.value = profil
  console.log("hhh",partenaire.value)
  const { data: statData } = await api.get('/partenaire/stats')
  stats.value = statData
})

function goTo(path) {
  router.push(path)
}
</script>
