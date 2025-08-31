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

    // Reset catégorie seulement si elle ne correspond pas au secteur
    if (!categories.value.find(c => c.slug === selectedCategorie.value)) {
      selectedCategorie.value = ""
    }
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

// 🔹 Synchronise quand le parent change
watch(() => props.modelValue.secteur_slug, (newSlug) => {
  selectedSecteur.value = newSlug || ""
})

// Recharge catégories si secteur change
watch(selectedSecteur, (slug) => {
  loadCategories(slug)
    console.log("Slug reçu dans catégories :", slug);

})

// Remonte les valeurs au parent
watch([selectedSecteur, selectedCategorie], () => {
  const payload = {
    secteur_slug: selectedSecteur.value || null,
    categorie_slug: selectedCategorie.value || null
  }
  emit("update:modelValue", payload)
  emit("change", payload)
})
</script>
