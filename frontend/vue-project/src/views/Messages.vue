<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header de la page -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <h1 class="text-2xl font-bold text-gray-900">Messages</h1>
          <p class="mt-1 text-sm text-gray-600">
            Gérez vos conversations avec les partenaires
          </p>
        </div>
      </div>
    </div>

    <!-- Interface de chat -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 h-[calc(100vh-200px)]">
        <ChatInterface />
      </div>
    </div>
  </div>
</template>

<script setup>
import ChatInterface from '@/components/chat/ChatInterface.vue'
</script>
