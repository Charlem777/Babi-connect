<template>
  <div class="bg-white rounded shadow p-4 text-center space-y-2">
    <div class="text-2xl">{{ icon }}</div>
    <div class="text-lg font-semibold text-gray-800">{{ value }}</div>
    <div class="text-sm text-gray-500">{{ label }}</div>
  </div>
</template>

<script setup>
defineProps({ label: String, value: [String, Number], icon: String })
</script>
