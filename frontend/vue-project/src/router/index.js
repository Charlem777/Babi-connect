import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import PartenairesView from '@/views/PartenairesView.vue'
import Offres from '../components/home/Offres.vue'
import OffresView from '@/views/OffresView.vue'
const routes = [
  {
    path: '/',
    name: 'Accueil',
    component: Home
  },
  {
    path: '/partenaires',
    name: 'Partenaires',
    component: PartenairesView
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
    path: '/partenaires/:slug',
    name: 'ProfilPartenaire',
    component: () => import('@/views/ProfilPartenaire.vue')
  },

  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
