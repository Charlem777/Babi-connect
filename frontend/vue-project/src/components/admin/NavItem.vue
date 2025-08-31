<template>
  <router-link
    :to="to"
    class="flex items-center space-x-2 px-4 py-2 rounded-md transition-all duration-200"
    :class="isActive ? 'bg-orange-500 text-white' : 'hover:bg-gray-800 hover:text-orange-400'"
  >
    <span class="text-xl">{{ icon }}</span>
    <span class="font-medium">{{ label }}</span>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
const props = defineProps({
  to: String,
  icon: String,
  label: String
})

const route = useRoute()
const isActive = computed(() => route.path === props.to)
</script>
