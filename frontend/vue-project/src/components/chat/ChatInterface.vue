<template>
  <div class="flex h-full bg-gray-50">
    <!-- Sidebar - Liste des conversations -->
    <div class="w-full md:w-80 bg-white border-r border-gray-200 flex flex-col" :class="{ 'hidden': showChat && isMobile }">
      <!-- Header -->
      <div class="p-4 border-b border-gray-100">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Messages</h2>
          <div class="flex items-center space-x-2">
            <div v-if="chatStore.unreadCount > 0" 
                 class="bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-[20px] text-center">
              {{ chatStore.unreadCount }}
            </div>
            <button 
              @click="refreshConversations"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Liste des conversations -->
      <div class="flex-1 overflow-y-auto">
        <div v-if="chatStore.isLoading && chatStore.conversations.length === 0" 
             class="p-4 text-center text-gray-500">
          <div class="animate-spin w-6 h-6 border-2 border-orange-500 border-t-transparent rounded-full mx-auto mb-2"></div>
          Chargement...
        </div>

        <div v-else-if="chatStore.conversations.length === 0" 
             class="p-4 text-center text-gray-500">
          <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
          <p class="text-sm">Aucune conversation</p>
        </div>

        <div v-else class="divide-y divide-gray-100">
          <div
            v-for="conversation in chatStore.sortedConversations"
            :key="conversation.id"
            @click="selectConversation(conversation.id)"
            :class="[
              'p-4 cursor-pointer hover:bg-gray-50 transition-colors',
              chatStore.currentConversation?.id === conversation.id ? 'bg-orange-50 border-r-2 border-orange-500' : ''
            ]"
          >
            <div class="flex items-start space-x-3">
              <!-- Avatar -->
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
                  {{ getAvatarText(conversation) }}
                </div>
              </div>

              <!-- Contenu -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <h3 class="text-sm font-medium text-gray-900 truncate">
                    {{ chatStore.getConversationTitle(conversation) }}
                  </h3>
                  <span class="text-xs text-gray-500">
                    {{ chatStore.formatMessageTime(conversation.derniere_activite) }}
                  </span>
                </div>
                
                <!-- Informations client détaillées pour les partenaires -->
                <div v-if="authStore.isPartenaire && conversation.client" class="mt-1">
                  <p class="text-xs text-gray-600">
                    {{ conversation.client.prenom }} {{ conversation.client.nom }}
                  </p>
                  <p class="text-xs text-gray-500">
                    {{ conversation.client.email }}
                  </p>
                </div>
                
                <p v-if="conversation.dernier_message" 
                   class="text-sm text-gray-600 truncate mt-1">
                  {{ conversation.dernier_message.contenu }}
                </p>
                
                <div v-if="conversation.messages_count > 0" 
                     class="flex items-center justify-between mt-2">
                  <span class="text-xs text-gray-400">
                    {{ conversation.messages_count }} message{{ conversation.messages_count > 1 ? 's' : '' }}
                  </span>
                  <div v-if="hasUnreadMessages(conversation)" 
                       class="w-2 h-2 bg-orange-500 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Zone de chat principale -->
    <div class="flex-1 flex flex-col" :class="{ 'hidden': !showChat && isMobile }">
      <!-- Header de la conversation -->
      <div v-if="chatStore.currentConversation" 
           class="p-4 bg-white border-b border-gray-200">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <!-- Bouton retour mobile -->
            <button 
              v-if="isMobile"
              @click="showChat = false"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors md:hidden"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            
            <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
              {{ getAvatarText(chatStore.currentConversation) }}
            </div>
            <div>
              <h3 class="font-medium text-gray-900">
                {{ chatStore.getConversationTitle(chatStore.currentConversation) }}
              </h3>
              <!-- Informations détaillées du client pour les partenaires -->
              <div v-if="authStore.isPartenaire && chatStore.currentConversation.client">
                <p class="text-sm text-gray-600">
                  {{ chatStore.currentConversation.client.prenom }} {{ chatStore.currentConversation.client.nom }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ chatStore.currentConversation.client.email }}
                </p>
              </div>
              <p v-else-if="chatStore.currentConversation.sujet" 
                 class="text-sm text-gray-500">
                {{ chatStore.currentConversation.sujet }}
              </p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <button 
              @click="archiveConversation"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              title="Archiver la conversation"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8l6 6 6-6"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Zone des messages ou formulaire nouvelle conversation -->
      <div v-if="showNewConversationForm && newConversationPartenaire" class="flex-1 flex flex-col">
        <!-- Header nouvelle conversation -->
        <div class="p-4 bg-white border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <button 
                v-if="isMobile"
                @click="showChat = false; showNewConversationForm = false"
                class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors md:hidden"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
              </button>
              
              <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
                {{ newConversationPartenaire.nom.charAt(0).toUpperCase() }}
              </div>
              <div>
                <h3 class="font-medium text-gray-900">
                  Nouveau message à {{ newConversationPartenaire.nom }}
                </h3>
                <p class="text-sm text-gray-500">
                  Écrivez votre message ci-dessous
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Zone de composition -->
        <div class="flex-1 p-4 bg-gray-50">
          <div class="bg-white rounded-lg p-4 shadow-sm">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Sujet (optionnel)
                </label>
                <input
                  v-model="newConversationSubject"
                  type="text"
                  placeholder="Objet de votre message"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Message *
                </label>
                <textarea
                  v-model="newConversationMessage"
                  rows="6"
                  placeholder="Tapez votre message ici..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none"
                ></textarea>
              </div>
              
              <div class="flex space-x-3">
                <button
                  @click="cancelNewConversation"
                  class="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Annuler
                </button>
                <button
                  @click="startNewConversation"
                  :disabled="!newConversationMessage.trim() || isSending"
                  :class="[
                    'flex-1 px-4 py-2 rounded-lg font-medium text-white transition-all',
                    newConversationMessage.trim() && !isSending
                      ? 'bg-orange-500 hover:bg-orange-600'
                      : 'bg-gray-300 cursor-not-allowed'
                  ]"
                >
                  <span v-if="isSending">Envoi...</span>
                  <span v-else>Envoyer</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Zone des messages existants -->
      <div v-else-if="chatStore.currentConversation" 
           class="flex-1 overflow-y-auto p-4 space-y-4">
        <div
          v-for="message in chatStore.currentMessages"
          :key="message.id"
          :class="[
            'flex',
            isOwnMessage(message) ? 'justify-end' : 'justify-start'
          ]"
        >
          <div :class="[
            'max-w-xs lg:max-w-md px-4 py-2 rounded-2xl',
            isOwnMessage(message) 
              ? 'bg-orange-500 text-white' 
              : 'bg-white border border-gray-200 text-gray-900'
          ]">
            <p class="text-sm">{{ message.contenu }}</p>
            <div :class="[
              'text-xs mt-1 flex items-center justify-between',
              isOwnMessage(message) ? 'text-orange-100' : 'text-gray-500'
            ]">
              <span>{{ chatStore.formatMessageTime(message.date_envoi) }}</span>
              <div v-if="isOwnMessage(message)" class="flex items-center space-x-1">
                <svg v-if="message.lu" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                <svg v-else class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Zone de saisie -->
      <div v-if="chatStore.currentConversation" 
           class="p-4 bg-white border-t border-gray-200">
        <form @submit.prevent="sendMessage" class="flex items-end space-x-3">
          <div class="flex-1">
            <textarea
              v-model="newMessage"
              @keydown.enter.prevent="sendMessage"
              placeholder="Tapez votre message..."
              rows="1"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-colors"
              style="min-height: 40px; max-height: 120px;"
            ></textarea>
          </div>
          <button
            type="submit"
            :disabled="!newMessage.trim() || isSending"
            :class="[
              'p-2 rounded-lg transition-all transform',
              newMessage.trim() && !isSending
                ? 'bg-orange-500 text-white hover:bg-orange-600 hover:scale-105 active:scale-95'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            ]"
          >
            <svg v-if="isSending" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
          </button>
        </form>
      </div>

      <!-- État vide -->
      <div v-else class="flex-1 flex items-center justify-center">
        <div class="text-center">
          <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Sélectionnez une conversation</h3>
          <p class="text-gray-500">Choisissez une conversation dans la liste pour commencer à discuter</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useAuthStore } from '@/stores/auth'

