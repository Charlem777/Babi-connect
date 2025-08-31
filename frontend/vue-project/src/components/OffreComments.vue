<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900">
        Commentaires ({{ commentaires.length }})
      </h3>
      <button 
        v-if="authStore.isAuthenticated && !showCommentForm"
        @click="showCommentForm = true"
        class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
      >
        Ajouter un commentaire
      </button>
    </div>

    <!-- Formulaire d'ajout de commentaire -->
    <div v-if="showCommentForm" class="mb-6 p-4 bg-gray-50 rounded-lg">
      <div class="space-y-4">
        <textarea
          v-model="nouveauCommentaire"
          placeholder="Écrivez votre commentaire..."
          rows="3"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none"
        ></textarea>
        <div class="flex space-x-3">
          <button
            @click="ajouterCommentaire"
            :disabled="!nouveauCommentaire.trim() || isSubmitting"
            class="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {{ isSubmitting ? 'Envoi...' : 'Publier' }}
          </button>
          <button
            @click="annulerCommentaire"
            class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Annuler
          </button>
        </div>
      </div>
    </div>

    <!-- Message d'authentification -->
    <div v-if="!authStore.isAuthenticated" class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
      <p class="text-blue-800 text-sm">
        <svg class="w-4 h-4 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
        </svg>
        Connectez-vous pour laisser un commentaire
      </p>
    </div>

    <!-- Liste des commentaires -->
    <div v-if="commentaires.length === 0" class="text-center py-8 text-gray-500">
      <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
      </svg>
      <p>Aucun commentaire pour le moment</p>
      <p class="text-sm">Soyez le premier à donner votre avis !</p>
    </div>

    <div v-else class="space-y-6">
      <CommentaireItem
        v-for="commentaire in commentaires"
        :key="commentaire.id"
        :commentaire="commentaire"
        :offre-id="offreId"
        @reply-added="onReplyAdded"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api'
import CommentaireItem from './CommentaireItem.vue'

const props = defineProps({
  offreId: {
    type: Number,
    required: true
  }
})

const authStore = useAuthStore()
const commentaires = ref([])
const showCommentForm = ref(false)
const nouveauCommentaire = ref('')
const isSubmitting = ref(false)

const chargerCommentaires = async () => {
  try {
    const { data } = await api.get(`/offres/${props.offreId}/commentaires`)
    commentaires.value = data.commentaires
  } catch (error) {
    console.error('Erreur lors du chargement des commentaires:', error)
  }
}

const ajouterCommentaire = async () => {
  if (!nouveauCommentaire.value.trim() || isSubmitting.value) return

  try {
    isSubmitting.value = true
    const { data } = await api.post(`/offres/${props.offreId}/commentaires`, {
      commentaire: nouveauCommentaire.value.trim()
    })
    
    commentaires.value.unshift(data.commentaire)
    annulerCommentaire()
  } catch (error) {
    console.error('Erreur lors de l\'ajout du commentaire:', error)
    alert('Erreur lors de l\'ajout du commentaire')
  } finally {
    isSubmitting.value = false
  }
}

const annulerCommentaire = () => {
  showCommentForm.value = false
  nouveauCommentaire.value = ''
}

const onReplyAdded = (parentId, newReply) => {
  // Trouver le commentaire parent et ajouter la réponse
  const findAndAddReply = (comments) => {
    for (let comment of comments) {
      if (comment.id === parentId) {
        if (!comment.reponses) comment.reponses = []
        comment.reponses.push(newReply)
        return true
      }
      if (comment.reponses && findAndAddReply(comment.reponses)) {
        return true
      }
    }
    return false
  }
  
  findAndAddReply(commentaires.value)
}

onMounted(() => {
  chargerCommentaires()
})
</script>
