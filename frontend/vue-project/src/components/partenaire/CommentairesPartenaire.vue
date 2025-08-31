<template>
  <div class="p-6 max-w-4xl mx-auto space-y-6">
    <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
      💬 Commentaires sur mes offres
    </h1>

    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto"></div>
      <p class="text-gray-600 mt-2">Chargement des commentaires...</p>
    </div>

    <div v-else-if="commentaires.length === 0" class="text-center py-12">
      <div class="text-6xl mb-4">💭</div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">Aucun commentaire</h3>
      <p class="text-gray-600">Vos offres n'ont pas encore reçu de commentaires.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="commentaire in commentaires"
        :key="commentaire.id"
        class="bg-white rounded-lg shadow-md border border-gray-200 p-6"
      >
        <!-- En-tête du commentaire -->
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <span class="text-blue-600 font-medium">
                {{ commentaire.utilisateur?.prenom?.charAt(0) || '?' }}
              </span>
            </div>
            <div>
              <p class="font-medium text-gray-900">
                {{ commentaire.utilisateur?.prenom }} {{ commentaire.utilisateur?.nom }}
              </p>
              <p class="text-sm text-gray-500">
                {{ formatDate(commentaire.date) }}
              </p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-sm font-medium text-orange-600">{{ commentaire.offre.titre }}</p>
            <p class="text-xs text-gray-500">Offre #{{ commentaire.offre.id }}</p>
          </div>
        </div>

        <!-- Contenu du commentaire -->
        <div class="mb-4">
          <p class="text-gray-800 leading-relaxed">{{ commentaire.commentaire }}</p>
        </div>

        <!-- Réponses existantes -->
        <div v-if="commentaire.reponses && commentaire.reponses.length > 0" class="mb-4">
          <h4 class="text-sm font-medium text-gray-700 mb-2">Vos réponses :</h4>
          <div
            v-for="reponse in commentaire.reponses"
            :key="reponse.id"
            class="bg-orange-50 rounded-lg p-3 mb-2 border-l-4 border-orange-400"
          >
            <div class="flex items-center gap-2 mb-1">
              <span class="text-orange-600 font-medium">{{ reponse.partenaire.nom }}</span>
              <span class="text-xs text-gray-500">{{ formatDate(reponse.date) }}</span>
            </div>
            <p class="text-gray-800">{{ reponse.reponse }}</p>
          </div>
        </div>

        <!-- Formulaire de réponse -->
        <div class="border-t pt-4">
          <form @submit.prevent="repondreCommentaire(commentaire.id)" class="space-y-3">
            <textarea
              v-model="reponses[commentaire.id]"
              class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
              rows="3"
              placeholder="Écrivez votre réponse..."
              required
            ></textarea>
            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="!reponses[commentaire.id] || envoyant[commentaire.id]"
                class="bg-orange-500 text-white px-4 py-2 rounded-md hover:bg-orange-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <span v-if="envoyant[commentaire.id]" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
                {{ envoyant[commentaire.id] ? 'Envoi...' : '📤 Répondre' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Message de succès -->
    <div
      v-if="message"
      class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg transition-opacity duration-300"
    >
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { api } from '@/api'

const commentaires = ref([])
const loading = ref(true)
const message = ref('')
const reponses = reactive({})
const envoyant = reactive({})

onMounted(async () => {
  await chargerCommentaires()
})

async function chargerCommentaires() {
  try {
    loading.value = true
    const { data } = await api.get('/partenaire/commentaires')
    commentaires.value = data
  } catch (err) {
    console.error('Erreur lors du chargement des commentaires :', err)
  } finally {
    loading.value = false
  }
}

async function repondreCommentaire(commentaireId) {
  const reponseText = reponses[commentaireId]
  if (!reponseText) return

  try {
    envoyant[commentaireId] = true
    await api.post(`/partenaire/commentaires/${commentaireId}/repondre`, {
      reponse: reponseText
    })

    // Réinitialiser le champ de réponse
    reponses[commentaireId] = ''
    
    // Recharger les commentaires pour voir la nouvelle réponse
    await chargerCommentaires()
    
    // Afficher message de succès
    message.value = '✅ Réponse envoyée avec succès'
    setTimeout(() => {
      message.value = ''
    }, 3000)
  } catch (err) {
    console.error('Erreur lors de l\'envoi de la réponse :', err)
    message.value = '❌ Erreur lors de l\'envoi de la réponse'
    setTimeout(() => {
      message.value = ''
    }, 3000)
  } finally {
    envoyant[commentaireId] = false
  }
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
/* Styles personnalisés si nécessaire */
</style>
