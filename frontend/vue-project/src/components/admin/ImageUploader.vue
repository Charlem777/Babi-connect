<template>
  <div class="space-y-2">
    <input type="file" @change="handleUpload" />
    <img v-if="preview" :src="preview" class="w-32 h-32 object-cover rounded shadow" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/api'

const emit = defineEmits(['uploaded'])
const preview = ref(null)

async function handleUpload(e) {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('photo', file)

 try {
  const { data } = await api.post('/admin/upload/secteur-photo', formData)
  preview.value = data.url
  emit('uploaded', data.url)
} catch (err) {
  alert(err.response?.data?.error || "Erreur lors de l’upload")
}

}
</script>
