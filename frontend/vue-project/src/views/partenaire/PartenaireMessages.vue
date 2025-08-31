<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-xl shadow-sm p-6 border border-orange-100">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Messages</h1>
          <p class="text-gray-600 mt-1">Gérez vos conversations avec les clients</p>
        </div>
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <span class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full font-medium">
            {{ unreadCount }} non lus
          </span>
        </div>
      </div>
    </div>

    <!-- Messages Interface -->
    <div class="bg-white rounded-xl shadow-sm border border-orange-100 overflow-hidden">
      <ChatInterface />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import ChatInterface from '@/components/chat/ChatInterface.vue'

const chatStore = useChatStore()
const unreadCount = ref(0)

onMounted(async () => {
  await chatStore.loadConversations()
  await chatStore.loadUnreadCount()
  unreadCount.value = chatStore.unreadCount
})
</script>

<style scoped>
/* Styles spécifiques pour l'interface partenaire */
</style>
