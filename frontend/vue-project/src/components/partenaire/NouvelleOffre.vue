<template>
  <div class="p-6 max-w-3xl mx-auto space-y-8 bg-white rounded-xl shadow-md">
    <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
      ➕ Nouvelle offre
    </h1>

    <form @submit.prevent="submit" class="space-y-6">
      <!-- Titre -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Titre de l’offre</label>
        <input
          v-model="offre.titre"
          class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
          placeholder="Ex: Réparation express"
          required
        />
      </div>
<div>
   <select v-model="offre.categorie_offre_id" class="w-full p-3 border border-gray-300 rounded-md">
  <option disabled value="">Sélectionnez une catégorie</option>
  <option v-for="cat in categories" :key="cat.id" :value="cat.id">
    {{ cat.nom }}
  </option>
</select>


          <label class="block text-sm font-medium text-gray-700 mb-1">Prix</label>
          <input
            v-model.number="offre.prix"
            type="number"
            class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
            placeholder="Ex: 5000"
          />
        </div>
      <!-- Description -->
      <div>

        <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
        <textarea
          v-model="offre.description"
          class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
          placeholder="Détaillez votre offre"
          rows="4"
        />
      </div>
      <!-- Options -->
<!-- Options -->
<div class="space-y-4">
  <label class="block text-sm font-medium text-gray-700 mb-1">Options de l’offre</label>

  <div v-if="offre.options.length === 0" class="text-sm text-gray-500 italic">
    Aucune option ajoutée pour l’instant.
  </div>

  <div
    v-for="(option, index) in offre.options"
    :key="index"
    class="grid grid-cols-1 md:grid-cols-4 gap-4 items-center"
  >
    <input
      v-model="option.nom"
      class="p-3 border border-gray-300 rounded-md focus:ring-orange-400 focus:outline-none"
      placeholder="Nom (ex: Taille)"
    />
    <input
      v-model="option.valeur"
      class="p-3 border border-gray-300 rounded-md focus:ring-orange-400 focus:outline-none"
      placeholder="Valeur (ex: XL)"
    />
    <input
      v-model.number="option.prix_supplementaire"
      type="number"
      class="p-3 border border-gray-300 rounded-md focus:ring-orange-400 focus:outline-none"
      placeholder="Prix supp. (ex: 1000)"
    />
    <button
      type="button"
      @click="removeOption(index)"
      class="text-red-500 hover:text-red-700 text-sm"
    >
      ❌ Supprimer
    </button>
  </div>

  <button
    type="button"
    @click="addOption"
    class="bg-orange-100 text-orange-700 px-4 py-2 rounded-md hover:bg-orange-200 transition"
  >
    ➕ Ajouter une option
  </button>
</div>


      <!-- Prix et localisation -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ville</label>
          <input
            v-model="offre.ville"
            class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
            placeholder="Ex: Abidjan"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Commune</label>
          <select v-model="offre.commune" class="input">
  <option disabled value="">Sélectionnez une commune</option>
  <option v-for="commune in communes" :key="commune" :value="commune">
    {{ commune }}
  </option>
</select>

        </div>
      </div>

      <!-- Localisation précise -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Localisation précise</label>
        <input
          v-model="offre.localisation"
          class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
          placeholder="Rue, quartier, repère..."
        />
      </div>

      <!-- Expiration -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Date d’expiration</label>
        <input
          v-model="offre.expire_le"
          type="date"
          class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
        />
      </div>
      <!-- Tags -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Tags</label>
        <div class="flex flex-wrap gap-2">
          <label
            v-for="tag in tags"
            :key="tag.id"
            class="flex items-center gap-2 bg-orange-50 px-3 py-1 rounded-full cursor-pointer hover:bg-orange-100"
          >
            <input
              type="checkbox"
              :value="tag.id"
              v-model="selectedTags"
              class="accent-orange-500"
            />
            <span class="text-sm text-gray-700">{{ tag.nom }}</span>
          </label>
        </div>
      </div>
      <!-- Image bannière -->
