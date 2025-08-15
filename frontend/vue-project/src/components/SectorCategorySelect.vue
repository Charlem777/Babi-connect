<script setup>
import { ref, onMounted, watch } from "vue"
import { api } from "@/api"

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ secteur_slug: null, categorie_slug: null })
  }
})

const emit = defineEmits(["update:modelValue", "change"])

const secteurs = ref([])
const categories = ref([])

const selectedSecteur = ref(props.modelValue.secteur_slug || "")
const selectedCategorie = ref(props.modelValue.categorie_slug || "")

const loadingSecteurs = ref(false)
const loadingCategories = ref(false)

async function loadSecteurs() {
  loadingSecteurs.value = true
  try {
    const { data } = await api.get("/secteurs")
    secteurs.value = data
  } finally {
    loadingSecteurs.value = false
  }
}

async function loadCategories(slug) {
  if (!slug) {
    categories.value = []
    selectedCategorie.value = ""
    return
  }
  loadingCategories.value = true
  try {
    const { data } = await api.get(`/secteurs/${slug}/categories`)
    categories.value = data
    selectedCategorie.value = ""
  } finally {
    loadingCategories.value = false
  }
}

onMounted(() => {
  loadSecteurs()
  if (selectedSecteur.value) {
    loadCategories(selectedSecteur.value)
  }
})

watch(selectedSecteur, (slug) => {
  loadCategories(slug)
})

watch([selectedSecteur, selectedCategorie], () => {
  const payload = {
    secteur_slug: selectedSecteur.value || null,
    categorie_slug: selectedCategorie.value || null
  }
  emit("update:modelValue", payload)
  emit("change", payload)
})
</script>

<template>
  <div class="mt-6">
    <select
      v-model="selectedSecteur"
      class="w-full border rounded-xl p-2 bg-yellow-800 h-12 text-white"
      :disabled="loadingSecteurs"
    >
      <option value="">— Tous les secteurs —</option>
      <option v-for="s in secteurs" :key="s.slug" :value="s.slug">
        {{ s.nom }}
      </option>
    </select>
  </div>

  <div v-if="categories.length" class="mb-4 mt-6">
    <nav class="flex gap-3 overflow-x-auto pb-2">
      <button
        @click="selectedCategorie = ''"
        :class="[
          'px-3 py-1 rounded-full border text-sm whitespace-nowrap',
          selectedCategorie === ''
            ? 'bg-orange-600 text-white border-orange-600'
            : 'bg-gray-100 text-gray-700 border-gray-300'
        ]"
      >
        Toutes
      </button>
      <button
        v-for="c in categories"
        :key="c.slug"
        @click="selectedCategorie = c.slug"
        :class="[
          'px-3 py-1 rounded-full border text-sm whitespace-nowrap',
          selectedCategorie === c.slug
            ? 'bg-orange-600 text-white border-orange-600'
            : 'bg-gray-100 text-gray-700 border-gray-300'
        ]"
      >
        {{ c.nom }}
      </button>
    </nav>
  </div>
</template>
