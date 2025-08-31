<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-100 via-white to-orange-50">
    <form @submit.prevent="handleLogin" class="bg-white shadow-xl rounded-xl p-8 w-full max-w-md space-y-6">
      <h2 class="text-2xl font-bold text-center text-gray-800">Connexion</h2>

      <!-- Sélecteur de rôle -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Se connecter en tant que :</label>
        <select v-model="role" class="w-full p-2 border rounded-md focus:ring-orange-400 focus:outline-none">
          <option value="admin">Admin</option>
          <option value="partenaire">Partenaire</option>
          <option value="client">Utilisateur</option>
        </select>
      </div>

      <!-- Email -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input v-model="email" type="email" required class="w-full p-3 border rounded-md focus:ring-orange-400 focus:outline-none" />
      </div>

      <!-- Mot de passe -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
        <input v-model="password" type="password" required class="w-full p-3 border rounded-md focus:ring-orange-400 focus:outline-none" />
      </div>

      <!-- Bouton -->
      <button type="submit" class="w-full bg-orange-500 text-white py-2 rounded-md hover:bg-orange-600 transition">
        Se connecter
      </button>

      <!-- Message d'erreur -->
      <p v-if="error" class="text-sm text-red-500 text-center">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const email = ref('')
const password = ref('')
const role = ref('client') 
const error = ref('')
const router = useRouter()
const authStore = useAuthStore()

async function handleLogin() {
  error.value = ''
  try {
    console.log(role.value)
    
    const result = await authStore.login({
      email: email.value,
      password: password.value,
      role: role.value
    })

    if (result.success) {
      if (role.value === 'admin') {
        router.push('/admin/dashboard')
      } else if (role.value === 'partenaire') {
        router.push('/partenaire/dashboard')
      } else {
        router.push('/')
      }
    } else {
      error.value = result.error || 'Identifiants incorrects'
    }
  } catch (err) {
    error.value = 'Erreur de connexion'
    console.error('Login error:', err)
  }
}
</script>
