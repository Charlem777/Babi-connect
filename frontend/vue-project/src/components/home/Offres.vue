<script setup>
import { ref } from "vue";
import { api } from "@/api";
import SectorCategorySelect from "@/components/SectorCategorySelect.vue";
const search = ref('')

const offres = ref([]);
const loading = ref(false);
const filters = ref({ secteur_slug: null, categorie_slug: null });

async function loadOffres() {
  loading.value = true;
  try {
    const params = {};
    if (filters.value.secteur_slug) params.secteur_slug = filters.value.secteur_slug;
    if (filters.value.categorie_slug) params.categorie_slug = filters.value.categorie_slug;
    const { data } = await api.get("/offres", { params });
    offres.value = data; // [{id,titre,prix,partenaire,...}]
    console.log(offres.value)
  } finally {
    loading.value = false;
  }
}

function onFiltersChange(payload) {
  filters.value = payload;
  loadOffres();
}

// charger au montage
loadOffres();
</script>

<template>

    <SectorCategorySelect @change="onFiltersChange" />

<div class="space-y-4 mt-6">
    <h1 class="text-2xl font-bold">Offres</h1>

 <div class="space-y-6">
    <div v-if="loading">Chargement…</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <article
        v-for="o in offres"
        :key="o.id"
        class="border rounded p-3"
      >
        <img v-if="o.image_banniere" :src="o.image_banniere" class="w-full h-40 object-cover rounded mb-2" />
        <h3 class="font-semibold">{{ o.titre }}</h3>
        <div class="text-sm opacity-70">
          {{ o.partenaire }} — {{ o.secteur }} / {{ o.categorie }}
        </div>
        <div class="mt-2 font-bold">{{ o.prix }} FCFA</div>
      </article>
    </div>
  </div>
</div>
</template>
<style>
header {
  background-size: cover;
  background-position: center;
}</style>