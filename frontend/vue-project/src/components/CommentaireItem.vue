<template>
  <div class="border-l-2 border-gray-100 pl-4">
    <!-- Commentaire principal -->
    <div class="flex space-x-3">
      <!-- Avatar utilisateur -->
      <div class="flex-shrink-0">
        <div class="w-8 h-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
          {{ getInitials(commentaire.utilisateur) }}
        </div>
      </div>

      <!-- Contenu du commentaire -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center space-x-2 mb-1">
          <h4 class="text-sm font-medium text-gray-900">
            {{ commentaire.utilisateur.prenom }} {{ commentaire.utilisateur.nom }}
          </h4>
          <span class="text-xs text-gray-500">•</span>
          <time class="text-xs text-gray-500">
            {{ formatDate(commentaire.date) }}
          </time>
        </div>
        
        <p class="text-gray-700 text-sm leading-relaxed mb-3">
          {{ commentaire.commentaire }}
        </p>

        <!-- Actions -->
        <div class="flex items-center space-x-4">
          <button
            v-if="authStore.isAuthenticated && !showReplyForm"
            @click="showReplyForm = true"
            class="text-xs text-gray-500 hover:text-orange-600 font-medium transition-colors"
          >
            Répondre
          </button>
        </div>

        <!-- Formulaire de réponse -->
        <div v-if="showReplyForm" class="mt-3 p-3 bg-gray-50 rounded-lg">
          <textarea
            v-model="replyText"
            placeholder="Écrivez votre réponse..."
            rows="2"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none text-sm"
          ></textarea>
          <div class="flex space-x-2 mt-2">
            <button
              @click="ajouterReponse"
              :disabled="!replyText.trim() || isSubmittingReply"
              class="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 text-white px-3 py-1.5 rounded text-xs font-medium transition-colors"
            >
              {{ isSubmittingReply ? 'Envoi...' : 'Répondre' }}
            </button>
            <button
              @click="annulerReponse"
              class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1.5 rounded text-xs font-medium transition-colors"
            >
              Annuler
            </button>
          </div>
        </div>

        <!-- Réponses -->
        <div v-if="commentaire.reponses && commentaire.reponses.length > 0" class="mt-4 space-y-4">
          <div
            v-for="reponse in commentaire.reponses"
            :key="reponse.id"
            class="flex space-x-3 pl-4 border-l border-gray-200"
          >
            <!-- Avatar réponse -->
            <div class="flex-shrink-0">
              <div class="w-6 h-6 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center text-white font-medium text-xs">
                {{ getInitials(reponse.utilisateur) }}
              </div>
            </div>

            <!-- Contenu réponse -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center space-x-2 mb-1">
                <h5 class="text-xs font-medium text-gray-900">
                  {{ reponse.utilisateur.prenom }} {{ reponse.utilisateur.nom }}
                </h5>
                <span class="text-xs text-gray-400">•</span>
                <time class="text-xs text-gray-400">
                  {{ formatDate(reponse.date) }}
                </time>
              </div>
              
              <p class="text-gray-600 text-xs leading-relaxed">
                {{ reponse.commentaire }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api'

const props = defineProps({
  commentaire: {
    type: Object,
    required: true
  },
  offreId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['reply-added'])

const authStore = useAuthStore()
const showReplyForm = ref(false)
const replyText = ref('')
const isSubmittingReply = ref(false)

const getInitials = (utilisateur) => {
  if (!utilisateur) return '?'
  const prenom = utilisateur.prenom || ''
  const nom = utilisateur.nom || ''
  return (prenom.charAt(0) + nom.charAt(0)).toUpperCase()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'À l\'instant'
  if (diffMins < 60) return `Il y a ${diffMins}min`
  if (diffHours < 24) return `Il y a ${diffHours}h`
  if (diffDays < 7) return `Il y a ${diffDays}j`
  
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
  })
}

const ajouterReponse = async () => {
  if (!replyText.value.trim() || isSubmittingReply.value) return

  try {
    isSubmittingReply.value = true
    const { data } = await api.post(`/offres/${props.offreId}/commentaires`, {
      commentaire: replyText.value.trim(),
      parent_id: props.commentaire.id
    })
    
    emit('reply-added', props.commentaire.id, data.commentaire)
    annulerReponse()
  } catch (error) {
    console.error('Erreur lors de l\'ajout de la réponse:', error)
    alert('Erreur lors de l\'ajout de la réponse')
  } finally {
    isSubmittingReply.value = false
  }
}

const annulerReponse = () => {
  showReplyForm.value = false
  replyText.value = ''
}
</script>
