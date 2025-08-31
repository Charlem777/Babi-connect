<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Overlay -->
    <div 
      class="absolute inset-0 bg-black/60 backdrop-blur-sm"
      @click="closeModal"
    ></div>
    
    <!-- Modal -->
    <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl transform transition-all">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-100">
        <h2 class="text-2xl font-bold text-gray-900">
          {{ isLoginMode ? 'Connexion' : 'Inscription' }}
        </h2>
        <button 
          @click="closeModal"
          class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6">
        <!-- Mode Invité Banner -->
        <div v-if="authStore.isGuest" class="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
          <div class="flex items-center text-orange-800">
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
            <span class="text-sm font-medium">Mode invité actif - Connectez-vous pour accéder à toutes les fonctionnalités</span>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-800 text-sm">{{ error }}</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Role Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Type de compte
            </label>
            <div class="grid grid-cols-2 gap-3">
              <button
                type="button"
                @click="form.role = 'client'"
                :class="[
                  'p-3 border-2 rounded-lg text-sm font-medium transition-all',
                  form.role === 'client' 
                    ? 'border-orange-500 bg-orange-50 text-orange-700' 
                    : 'border-gray-200 text-gray-600 hover:border-gray-300'
                ]"
              >
                👤 Client
              </button>
              <button
                type="button"
                @click="form.role = 'partenaire'"
                :class="[
                  'p-3 border-2 rounded-lg text-sm font-medium transition-all',
                  form.role === 'partenaire' 
                    ? 'border-green-500 bg-green-50 text-green-700' 
                    : 'border-gray-200 text-gray-600 hover:border-gray-300'
                ]"
              >
                🏪 Partenaire
              </button>
            </div>
          </div>

          <!-- Name fields (only for registration) -->
          <div v-if="!isLoginMode" class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Nom
              </label>
              <input
                v-model="form.nom"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-colors"
                placeholder="Votre nom"
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Prénom
              </label>
              <input
                v-model="form.prenom"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-colors"
                placeholder="Votre prénom"
              >
            </div>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              v-model="form.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-colors"
              placeholder="votre@email.com"
            >
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Mot de passe
            </label>
            <input
              v-model="form.password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-colors"
              placeholder="••••••••"
            >
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.isLoading"
            :class="[
              'w-full py-3 px-4 rounded-lg font-medium text-white transition-all transform',
              form.role === 'partenaire' 
                ? 'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700' 
                : 'bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700',
              authStore.isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-[1.02] active:scale-[0.98]'
            ]"
          >
            <span v-if="authStore.isLoading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Chargement...
            </span>
            <span v-else>
              {{ isLoginMode ? 'Se connecter' : 'S\'inscrire' }}
            </span>
          </button>
        </form>

        <!-- Toggle Mode -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            {{ isLoginMode ? 'Pas encore de compte ?' : 'Déjà un compte ?' }}
            <button
              @click="toggleMode"
              class="font-medium text-orange-600 hover:text-orange-500 transition-colors"
            >
              {{ isLoginMode ? 'S\'inscrire' : 'Se connecter' }}
            </button>
          </p>
        </div>

        <!-- Guest Mode -->
        <div class="mt-4 pt-4 border-t border-gray-100">
          <button
            @click="continueAsGuest"
            class="w-full py-2 px-4 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-lg transition-colors"
          >
            Continuer en tant qu'invité
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'success'])

const authStore = useAuthStore()
const isLoginMode = ref(true)
const error = ref('')

const form = reactive({
  email: '',
  password: '',
  nom: '',
  prenom: '',
  role: 'client'
})

const closeModal = () => {
  emit('close')
  resetForm()
}

const resetForm = () => {
  form.email = ''
  form.password = ''
  form.nom = ''
  form.prenom = ''
  form.role = 'client'
  error.value = ''
}

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  error.value = ''
}

const handleSubmit = async () => {
  error.value = ''
  
  try {
    let result
    
    if (isLoginMode.value) {
      result = await authStore.login({
        email: form.email,
        password: form.password,
        role: form.role
      })
    } else {
      result = await authStore.register({
        email: form.email,
        password: form.password,
        nom: form.nom,
        prenom: form.prenom,
        role: form.role
      })
    }

    if (result.success) {
      emit('success', result.user)
      closeModal()
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Une erreur inattendue s\'est produite'
  }
}

const continueAsGuest = async () => {
  await authStore.createGuestSession()
  closeModal()
}
</script>
