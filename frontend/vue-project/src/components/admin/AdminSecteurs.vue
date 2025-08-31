<template>
  <div class="p-6 space-y-6">
    <AdminHeader
      title="Gestion des secteurs"
      subtitle="Ajoutez, modifiez ou supprimez les secteurs utilisés par les partenaires"
      icon="🌟"
    />

    <div class="space-y-4 bg-white p-4 rounded shadow">
      <h3 class="text-lg font-semibold text-gray-700">Ajouter un secteur</h3>

      <input
        v-model="newSecteur.nom"
        placeholder="Nom du secteur"
        class="border px-3 py-2 rounded w-full"
      />
      <textarea
        v-model="newSecteur.description"
        placeholder="Description"
        class="border px-3 py-2 rounded w-full"
      />
      <ImageUploader @uploaded="url => newSecteur.photo = url" />
      <button
        @click="addSecteur"
        class="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700"
      >
        ➕ Ajouter
      </button>
    </div>

    <EditableList
      :items="secteurs"
      item-key="id"
      label-key="nom"
      :show-image="true"
      @update="updateSecteur"
      @delete="deleteSecteur"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import AdminHeader from './AdminHeader.vue'
import ImageUploader from './ImageUploader.vue'
import EditableList from '@/components/admin/EditableList.vue'

const secteurs = ref([])
const newSecteur = ref({
  nom: '',
  description: '',
  photo: ''
})

onMounted(async () => {
  const { data } = await api.get('/admin/secteurs')
  secteurs.value = data
})

async function addSecteur() {
  const nom = newSecteur.value.nom.trim()
  if (!nom) return alert("Le nom est requis")

  const slug = nom.toLowerCase().replace(/\s+/g, '-')
  const { data } = await api.post('/admin/secteurs', {
    nom,
    slug,
    description: newSecteur.value.description,
    photo: newSecteur.value.photo
  })

  secteurs.value.push(data)
  newSecteur.value = { nom: '', description: '', photo: '' }
}

async function updateSecteur(id, nom, description, photo) {
  const slug = nom.toLowerCase().replace(/\s+/g, '-')
  await api.put(`/admin/secteurs/${id}`, { nom, slug, description, photo })

  const secteur = secteurs.value.find(s => s.id === id)
  if (secteur) {
    secteur.nom = nom
    secteur.description = description
    secteur.photo = photo
  }
}

async function deleteSecteur(id) {
  try {
    await api.delete(`/admin/secteurs/${id}`)
    secteurs.value = secteurs.value.filter(s => s.id !== id)
  } catch (err) {
    alert(err.response.data.error || "Erreur lors de la suppression")
  }
}
</script>
