<template>
  <component 
    :is="getCardComponent()" 
    :offre="offre" 
    v-bind="$attrs"
  />
</template>

<script setup>
import { computed } from 'vue'
import OffreCardEvent from '@/components/OffreCardEvent.vue'
import OffreCardService from '@/components/OffreCardService.vue'
import OffreCardShop from '@/components/OffreCardShop.vue'
import OffreCard from '@/components/OffreCard.vue'

const props = defineProps({
  offre: {
    type: Object,
    required: true
  }
})

const getCardComponent = () => {
  // The API returns secteur directly as o.partenaire.secteur.nom
  const secteur = props.offre.secteur || props.offre.partenaire?.secteur
  
  console.log('OffreCardAdapter - Secteur detected:', secteur)
  console.log('Full offre structure:', {
    secteur: props.offre.secteur,
    partenaire: props.offre.partenaire,
    partenaireSecetur: props.offre.partenaire?.secteur
  })
  
  if (!secteur) {
    console.log('No secteur found, using default OffreCard')
    return OffreCard
  }

  const secteurLower = secteur.toLowerCase()
  
  if (secteurLower.includes('événement') || secteurLower.includes('event')) {
    console.log('Using OffreCardEvent for secteur:', secteur)
    return OffreCardEvent
  }
  
  if (secteurLower.includes('service') || secteurLower.includes('beauté') || secteurLower.includes('restauration')) {
    console.log('Using OffreCardService for secteur:', secteur)
    return OffreCardService
  }
  
  if (secteurLower.includes('mode') || secteurLower.includes('shop') || secteurLower.includes('vente')) {
    console.log('Using OffreCardShop for secteur:', secteur)
    return OffreCardShop
  }
  
  console.log('No specific match found, using default OffreCard for secteur:', secteur)
  return OffreCard
}
</script>
