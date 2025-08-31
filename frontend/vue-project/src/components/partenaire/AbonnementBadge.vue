<template>
  <div class="bg-white rounded shadow p-4 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-gray-800">🎫 Abonnement</h2>
      <p class="text-sm text-gray-500">
        Type : <span class="font-medium text-gray-700">{{ abonnement.type || 'Non défini' }}</span>
      </p>
      <p class="text-sm text-gray-500">
        Expire le :
        <span :class="expireClass">
          {{ formattedDate || 'Non définie' }}
        </span>
      </p>
    </div>

    <span
      :class="[
        'px-3 py-1 rounded-full text-sm font-semibold',
        abonnement.actif ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      ]"
    >
      {{ abonnement.actif ? 'Actif' : 'Inactif' }}
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  abonnement: {
    type: Object,
    required: true
  }
})
console.log(props.abonnement)
const formattedDate = computed(() => {
  if (!props.abonnement.expire_le) return null
  const date = new Date(props.abonnement.expire_le)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const expireClass = computed(() => {
  if (!props.abonnement.expire_le) return 'text-gray-700'
  const now = new Date()
  const expireDate = new Date(props.abonnement.expire_le)
  return expireDate < now ? 'text-red-600 font-semibold' : 'text-gray-700'
})
</script>