const chatStore = useChatStore()
const authStore = useAuthStore()

const newMessage = ref('')
const isSending = ref(false)
const showChat = ref(false)
const isMobile = ref(false)
const showNewConversationForm = ref(false)
const newConversationPartenaire = ref(null)
const newConversationSubject = ref('')
const newConversationMessage = ref('')

const isOwnMessage = (message) => {
  if (authStore.isGuest) {
    return message.expediteur_type === 'guest'
  }
  return message.expediteur_id === authStore.user?.id && 
         message.expediteur_type === authStore.role
}

const getAvatarText = (conversation) => {
  const title = chatStore.getConversationTitle(conversation)
  return title.charAt(0).toUpperCase()
}

const hasUnreadMessages = (conversation) => {
  // Logique simplifiée - dans une vraie app, vous pourriez avoir plus de détails
  return conversation.messages_count > 0 && 
         conversation.dernier_message && 
         !conversation.dernier_message.lu &&
         !isOwnMessage(conversation.dernier_message)
}

const selectConversation = async (conversationId) => {
  try {
    await chatStore.loadConversation(conversationId)
    showChat.value = true
  } catch (error) {
    console.error('Erreur lors de la sélection de la conversation:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || isSending.value) return

  try {
    isSending.value = true
    await chatStore.sendMessage(
      chatStore.currentConversation.id,
      newMessage.value.trim()
    )
    newMessage.value = ''
  } catch (error) {
    console.error('Erreur lors de l\'envoi du message:', error)
  } finally {
    isSending.value = false
  }
}

const archiveConversation = async () => {
  if (!chatStore.currentConversation) return

  try {
    await chatStore.archiveConversation(chatStore.currentConversation.id)
  } catch (error) {
    console.error('Erreur lors de l\'archivage:', error)
  }
}

const refreshConversations = async () => {
  await Promise.all([
    chatStore.loadConversations(),
    chatStore.loadUnreadCount()
  ])
}

const cancelNewConversation = () => {
  showNewConversationForm.value = false
  newConversationPartenaire.value = null
  newConversationSubject.value = ''
  newConversationMessage.value = ''
}

const startNewConversation = async () => {
  if (!newConversationMessage.value.trim() || isSending.value) return

  try {
    isSending.value = true
    await chatStore.startNewConversation(
      newConversationPartenaire.value.id,
      newConversationSubject.value,
      newConversationMessage.value.trim()
    )
    showNewConversationForm.value = false
    newConversationPartenaire.value = null
    newConversationSubject.value = ''
    newConversationMessage.value = ''
  } catch (error) {
    console.error('Erreur lors du démarrage d\'une nouvelle conversation:', error)
  } finally {
    isSending.value = false
  }
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await refreshConversations()
  }
  
  // Vérifier si un partenaire est présélectionné pour initier une conversation
  if (chatStore.selectedPartenaire) {
    // Vérifier si une conversation existe déjà avec ce partenaire
    const existingConversation = chatStore.conversations.find(conv => 
      conv.partenaire_id === chatStore.selectedPartenaire.id
    )
    
    if (existingConversation) {
      // Ouvrir la conversation existante
      await selectConversation(existingConversation.id)
    } else {
      // Préparer une nouvelle conversation (afficher l'interface pour écrire)
      showNewConversationForm.value = true
      newConversationPartenaire.value = chatStore.selectedPartenaire
    }
    
    // Nettoyer la sélection
    chatStore.selectedPartenaire = null
  }
  
  const mediaQuery = window.matchMedia('(max-width: 768px)')
  isMobile.value = mediaQuery.matches
  mediaQuery.addEventListener('change', (event) => {
    isMobile.value = event.matches
  })
})
</script>
