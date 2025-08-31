<template>
  <ul class="space-y-4">
    <li
      v-for="item in items"
      :key="item[itemKey]"
      class="bg-white p-4 rounded shadow space-y-4"
    >
      <!-- Abonnement -->
      <div v-if="showAbonnement" class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">Type d’abonnement</label>
        <select v-model="item.abonnement.type" class="input">
          <option disabled value="">Type d’abonnement</option>
          <option value="basique">Basique</option>
          <option value="premium">Premium</option>
        </select>

        <label class="block text-sm font-medium text-gray-700">Date d’expiration</label>
        <input
          type="date"
          :value="formatDate(item.abonnement.expire_le)"
          @input="item.abonnement.expire_le = $event.target.value"
          class="input"
        />

        <div class="flex items-center justify-between text-xs text-gray-500 italic">
          <span>Actuellement : {{ item.abonnement.expire_le || 'Non définie' }}</span>
          <span
            v-if="item.abonnement?.expire_le && new Date(item.abonnement.expire_le) < new Date()"
            class="px-2 py-1 rounded-full bg-red-100 text-red-700 font-semibold"
          >
            Expiré
          </span>
        </div>

        <label class="flex items-center gap-2 mt-1">
          <input type="checkbox" v-model="item.abonnement.actif" />
          <span class="text-sm text-gray-700">Actif</span>
        </label>
      </div>

      <!-- Nom -->
      <label class="block text-sm font-medium text-gray-700">Nom</label>
      <input
      disabled
        v-model="item[labelKey]"
        class="input"
        placeholder="Nom"
      />
    <div v-if="!showAbonnement">
      <!-- Description -->
      <label class="block text-sm font-medium text-gray-700">Description</label>
      
      <textarea
        v-model="item.description"
        class="input"
        placeholder="Description"
      />
      </div>
      <!-- Secteur -->
      <div v-if="showSecteur" class="space-y-2">
        <div class="text-sm text-gray-600 italic">
          Secteur :
          <span class="font-medium text-gray-800">
            {{ getSecteurNom(item.secteur_id) }}
          </span>
        </div>

        <select
          v-model="item.secteur_id"
          class="input"
        >
          <option disabled value="">Sélectionnez un secteur</option>
          <option
            v-for="secteur in secteurs"
            :key="secteur.id"
            :value="secteur.id"
          >
            {{ secteur.nom }}
          </option>
        </select>
      </div>

      <!-- Upload -->
      <div v-if="showImage" class="flex items-center gap-4">
        <input type="file" @change="e => handlePhotoUpload(e, item)" />

        <div class="flex items-center gap-4">
          <transition name="fade">
            <div v-if="item.photo" class="relative group">
              <img
                :src="item.photo"
                class="w-20 h-20 object-cover rounded shadow hover:scale-105 transition-transform duration-300"
                alt="Photo du secteur"
              />
              <span
                class="absolute bottom-0 left-0 bg-black bg-opacity-50 text-white text-xs px-1 rounded-tr group-hover:block hidden"
              >
                📷
              </span>
            </div>
          </transition>
          
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-2 mt-2">
        <button
          @click="handleUpdate(item)"
          class="text-blue-600 hover:text-blue-800 transition-colors"
        >
          💾 Sauvegarder
        </button>
        <button
          @click="() => emit('delete', item[itemKey])"
          class="text-red-600 hover:text-red-800 transition-colors"
        >
          🗑️ Supprimer
        </button>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { api } from '@/api'

const props = defineProps({
  items: Array,
  itemKey: String,
  labelKey: String,
  showImage: { type: Boolean, default: false },
  showSecteur: { type: Boolean, default: false },
  secteurs: { type: Array, default: () => [] },
  allowSecteurEdit: { type: Boolean, default: false },
  showAbonnement: { type: Boolean, default: false }
})

const emit = defineEmits(['update', 'delete'])

function getSecteurNom(secteur_id) {
  const secteur = props.secteurs.find(s => s.id === secteur_id)
  return secteur ? secteur.nom : 'Non défini'
}

async function handlePhotoUpload(e, item) {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('photo', file)

  try {
    const { data } = await api.post('/admin/upload/secteur-photo', formData)
    item.photo = data.url

    const slug = (item.nom || '').toLowerCase().replace(/\s+/g, '-')
    await api.put(`/admin/secteurs/${item.id}`, {
      nom: item.nom,
      slug,
      description: item.description,
      photo: item.photo
    })
  } catch (err) {
    alert(err.response?.data?.error || "Erreur lors de l’upload")
  }
}
function formatDate(dateString) {

  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toISOString().split('T')[0] // "2025-09-13"
}

function handleUpdate(item) {
  const payload = {
    id: item[props.itemKey],
    nom: item[props.labelKey],
    description: item.description
  }

  if (props.showImage) {
    payload.photo = item.photo
  }

  if (props.showSecteur) {
    payload.secteur_id = item.secteur_id
  }

 // dans handleUpdate(item)
if (props.showAbonnement && item.abonnement) {
  // on met les champs d'abonnement au niveau racine pour correspondre à updateAbonnement
  payload.type = item.abonnement.type || null
  payload.date_fin = item.abonnement.expire_le ? formatDate(item.abonnement.expire_le) : null
  payload.actif = !!item.abonnement.actif
}
console.log('emit payload', payload)
emit('update', payload.id, payload)

}
</script>

<style scoped>


.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
