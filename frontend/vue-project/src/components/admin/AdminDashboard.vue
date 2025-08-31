<template>
  <AdminLayout>
    
    <div class="p-6 space-y-8">
      <h1 class="text-3xl font-bold text-gray-800">Tableau de bord</h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <DashboardCard title="Utilisateurs" icon="👥" :count="stats.utilisateurs" />
        <DashboardCard title="Partenaires" icon="🤝" :count="stats.partenaires" />
        <DashboardCard title="Abonnements" icon="🎫" :count="stats.abonnements" />
        <DashboardCard title="Offres" icon="🎁" :count="stats.offres" />
        <DashboardCard title="Secteurs" icon="🏷️" :count="stats.secteurs" />
        <DashboardCard title="Catégories" icon="📁" :count="stats.categories" />
      </div>

      <RecentOffres />
      <RecentPartenaires />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import DashboardCard from '@/components/admin/DashboardCard.vue'
import RecentOffres from './RecentOffres.vue'
import RecentPartenaires from './RecentPartenaires.vue'
import AdminLayout from './AdminLayout.vue'

const stats = ref({ utilisateurs: 0, partenaires: 0, offres: 0, secteurs: 0, categories: 0, abonnements: 0 })

onMounted(async () => {
  const { data } = await api.get('/admin/stats')
  stats.value = data
})
</script>
