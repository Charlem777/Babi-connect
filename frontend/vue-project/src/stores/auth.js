import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  // État
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const role = ref(localStorage.getItem('role') || 'guest')
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => {
    const result = !!token.value && role.value !== 'guest'
    console.log('🔐 isAuthenticated computed:', {
      hasToken: !!token.value,
      role: role.value,
      result: result
    })
    return result
  })
  const isGuest = computed(() => role.value === 'guest' || !token.value)
  const isPartenaire = computed(() => role.value === 'partenaire')
  const isClient = computed(() => role.value === 'client')
  const isAdmin = computed(() => role.value === 'admin')

  // Configuration axios
  const setupAxiosInterceptors = () => {
    // Clear existing interceptors to avoid duplicates
    api.interceptors.request.clear()
    api.interceptors.response.clear()
    
    api.interceptors.request.use(
      (config) => {
        const currentToken = token.value || localStorage.getItem('token')
        if (currentToken) {
          config.headers.Authorization = `Bearer ${currentToken}`
          console.log('🔐 Adding token to request:', currentToken.substring(0, 20) + '...')
        } else {
          console.log('⚠️ No token available for request')
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          console.log('🔒 401 error, logging out')
          await logout()
        }
        return Promise.reject(error)
      }
    )
  }

  // Actions
  const login = async (credentials) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('🔐 Login attempt:', credentials.email, credentials.role)

      const response = await api.post('/login', credentials)
      const { token: newToken, role: newRole, user: userData } = response.data

      console.log('✅ Login successful:', { newToken: newToken?.substring(0, 20) + '...', newRole, userData })

      token.value = newToken
      role.value = newRole
      user.value = userData

      localStorage.setItem('token', newToken)
      localStorage.setItem('role', newRole)
      localStorage.setItem('user', JSON.stringify(userData))

      console.log('🔄 Auth state updated:', {
        token: !!token.value,
        role: role.value,
        isAuthenticated: isAuthenticated.value,
        user: user.value?.nom || user.value?.name
      })

      return { success: true, user: userData }
    } catch (err) {
      console.error('❌ Login failed:', err)
      error.value = err.response?.data?.error || 'Erreur de connexion'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await api.post('/register', userData)
      const { token: newToken, role: newRole, user: newUser } = response.data

      token.value = newToken
      role.value = newRole
      user.value = newUser

      localStorage.setItem('token', newToken)
      localStorage.setItem('role', newRole)
      localStorage.setItem('user', JSON.stringify(newUser))

      return { success: true, user: newUser }
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur lors de l\'inscription'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const createGuestSession = async (guestData = {}) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await api.post('/guest-session', guestData)
      const { token: guestToken, guest } = response.data

      token.value = guestToken
      role.value = 'guest'
      user.value = guest

      localStorage.setItem('token', guestToken)
      localStorage.setItem('role', 'guest')
      localStorage.setItem('user', JSON.stringify(guest))

      return { success: true, guest }
    } catch (err) {
      error.value = err.response?.data?.error || 'Erreur création session invité'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const verifyToken = async () => {
    if (!token.value) {
      await createGuestSession()
      return
    }

    try {
      // Envoyer le token dans l'en-tête Authorization pour verify-token
      const response = await api.post('/verify-token', {}, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      const { valid, role: tokenRole, user: userData, guest } = response.data

      if (valid) {
        role.value = tokenRole
        user.value = tokenRole === 'guest' ? guest : userData
        localStorage.setItem('role', tokenRole)
        localStorage.setItem('user', JSON.stringify(tokenRole === 'guest' ? guest : userData))
      } else {
        await createGuestSession()
      }
    } catch (err) {
      console.log('❌ Erreur vérification token:', err)
      await createGuestSession()
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await api.post('/logout')
      }
    } catch (err) {
      console.error('Erreur lors de la déconnexion:', err)
    } finally {
      token.value = null
      role.value = 'guest'
      user.value = null

      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('user')

      // Créer une nouvelle session invité
      await createGuestSession()
    }
  }

  const requireAuth = () => {
    if (!isAuthenticated.value) {
      throw new Error('Connexion requise pour accéder à cette fonctionnalité')
    }
  }

  const initializeAuth = async () => {
    // Récupérer les données du localStorage
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (err) {
        localStorage.removeItem('user')
      }
    }

    // Vérifier le token ou créer une session invité
    await verifyToken()
    
    // Configurer les intercepteurs axios
    setupAxiosInterceptors()
  }

  return {
    // État
    user,
    token,
    role,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    isGuest,
    isPartenaire,
    isClient,
    isAdmin,
    
    // Actions
    login,
    register,
    createGuestSession,
    verifyToken,
    logout,
    requireAuth,
    initializeAuth
  }
})
