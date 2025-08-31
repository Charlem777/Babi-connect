import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import '../../styles/style.css'
import "@fontsource/poppins";

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialiser l'authentification
const authStore = useAuthStore()
authStore.initializeAuth().then(() => {
  app.mount('#app')
})
