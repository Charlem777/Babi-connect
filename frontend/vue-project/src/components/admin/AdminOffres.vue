<template>
=    <div class="p-6 space-y-6">
      <AdminHeader title="Offres publiées" />

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="offre in offres"
          :key="offre.id"
          class="bg-white p-4 rounded shadow hover:bg-orange-50 transition"
        >
          <RouterLink :to="`/admin/offres/${offre.id}`" class="block space-y-1">
            <h3 class="font-semibold text-gray-800">{{ offre.titre }}</h3>
            <p class="text-sm text-gray-500">{{ offre.ville }} — {{ offre.partenaire.nom }}</p>
            <p class="text-xs text-gray-400">Publié le {{ formatDate(offre.date_publication) }}</p>
            <span
              class="inline-block mt-2 px-2 py-1 text-xs rounded-full"
              :class="offre.est_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
            >
              {{ offre.est_active ? 'Active' : 'Expirée' }}
            </span>
          </RouterLink>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminHeader from '@/components/admin/AdminHeader.vue'

const offres = ref([])

onMounted(async () => {
  const { data } = await api.get('/admin/offres/recentes')
  offres.value = data
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>
