<template>
    <div class="p-6 space-y-6">
<AdminHeader
  title="Catégories partenaires"
  subtitle="Ajoutez, modifiez ou supprimez les catégories utilisées par les partenaires"
  icon="📂"
>
  <RouterLink to="/admin/categories/new" class="text-sm text-orange-600 hover:underline">
    ➕ Nouvelle catégorie
  </RouterLink>
</AdminHeader>

      <AddItemForm
        placeholder="Nom de la catégorie"
        :secteurs="secteurs"
        @submit="addCategorie"
        />


      <EditableList
  :items="categories"
  :secteurs="secteurs"
  item-key="id"
  label-key="nom"
  :show-image="false"
  :show-secteur="true"
  :allow-secteur-edit="true"
  @update="updateCategorie"
  @delete="deleteCategorie"
/>


    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import AdminHeader from '@/components/admin/AdminHeader.vue'
import AddItemForm from '@/components/admin/AddItemForm.vue'
import EditableList from '@/components/admin/EditableList.vue'

const categories = ref([])
const secteurs = ref([])

onMounted(async () => {
  const [secteursRes, categoriesRes] = await Promise.all([
    api.get('/admin/secteurs'),
    api.get('/admin/categories-partenaires')
  ])
  secteurs.value = secteursRes.data
  categories.value = categoriesRes.data
})

async function addCategorie({ nom, description, secteur_id }) {
  const { data } = await api.post('/admin/categories-partenaires', {
    nom,
    description,
    secteur_id
  })
  categories.value.push(data)
}

async function updateCategorie(id, nom, description, secteur_id) {
  const { data } = await api.put(`/admin/categories-partenaires/${id}`, {
    nom,
    description,
    secteur_id
  })

  const cat = categories.value.find(c => c.id === id)
  if (cat) {
    cat.nom = data.nom
    cat.description = data.description
    cat.secteur_id = data.secteur_id
    cat.secteur_nom = data.secteur_nom // 🔹 ajouter cette ligne
  }
}





async function deleteCategorie(id) {
  await api.delete(`/admin/categories-partenaires/${id}`)
  categories.value = categories.value.filter(c => c.id !== id)
}
</script>