<div class="space-y-2">
  <label class="block text-sm font-medium text-gray-700 mb-1">Image bannière</label>
  <input
    type="file"
    @change="handleUpload"
    class="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-orange-100 file:text-orange-700 hover:file:bg-orange-200"
  />

  <div
    v-if="offre.image_banniere"
    class="relative group w-full max-h-64 rounded-lg overflow-hidden shadow-lg border border-gray-200"
  >
    <img
      :src="`http://localhost:5000${offre.image_banniere}`"
      alt="Bannière"
      class="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
    />
    <button
      type="button"
      @click="offre.image_banniere = ''"
      class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 shadow-md opacity-0 group-hover:opacity-100 transition"
      title="Supprimer"
    >
      ✕
    </button>
  </div>
</div>

      <!-- Photos supplémentaires -->
<div class="space-y-2">
  <label class="block text-sm font-medium text-gray-700 mb-1">Photos supplémentaires</label>
  <input type="file" multiple @change="handlePhotoUpload" class="input-file" />

  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
    <div
      v-for="(url, index) in uploadedPhotoUrls"
      :key="url"
      class="relative group rounded-lg overflow-hidden shadow-md border border-gray-200"
    >
      <img
        :src="url"
        class="w-full h-32 object-cover transition-transform duration-300 group-hover:scale-105"
      />
      <button
        type="button"
        @click="removePhoto(index)"
        class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 shadow-md opacity-0 group-hover:opacity-100 transition"
        title="Supprimer"
      >
        ✕
      </button>
    </div>
  </div>
</div>


      <!-- Bouton -->
      <button
        type="submit"
        class="bg-orange-500 text-white py-2 px-6 rounded-md hover:bg-orange-600 transition w-full md:w-auto"
      >
        💾 Enregistrer
      </button>

      <!-- Message -->
      <p v-if="message" class="text-green-600 text-sm text-center">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const message = ref('')
const tags = ref([])
const selectedTags = ref([])

const offre = ref({
  titre: '',
  description: '',
  prix: null,
  ville: '',
  commune: '',
  localisation: '',
  expire_le: '',
  image_banniere: '',
  categorie_offre_id: '',   // 🔧 ajouté
  options: [],
  photos: []                 // 🔧 ajouté
})

onMounted(async () => {
  const { data } = await api.get('/partenaire/tags')
  tags.value = data
})

const communes = [
  "Yopougon", "Abobo", "Cocody", "Treichville", "Marcory",
  "Koumassi", "Plateau", "Adjame", "Attécoubé", "Port-Bouët", "Songon"
]

const categories = ref([])
const uploadedPhotoUrls = ref([])

onMounted(async () => {
  const { data: tagData } = await api.get('/partenaire/tags')
  tags.value = tagData

  const { data: catData } = await api.get('/partenaire/categories-offres')
  categories.value = catData
})
async function handleUpload(e) {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('image', file)

  try {
    const { data } = await api.post('/partenaire/upload/photo-offre', formData)
    offre.value.image_banniere = data.url
  } catch (err) {
    console.error("Erreur upload bannière :", err)
  }
}

async function handlePhotoUpload(e) {
  const files = Array.from(e.target.files)
  for (const file of files) {
    const formData = new FormData()
    formData.append('image', file)
    const { data } = await api.post('/partenaire/upload/photo-offre', formData)
    uploadedPhotoUrls.value.push( `http://localhost:5000/${data.url}`)
  }
}

async function submit() {
 const payload = {
  ...offre.value,
  tags: selectedTags.value,
  photos: uploadedPhotoUrls.value
}


  try {
    console.log("Payload envoyé :", payload)

    await api.post('/partenaire/offres', payload)   // 🔧 corrigé l’URL
    message.value = "✅ Offre enregistrée avec succès"
    setTimeout(() => {
      message.value = ""
      router.push('/partenaire/offres')
    }, 2000)
  } catch (e) {
    message.value = "❌ Erreur lors de la création"
  }
}

function addOption() {
  offre.value.options.push({
    nom: '',
    valeur: '',
    prix_supplementaire: 0
  })
}
function removeOption(index) {
  offre.value.options.splice(index, 1)
}
function removePhoto(index) {
  uploadedPhotoUrls.value.splice(index, 1)
}

</script>

