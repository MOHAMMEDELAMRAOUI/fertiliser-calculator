<template>
  <div class="app">
    <h1>Liste des Ingrédients</h1>
    <div v-if="loading">Chargement...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul v-else>
      <li v-for="ingredient in ingredients" :key="ingredient.id">
        {{ ingredient.name }} - 
        N: {{ ingredient.N }}% |
        P₂O₅: {{ ingredient.P2O5 }}% |
        K₂O: {{ ingredient.K2O }}% |
        S: {{ ingredient.S }}%
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      ingredients: [],
      loading: true,
      error: null
    };
  },
  async created() {
    try {
      console.log("Tentative de connexion à l'API...");
      const response = await fetch('http://localhost:5000/api/ingredients');
      console.log("Réponse reçue:", response);
      
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("Données reçues:", data);
      this.ingredients = data;
      
    } catch (err) {
      this.error = `Échec du chargement (${err.message})`;
      console.error("Détails de l'erreur:", err);
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style>
.app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 10px 0;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 4px;
}

.error {
  color: red;
}
</style>