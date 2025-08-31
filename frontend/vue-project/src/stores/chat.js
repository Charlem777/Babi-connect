import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'
import { useAuthStore } from './auth'

export const useChatStore = defineStore('chat', () => {
  // État
  const conversations = ref([])
  const currentConversation = ref(null)
  const messages = ref([])
  const unreadCount = ref(0)
  const isLoading = ref(false)
  const error = ref(null)
  const selectedPartenaire = ref(null) // Pour initier une nouvelle conversation

  // Getters
  const sortedConversations = computed(() => {
    return [...conversations.value].sort((a, b) => 
      new Date(b.derniere_activite) - new Date(a.derniere_activite)
    )
  })

  const currentMessages = computed(() => {
    return [...messages.value].sort((a, b) => 
      new Date(a.date_envoi) - new Date(b.date_envoi)
    )
  })

  // Actions
  const loadConversations = async () => {
    const authStore = useAuthStore()
    
    if (!authStore.isAuthenticated) {
      conversations.value = []
      return
    }

    try {
      isLoading.value = true
      const response = await api.get('/chat/conversations')
      conversations.value = response.data.conversations || []
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur lors du chargement des conversations'
      console.error('Erreur chargement conversations:', err)
    } finally {
      isLoading.value = false
    }
  }

  const loadConversation = async (conversationId) => {
    try {
      isLoading.value = true
      const response = await api.get(`/chat/conversations/${conversationId}`)
      
      currentConversation.value = response.data.conversation
      messages.value = response.data.messages || []
      
      // Mettre à jour la conversation dans la liste
      const index = conversations.value.findIndex(c => c.id === conversationId)
      if (index !== -1) {
        conversations.value[index] = response.data.conversation
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur lors du chargement de la conversation'
      console.error('Erreur chargement conversation:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const createConversation = async (partenaireId, sujet, messageInitial) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await api.post('/chat/conversations', {
        partenaire_id: partenaireId,
        sujet: sujet,
        message: messageInitial
      })

      const newConversation = response.data.conversation
      
      // Ajouter à la liste des conversations
      conversations.value.unshift(newConversation)
      
      // Charger la conversation complète
      await loadConversation(newConversation.id)
      
      return newConversation
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur lors de la création de la conversation'
      console.error('Erreur création conversation:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const startNewConversation = async (partenaireId, sujet, messageInitial) => {
    try {
      isLoading.value = true
      error.value = null

      const conversation = await createConversation(partenaireId, sujet, messageInitial)
      
      // Charger la conversation complète
      await loadConversation(conversation.id)
      
      return conversation
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur lors de la création de la conversation'
      console.error('Erreur création conversation:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const sendMessage = async (conversationId, contenu, typeMessage = 'text') => {
    try {
      const response = await api.post(`/chat/conversations/${conversationId}/messages`, {
        contenu,
        type_message: typeMessage
      })

      const newMessage = response.data.message
      
      // Ajouter le message à la liste
      messages.value.push(newMessage)
      
      // Mettre à jour la dernière activité de la conversation
      if (currentConversation.value?.id === conversationId) {
        currentConversation.value.derniere_activite = newMessage.date_envoi
      }
      
      // Mettre à jour dans la liste des conversations
      const convIndex = conversations.value.findIndex(c => c.id === conversationId)
      if (convIndex !== -1) {
        conversations.value[convIndex].derniere_activite = newMessage.date_envoi
        conversations.value[convIndex].dernier_message = newMessage
      }
      
      return newMessage
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur lors de l\'envoi du message'
      console.error('Erreur envoi message:', err)
      throw err
    }
  }

  const markMessageAsRead = async (conversationId, messageId) => {
    try {
      await api.put(`/chat/conversations/${conversationId}/messages/${messageId}/read`)
      
      // Mettre à jour le message localement
      const message = messages.value.find(m => m.id === messageId)
      if (message) {
        message.lu = true
      }
    } catch (err) {
      console.error('Erreur marquage message lu:', err)
    }
  }

  const archiveConversation = async (conversationId) => {
    try {
      await api.put(`/chat/conversations/${conversationId}/archive`)
      
      // Mettre à jour localement
      const conversation = conversations.value.find(c => c.id === conversationId)
      if (conversation) {
        conversation.statut = 'archived'
      }
      
      // Si c'est la conversation courante, la fermer
      if (currentConversation.value?.id === conversationId) {
        currentConversation.value = null
        messages.value = []
      }
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur lors de l\'archivage'
      throw err
    }
  }

  const loadUnreadCount = async () => {
    const authStore = useAuthStore()
    
    if (!authStore.isAuthenticated) {
      unreadCount.value = 0
      return
    }

    try {
      const response = await api.get('/chat/unread-count')
      unreadCount.value = response.data.unread_count || 0
    } catch (err) {
      console.error('Erreur chargement messages non lus:', err)
    }
  }

  const clearCurrentConversation = () => {
    currentConversation.value = null
    messages.value = []
  }

  const clearError = () => {
    error.value = null
  }

  // Utilitaires
  const formatMessageTime = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = (now - date) / (1000 * 60 * 60)
    
    if (diffInHours < 1) {
      return 'À l\'instant'
    } else if (diffInHours < 24) {
      return date.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    } else if (diffInHours < 48) {
      return 'Hier'
    } else {
      return date.toLocaleDateString('fr-FR', { 
        day: 'numeric', 
        month: 'short' 
      })
    }
  }

  const getConversationTitle = (conversation) => {
    if (conversation.sujet) {
      return conversation.sujet
    }
    
    const authStore = useAuthStore()
    
    if (authStore.isPartenaire) {
      return conversation.client 
        ? `${conversation.client.prenom} ${conversation.client.nom}`
        : conversation.guest_name || 'Invité'
    } else {
      return conversation.partenaire?.nom || 'Partenaire'
    }
  }

  return {
    // État
    conversations,
    currentConversation,
    messages,
    unreadCount,
    isLoading,
    error,
    selectedPartenaire,
    
    // Getters
    sortedConversations,
    currentMessages,
    
    // Actions
    loadConversations,
    loadConversation,
    createConversation,
    startNewConversation,
    sendMessage,
    markMessageAsRead,
    archiveConversation,
    loadUnreadCount,
    clearCurrentConversation,
    clearError,
    
    // Utilitaires
    formatMessageTime,
    getConversationTitle
  }
})
