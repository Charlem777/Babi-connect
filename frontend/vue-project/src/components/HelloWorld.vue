<!-- CategoriePartenaire.vue -->
<template>
  <div class="grid grid-cols-2 gap-4 p-4">
    <div v-for="cat in categories" :key="cat.id" class="bg-white shadow-md p-3 rounded">
      {{ cat.nom }}
    </div>
  </div>
</template>

<script>
export default {
  name: "CategoriePartenaire",
  data() {
    return {
      categories: []
    };
  },
  mounted() {
    fetch("http://localhost:5000/api/categories")
      .then((res) => res.json())
      .then((data) => {
        this.categories = data;
      });
  }
};
</script>

<style scoped>
/* 💅 Tu peux ajouter du style ici ou utiliser Tailwind */
</style>
