<template>
  <div class="bg-white shadow rounded-lg p-4 flex justify-between items-center">
    <div>
      <h2 class="text-lg font-semibold text-gray-700">{{ title }}</h2>
      <p class="text-2xl font-bold text-orange-500">{{ count }}</p>
    </div>
    <div class="text-3xl">{{ icon }}</div>
  </div>
</template>

<script setup>
defineProps({ title: String, icon: String, count: Number })
</script>
