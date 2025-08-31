<template>
    <div class="p-6 space-y-6">
<AdminHeader
  title="Gesion des Partenaires"
  subtitle="Ajoutez, modifiez ou supprimez les partenaires"
  icon="🤝"
  />
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="p in partenaires"
          :key="p.id"
          class="bg-white p-4 rounded shadow flex items-center gap-4 hover:bg-orange-50 transition"
        >
          <img :src="p.logo" alt="Logo" class="w-12 h-12 rounded-full object-cover" v-if="p.logo" />
          <div>
            <h3 class="font-semibold text-gray-800">{{ p.nom }}</h3>
            <p class="text-sm text-gray-500">
              {{ p.ville }} — <span class="font-medium">{{ p.secteur?.nom || 'Secteur inconnu' }}</span><br>
              Catégorie : <span class="italic">{{ p.categorie?.nom || 'N/A' }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminHeader from '@/components/admin/AdminHeader.vue'

const partenaires = ref([])

onMounted(async () => {
  const { data } = await api.get('/admin/partenaires/recent')
  partenaires.value = data
})
</script>
