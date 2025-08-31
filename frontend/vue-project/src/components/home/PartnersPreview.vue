<template>
  <section class="py-12 lg:py-20 bg-gradient-to-br from-orange-50/50 via-white to-green-50/30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="text-center mb-12 lg:mb-16">
        <div class="inline-flex items-center gap-2 bg-orange-100 text-orange-600 px-4 py-2 rounded-full text-sm font-medium mb-4">
          <span>🇨🇮</span>
          <span>Talents Ivoiriens</span>
        </div>
        <h2 class="text-3xl lg:text-5xl font-bold text-gray-900 mb-4">
          Découvrez nos 
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-green-600">
            secteurs d'excellence
          </span>
        </h2>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Des professionnels passionnés qui font rayonner le savoir-faire ivoirien
        </p>
      </div>

      <!-- Grid des secteurs -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 lg:gap-8">
        <div
          v-for="(secteur, index) in secteurs"
          :key="secteur.id"
          :style="{ animationDelay: `${index * 100}ms` }"
          class="card-enter group relative bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-500 border border-gray-100 hover:border-orange-200 overflow-hidden hover:-translate-y-2"
        >
          <!-- Image avec overlay -->
          <div class="relative h-48 overflow-hidden">
            <img
              :src="getSecteurImage(secteur)"
              :alt="secteur.nom"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
              @error="handleImageError"
            />
            <!-- Gradient overlay -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <!-- Icône secteur -->
            <div class="absolute top-4 left-4 bg-white/90 backdrop-blur-sm text-orange-600 w-12 h-12 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
              <span class="text-xl">{{ getSecteurIcon(secteur.nom) }}</span>
            </div>

            <!-- Badge nombre d'offres -->
            <div class="absolute top-4 right-4 bg-green-500 text-white px-3 py-1 rounded-full text-xs font-semibold shadow-lg">
              {{ Math.floor(Math.random() * 50) + 10 }}+ offres
            </div>
          </div>

          <!-- Contenu -->
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-3 group-hover:text-orange-600 transition-colors duration-300">
              {{ secteur.nom }}
            </h3>
            <p class="text-gray-600 text-sm leading-relaxed mb-6 line-clamp-2">
              {{ secteur.description || getDefaultDescription(secteur.nom) }}
            </p>

            <!-- Stats rapides -->
            <div class="flex items-center justify-between mb-6 text-xs text-gray-500">
              <div class="flex items-center gap-1">
                <span>⭐</span>
                <span>4.{{ Math.floor(Math.random() * 3) + 6 }}</span>
              </div>
              <div class="flex items-center gap-1">
                <span>👥</span>
                <span>{{ Math.floor(Math.random() * 200) + 50 }}+ pros</span>
              </div>
              <div class="flex items-center gap-1">
                <span>📍</span>
                <span>Abidjan</span>
              </div>
            </div>

            <!-- CTA Button -->
            <router-link
              :to="{
                path: '/offres',
                query: { secteur_slug: secteur.slug }
              }"
              class="group/btn relative w-full inline-flex items-center justify-center px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-semibold rounded-xl hover:from-orange-600 hover:to-orange-700 transition-all duration-300 shadow-lg hover:shadow-xl overflow-hidden"
            >
              <span class="relative z-10 flex items-center gap-2">
                <span>Explorer</span>
                <svg class="w-4 h-4 group-hover/btn:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
              <!-- Shine effect -->
              <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover/btn:translate-x-full transition-transform duration-700"></div>
            </router-link>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="text-center mt-16">
        <router-link
          to="/offres"
          class="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-green-500 to-green-600 text-white font-semibold rounded-2xl hover:from-green-600 hover:to-green-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105"
        >
          <span>Voir tous les secteurs</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const secteurs = ref([])

// Icônes par secteur
const getSecteurIcon = (nom) => {
  const icons = {
    'Événementiel': '🎉',
    'Beauté': '💄',
    'Restauration': '🍽️',
    'Services': '🔧',
    'Mode': '👗',
    'Santé': '🏥',
    'Éducation': '📚',
    'Transport': '🚗',
    'Immobilier': '🏠',
    'Technologie': '💻'
  }
  return icons[nom] || '🏷️'
}

// Descriptions par défaut
const getDefaultDescription = (nom) => {
  const descriptions = {
    'Événementiel': 'Organisez des événements mémorables avec nos experts en événementiel.',
    'Beauté': 'Sublimez votre beauté avec nos professionnels de la beauté et du bien-être.',
    'Restauration': 'Savourez les délices de la gastronomie ivoirienne et internationale.',
    'Services': 'Des services professionnels de qualité pour tous vos besoins.',
    'Mode': 'Découvrez les dernières tendances de la mode ivoirienne et internationale.',
    'Santé': 'Prenez soin de votre santé avec nos professionnels qualifiés.',
    'Éducation': 'Développez vos compétences avec nos experts en formation.',
    'Transport': 'Déplacez-vous en toute sécurité avec nos services de transport.',
    'Immobilier': 'Trouvez le bien immobilier de vos rêves en Côte d\'Ivoire.',
    'Technologie': 'Innovez avec nos solutions technologiques de pointe.'
  }
  return descriptions[nom] || 'Un secteur dynamique et en pleine expansion avec des professionnels qualifiés.'
}

// Images par secteur
const getSecteurImage = (secteur) => {
  // Utiliser une image par défaut ou l'image du secteur si disponible
  return secteur.image || '/src/assets/chris-slupski-eKYgEj1U97k-unsplash.jpg'
}

const handleImageError = (event) => {
  event.target.src = '/src/assets/chris-slupski-eKYgEj1U97k-unsplash.jpg'
}

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5000/api/secteurs')
    const data = await res.json()
    secteurs.value = data.map(s => ({
      id: s.id,
      nom: s.nom,
      description: s.description,
      slug: s.slug,
      image: s.image,
    }))
    console.log(secteurs.value)
  } catch (err) {
    console.error('Erreur chargement secteurs', err)
    // Données de fallback pour le développement
    secteurs.value = [
      { id: 1, nom: 'Événementiel', slug: 'evenementiel', description: 'Organisez des événements mémorables' },
      { id: 2, nom: 'Beauté', slug: 'beaute', description: 'Sublimez votre beauté naturelle' },
      { id: 3, nom: 'Restauration', slug: 'restauration', description: 'Savourez les délices culinaires' },
      { id: 4, nom: 'Services', slug: 'services', description: 'Des services professionnels de qualité' }
    ]
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-enter {
  opacity: 0;
  transform: translateY(30px);
  animation: fadeSlideUp 0.8s ease-out forwards;
}

@keyframes fadeSlideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Effet de perspective au hover */
.group:hover {
  transform: perspective(1000px) rotateX(2deg) rotateY(-2deg) translateY(-8px);
}
</style>
