<template>
  <div class="flex items-center justify-between border-b pb-2 mb-4">
    <div class="space-y-1">
      <h2 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
        <span v-if="icon">{{ icon }}</span>
        {{ title }}
      </h2>
      <p v-if="subtitle" class="text-sm text-gray-500">{{ subtitle }}</p>
    </div>
    <div class="transition-all duration-300 ease-in-out">
  <slot />
</div>

  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '' }
})
</script>
