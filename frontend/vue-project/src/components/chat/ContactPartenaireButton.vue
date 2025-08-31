<template>
  <button
    @click="handleContact"
    :disabled="isLoading"
    :class="[
      'inline-flex items-center px-4 py-2 rounded-lg font-medium transition-all transform',
      variant === 'primary' 
        ? 'bg-gradient-to-r from-orange-500 to-orange-600 text-white hover:from-orange-600 hover:to-orange-700' 
        : 'bg-white text-orange-600 border-2 border-orange-500 hover:bg-orange-50',
      isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 active:scale-95',
      size === 'sm' ? 'text-sm px-3 py-1.5' : 'text-base px-4 py-2'
    ]"
  >
    <svg v-if="isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
    </svg>
    {{ buttonText }}
  </button>

  <!-- Modal de contact -->
  <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="closeModal"></div>
    
    <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-100">
        <h3 class="text-xl font-semibold text-gray-900">
          Contacter {{ partenaire?.nom }}
        </h3>
        <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6">
        <!-- Auth required notice for guests -->
        <div v-if="authStore.isGuest && !guestInfo.provided" class="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
          <p class="text-sm text-orange-800 mb-3">
            Pour contacter ce partenaire, veuillez fournir vos informations :
          </p>
          <div class="space-y-3">
            <input
              v-model="guestInfo.name"
              type="text"
              placeholder="Votre nom"
              class="w-full px-3 py-2 border border-orange-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            >
            <input
              v-model="guestInfo.email"
              type="email"
              placeholder="Votre email"
              class="w-full px-3 py-2 border border-orange-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            >
          </div>
        </div>

        <!-- Error message -->
        <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-800 text-sm">{{ error }}</p>
        </div>

        <!-- Message form -->
        <form @submit.prevent="sendMessage" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Sujet (optionnel)
            </label>
            <input
              v-model="messageForm.sujet"
              type="text"
              placeholder="Objet de votre message"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Message *
            </label>
            <textarea
              v-model="messageForm.message"
              required
              rows="4"
              placeholder="Tapez votre message ici..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none"
            ></textarea>
          </div>

          <div class="flex space-x-3">
            <button
              type="button"
              @click="closeModal"
              class="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              :disabled="!canSendMessage || isSending"
              :class="[
                'flex-1 px-4 py-2 rounded-lg font-medium text-white transition-all',
                canSendMessage && !isSending
                  ? 'bg-orange-500 hover:bg-orange-600'
                  : 'bg-gray-300 cursor-not-allowed'
              ]"
            >
              <span v-if="isSending">Envoi...</span>
              <span v-else>Envoyer</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'

const props = defineProps({
  partenaire: {
    type: Object,
    required: true
  },
  variant: {
    type: String,
    default: 'primary', // 'primary' | 'secondary'
    validator: (value) => ['primary', 'secondary'].includes(value)
  },
  size: {
    type: String,
    default: 'base', // 'sm' | 'base'
    validator: (value) => ['sm', 'base'].includes(value)
  }
})

const emit = defineEmits(['conversation-created'])

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const showModal = ref(false)
const isLoading = ref(false)
const isSending = ref(false)
const error = ref('')

const guestInfo = reactive({
  name: '',
  email: '',
  provided: false
})

const messageForm = reactive({
  sujet: '',
  message: ''
})

const buttonText = computed(() => {
  return isLoading.value ? 'Chargement...' : 'Contacter'
})

const canSendMessage = computed(() => {
  const hasMessage = messageForm.message.trim().length > 0
  
  if (authStore.isGuest) {
    return hasMessage && guestInfo.name.trim() && guestInfo.email.trim()
  }
  
  return hasMessage
})

const handleContact = async () => {
  if (!authStore.token) {
    // Pas de token du tout, créer une session invité
    await authStore.createGuestSession()
  }
  
  // Rediriger directement vers la page des messages avec le partenaire sélectionné
  try {
    // Stocker l'ID du partenaire pour initier la conversation
    chatStore.selectedPartenaire = props.partenaire
    
    // Rediriger vers la page messages appropriée selon le rôle
    if (authStore.isAuthenticated && !authStore.isGuest) {
      router.push('/messages')
    } else {
      // Pour les invités, ouvrir quand même l'interface mais avec une note
      router.push('/messages')
    }
  } catch (err) {
    console.error('Erreur lors de l\'ouverture des messages:', err)
    // Fallback: ouvrir le modal si la redirection échoue
    showModal.value = true
    error.value = ''
  }
}

const closeModal = () => {
  showModal.value = false
  error.value = ''
  messageForm.sujet = ''
  messageForm.message = ''
  guestInfo.name = ''
  guestInfo.email = ''
  guestInfo.provided = false
}

const sendMessage = async () => {
  if (!canSendMessage.value) return

  try {
    isSending.value = true
    error.value = ''

    // Si invité, mettre à jour les infos dans le token
    if (authStore.isGuest && !guestInfo.provided) {
      await authStore.createGuestSession({
        name: guestInfo.name.trim(),
        email: guestInfo.email.trim()
      })
      guestInfo.provided = true
    }

    // Créer la conversation
    const conversation = await chatStore.createConversation(
      props.partenaire.id,
      messageForm.sujet.trim() || `Message pour ${props.partenaire.nom}`,
      messageForm.message.trim()
    )

    emit('conversation-created', conversation)
    closeModal()

    // Rediriger vers la page des messages si l'utilisateur est connecté
    if (authStore.isAuthenticated) {
      router.push('/messages')
    } else {
      // Pour les invités, afficher un message de confirmation
      alert('Votre message a été envoyé ! Le partenaire pourra vous répondre par email.')
    }

  } catch (err) {
    error.value = err.message || 'Erreur lors de l\'envoi du message'
  } finally {
    isSending.value = false
  }
}
</script>
