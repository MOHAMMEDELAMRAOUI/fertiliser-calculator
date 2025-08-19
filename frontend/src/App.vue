<template>
  <v-app>
    <!-- Header -->
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Mon Projet</v-toolbar-title>
    </v-app-bar>

    <!-- Sidebar -->
    <v-navigation-drawer app v-model="drawer" color="grey-lighten-4">
      <v-list>
        <v-list-item-group>
          <v-list-item v-for="item in menuItems" :key="item.title">
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <!-- Contenu principal -->
    <v-main>
      <v-container class="pa-4">
        <h1>Bienvenue 🚀</h1>
        <p>Ceci est ton contenu principal.</p>
        <v-card class="pa-4 mt-4" max-width="600">
          <v-card-title>Exemple de Carte</v-card-title>
          <v-card-text>
            Tu peux ajouter ici tes formulaires, tableaux ou autres composants Vuetify.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary">Action</v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app color="primary" dark>
      <v-col class="text-center">
        © {{ new Date().getFullYear() }} - Mon Projet
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data: () => ({
    drawer: true,
    menuItems: [
      { title: "Accueil", icon: "mdi-home" },
      { title: "Profil", icon: "mdi-account" },
      { title: "Paramètres", icon: "mdi-cog" },
    ],
  }),
}
</script>
