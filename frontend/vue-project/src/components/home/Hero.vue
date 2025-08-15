<template>
  <section class="min-h-[70vh] flex flex-col justify-center items-center text-center bg-gradient-to-b from-indigo-100 to-white px-6">
    
    <h1 class="text-4xl md:text-5xl font-extrabold text-indigo-700 mb-4 leading-tight">
      Connecté à la culture,<br />
      Proche des bonnes affaires
    </h1>
    <p class="text-lg text-gray-600 mb-6 max-w-xl">
      Trouve les partenaires locaux qui te correspondent, explore les offres et découvre une nouvelle façon de connecter avec Abidjan.
    </p>
    <router-link
      to="/partenaires"
      class="inline-block bg-indigo-600 text-white px-6 py-3 rounded-full text-base font-semibold hover:bg-indigo-700 transition"
    >
      Découvrir les partenaires
    </router-link>
  </section>
</template>

<script setup>
// Ce composant est autonome, pas besoin d'import pour l'instant
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.8s ease-out forwards;
}
</style>
