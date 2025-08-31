<template>
  <div class="">
    <select v-model="selectedSecteur" @change="emitChange" class="w-full border rounded-xl p-2 bg-gradient-to-r from-orange-500 to-orange-600 h-10  text-white">
      <option value="">— Tous les secteurs —</option>
      <option v-for="s in secteurs" :key="s.slug" :value="s.slug">{{ s.nom }}</option>
    </select>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { api } from "@/api";

const props = defineProps({ modelValue: String });
const emit = defineEmits(["update:modelValue", "change"]);

const secteurs = ref([]);
const selectedSecteur = ref(props.modelValue || "");

// Charger secteurs depuis API
async function loadSecteurs() {
  try {
    const { data } = await api.get("/secteurs");
    secteurs.value = data;
  } catch (e) {
    console.error("Erreur chargement secteurs", e);
  }
}

// Sync parent -> local
watch(() => props.modelValue, val => selectedSecteur.value = val || "", { immediate: true });

// Sync local -> parent
watch(selectedSecteur, val => emit("update:modelValue", val));
function emitChange() { emit("change", selectedSecteur.value); }
watch(selectedSecteur, (val) => {
  console.log("🔹 Sector selected (local):", val)
  emit("update:modelValue", val)
})


onMounted(loadSecteurs);
</script>
