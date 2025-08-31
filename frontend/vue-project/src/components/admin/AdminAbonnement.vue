<template>
  <div class="p-6 space-y-6">
    <AdminHeader
      title="Gestion des abonnements"
      subtitle="Attribuez, modifiez ou désactivez les abonnements des partenaires"
      icon="🎫"
    />

    <EditableList
      :items="partenaires"
      item-key="id"
      label-key="nom"
      :show-abonnement="true"
      @update="updateAbonnement"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import AdminHeader from './AdminHeader.vue'
import EditableList from '@/components/admin/EditableList.vue'

const partenaires = ref([])

onMounted(async () => {
  const { data } = await api.get('/admin/partenaires') // ← assure-toi que cette route renvoie l’abonnement
  partenaires.value = data
})
function formatDate(dateString) {
  if (!dateString) return ''
  return new Date(dateString).toISOString().split('T')[0]
}



async function updateAbonnement(id, abonnementData) {
  const partenaire = partenaires.value.find(p => p.id === id)
  const abId = partenaire.abonnement?.id

  if (!abId) {
    alert("Aucun abonnement actif à mettre à jour pour ce partenaire.")
    return
  }

  // accepter les 2 formes : { type, date_fin, actif } OU { abonnement: { ... } }
  const abData = abonnementData.abonnement ? abonnementData.abonnement : abonnementData
console.log('updateAbonnement reçu', abonnementData)
  // preferer date_fin sinon expire_le
  const dateValue = abData.date_fin || abData.expire_le
  const payload = {
    type: abData.type || null,
    date_fin: dateValue ? formatDate(dateValue) : null,
    actif: !!abData.actif
  }

  console.log('DEBUG payload envoyé ->', payload) // debug temporaire
  try {
    console.log('payload envoyé', payload)
    await api.put(`/admin/abonnements/${abId}`, payload)
    const { data } = await api.get(`/admin/partenaires/${id}`)
    Object.assign(partenaire, data)
    console.log('data renv:',data)
  } catch (err) {
    alert(err.response?.data?.error || "Erreur lors de la mise à jour de l’abonnement.")
  }
}



</script>
