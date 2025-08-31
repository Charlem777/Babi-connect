<template>
  <div
    class="bg-white rounded shadow p-4 hover:bg-blue-50 transition cursor-pointer"
    @click="$emit('click')"
  >
    <div class="text-2xl mb-2">{{ icon }}</div>
    <h3 class="text-lg font-bold text-gray-800">{{ title }}</h3>
    <p class="text-sm text-gray-500">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({ title: String, description: String, icon: String })
defineEmits(['click'])
</script>
