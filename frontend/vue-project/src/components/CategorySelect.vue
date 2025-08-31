<template>
  <div v-if="categories.length" class="sticky top-[120px] z-30 bg-white border-b">
    <nav class="flex gap-3 overflow-x-auto no-scrollbar px-4 py-3">
      <button
        @click="select('')"
        :class="buttonClass('')"
      >
        Toutes
      </button>
      <button
        v-for="c in categories"
        :key="c.slug"
        @click="select(c.slug)"
        :class="buttonClass(c.slug)"
      >
        {{ c.nom }}
      </button>
    </nav>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { api } from "@/api";

const props = defineProps({
  secteurSlug: String,
  modelValue: String,
});

const emit = defineEmits(["update:modelValue", "change"]);

const categories = ref([]);
const selectedCategorie = ref(props.modelValue || "");

async function loadCategories(slug) {
  try {
    const endpoint = slug ? `/secteurs/${slug}/categories` : `/categories`;
    const { data } = await api.get(endpoint);
    categories.value = data;
  } catch (e) {
    console.error("Erreur chargement catégories", e);
  }
}

function select(slug) {
  selectedCategorie.value = slug;
  emit("update:modelValue", slug);
  emit("change", slug);
}

function buttonClass(slug) {
  return [
    'px-4 py-2 rounded-full border text-sm font-medium whitespace-nowrap transition',
    selectedCategorie.value === slug
      ? 'bg-orange-600 text-white border-orange-600'
      : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'
  ];
}

// Watch secteur -> recharge catégories
watch(() => props.secteurSlug, (slug) => {
  loadCategories(slug)
  // reset sélection locale si secteur change
  selectedCategorie.value = ''
  emit("update:modelValue", '') 
})

</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
