<script setup>
import { ref, watch, onMounted } from "vue"
import { api } from "@/api"

const props = defineProps({
  secteurSlug: String,
  modelValue: String
})

const emit = defineEmits(["update:modelValue", "change"])

const categories = ref([])
const selectedCategorie = ref(props.modelValue || "")
const loading = ref(false)

async function loadCategories(slug) {
  console.log("🔹 Loading categories for secteur:", slug)
  loading.value = true
  try {
    const endpoint = slug ? `/secteurs/${slug}/categories` : `/categories`
    const { data } = await api.get(endpoint)
    console.log("🔹 Categories loaded:", data)
    categories.value = data
  } finally {
    loading.value = false
  }
}


// Sélection d’une catégorie
function select(slug) {
  selectedCategorie.value = slug
  emit("update:modelValue", slug)
  emit("change", slug)
}

// Watch sur le secteur pour recharger catégories et reset sélection
let previousSecteur = props.secteurSlug

watch(
  () => props.secteurSlug,
  (slug) => {
    if (slug !== previousSecteur) {
      loadCategories(slug)
      selectedCategorie.value = ""
      emit("update:modelValue", "")
      previousSecteur = slug
    }
  },
  { immediate: true }
)


// Watch sur le modelValue du parent pour sync local
watch(
  () => props.modelValue,
  (val) => { selectedCategorie.value = val || "" }
)


watch(selectedCategorie, (val) => {
  console.log("🔹 Selected category changed:", val)
  emit("update:modelValue", val)
  emit("change", val)
})
onMounted(() => {
  loadCategories(props.secteurSlug)
})

</script>

<template>
  <div v-if="categories.length" class="sticky top-36 md:top-16 z-40 bg-white border-b border-gray-200 shadow-sm">
    <nav class="flex gap-3 overflow-x-auto no-scrollbar px-4 py-3">
      <button
        @click="select('')"
        :class="selectedCategorie === '' ? 'bg-orange-600 text-white border-orange-600' : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'"
        class="px-4 py-2 rounded-full border text-sm whitespace-nowrap transition-colors duration-200"
      >
        Toutes
      </button>
      <button
        v-for="c in categories"
        :key="c.slug"
        @click="select(c.slug)"
        :class="selectedCategorie === c.slug ? 'bg-orange-600 text-white border-orange-600' : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'"
        class="px-4 py-2 rounded-full border text-sm whitespace-nowrap transition-colors duration-200"
      >
        {{ c.nom }}
      </button>
    </nav>
  </div>
</template>
