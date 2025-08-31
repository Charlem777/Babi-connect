import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Home from '@/views/Home.vue'
import PartenairesView from '@/views/PartenairesView.vue'
import Offres from '../components/home/Offres.vue'
import OffresView from '@/views/OffresView.vue'
import PartnersPreview from '@/components/home/PartnersPreview.vue'
import LoginView from '@/components/LoginView.vue'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import AdminOffres from '@/components/admin/AdminOffres.vue'
import AdminSecteurs from '@/components/admin/AdminSecteurs.vue'
import AdminPartenaires from '@/components/admin/AdminPartenaires.vue'
import AdminCategories from '@/components/admin/AdminCategories.vue'
import AdminAbonnement from '@/components/admin/AdminAbonnement.vue'
import PartenaireDashboard from '@/components/partenaire/PartenaireDashboard.vue'
import MesOffres from '@/components/partenaire/MesOffres.vue'
import NouvelleOffre from '@/components/partenaire/NouvelleOffre.vue'
import AvisPartenaire from '@/components/partenaire/AvisPartenaire.vue'
import StatCard from '@/components/partenaire/StatCard.vue'
import ProfilPartenaireUpdate from '@/components/partenaire/ProfilPartenaireUpdate.vue'
import PartenaireOffre from '@/components/partenaire/PartenaireOffreUpdate.vue'
import CommentairesPartenaire from '@/components/partenaire/CommentairesPartenaire.vue'
import Messages from '@/views/Messages.vue'
import PartenaireMessages from '@/views/partenaire/PartenaireMessages.vue'

const routes = [
  {
    path: '/',
    name: 'Accueil',
    component: Home
  },
  {
    path: '/partenaire',
    name: 'Partenaires',
    component: PartenairesView
  },
   {
    path: '/partenaires-actifs',
    name: 'PartenairesActifs',
    component: PartnersPreview
  },
  {
    path:'/offres',
    name: 'Offres',
    component: OffresView

  },
  {
    path: '/offres/:id',
    name: 'OffreDetail',
    component: () => import('@/views/OffreDetail.vue'),
  },
  {
    path: '/favoris',
    name: 'Favoris',
    component: () => import('@/views/Favoris.vue'),
    meta: { requiresAuth: true }
  },
    {
    path: '/partenaires/:slug',
    name: 'ProfilPartenaire',
    component: () => import('@/views/ProfilPartenaire.vue')
  },
  {
    path: '/offres/populaires',
    name:'OffrePopulaire',
    component: () => import('@/views/OffresPopulaire.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
  path: '/admin/dashboard',
  component: AdminDashboard,
  meta: { requiresAuth: true }
},

  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  },
  {
    path: '/admin',
    component: () => import('@/components/admin/AdminLayout.vue'),
    children: [
      { path: 'dashboard', component: AdminDashboard },
      { path: 'offres', component: AdminOffres },
      { path: 'partenaires', component: AdminPartenaires },
      { path: 'categories', component: AdminCategories },
      { path: 'secteurs', component: AdminSecteurs },
      { path: 'abonnements', component: AdminAbonnement }

    ]
  },
  {
  path: '/partenaire',
  component: () => import('@/components/partenaire/PartenaireLayout.vue'),
  meta: { requiresAuth: true, role: 'partenaire' },
  children: [
    { path: 'dashboard', component: PartenaireDashboard },
    { path: 'profil', component: ProfilPartenaireUpdate},
    { path: 'offres', component: MesOffres },
    { path: 'offres/nouvelle', component: NouvelleOffre },
    { path: 'messages', component: PartenaireMessages },
    { path: 'avis', component: AvisPartenaire },
    { path: 'stats', component: StatCard },
    { path: 'offres/:id', component: PartenaireOffre },
    { path: 'commentaires', component: CommentairesPartenaire }
  ]
},
  {
    path: '/messages',
    name: 'Messages',
    component: Messages,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navigation pour l'authentification
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Attendre que l'authentification soit initialisée
  if (!authStore.user && !authStore.isGuest) {
    await authStore.initializeAuth()
  }
  
  // Debug: Log authentication state
  console.log('🔐 Router Guard Debug:', {
    path: to.path,
    requiresAuth: to.meta.requiresAuth,
    isAuthenticated: authStore.isAuthenticated,
    role: authStore.role,
    hasToken: !!authStore.token,
    user: authStore.user
  })
  
  // Vérifier si la route nécessite une authentification
  if (to.meta.requiresAuth) {
    // Vérifier si l'utilisateur est authentifié (pas invité et a un token)
    if (authStore.isGuest || !authStore.token || authStore.role === 'guest') {
      console.log('❌ Access denied - not authenticated')
      // Rediriger vers l'accueil avec un message
      next({ 
        path: '/', 
        query: { 
          redirect: to.fullPath,
          message: 'Connexion requise pour accéder à cette page'
        }
      })
      return
    }
    
    // Vérifier le rôle si nécessaire
    if (to.meta.requiresRole && authStore.role !== to.meta.requiresRole) {
      console.log('❌ Access denied - insufficient role')
      next({ 
        path: '/', 
        query: { 
          message: 'Accès refusé - rôle insuffisant'
        }
      })
      return
    }
    
    console.log('✅ Access granted')
  }
  
  next()
})

export default router
