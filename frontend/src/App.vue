<template>
  <div class="container">
    <h1>Formulation d'engrais (N, P₂O₅, K₂O, S)</h1>

    <section class="card">
      <h2>1) Ingrédients disponibles</h2>
      <div class="actions">
        <button @click="loadIngredients" :disabled="loading">{{ loading ? 'Chargement...' : 'Recharger' }}</button>
        <label>
          <input type="checkbox" v-model="onlyAvailable" /> N'afficher que disponibles
        </label>
        <span v-if="ingredients.length">{{ filteredIngredients.length }} / {{ ingredients.length }} visibles</span>
      </div>
      <IngredientsSelector
        :ingredients="filteredIngredients"
        v-model="selectedIds"
      />
    </section>

    <section class="card">
      <h2>2) Cibles</h2>
      <TargetForm v-model:target="target" />
      <button class="primary" @click="calculate" :disabled="!canCalculate || submitting">
        {{ submitting ? 'Calcul en cours...' : 'Lancer le calcul' }}
      </button>
      <p class="error" v-if="error">{{ error }}</p>
    </section>

    <section v-if="result" class="card">
      <h2>3) Résultats</h2>
      <ResultsTable :result="result" />
      <ContributionChart :target="target" :result="result" />
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { api } from './lib/api'
import IngredientsSelector from './components/IngredientsSelector.vue'
import TargetForm from './components/TargetForm.vue'
import ResultsTable from './components/ResultsTable.vue'
import ContributionChart from './components/ContributionChart.vue'

const ingredients = ref([])
const selectedIds = ref([])
const onlyAvailable = ref(true)
const loading = ref(false)
const submitting = ref(false)
const error = ref('')
const result = ref(null)

const target = ref({ n: 10, p2o5: 10, k2o: 10, s: 5 })
const canCalculate = ref(false)

const filteredIngredients = computed(() =>
  ingredients.value.filter(i => (onlyAvailable.value ? i.is_available : true))
)

watch([selectedIds, target], () => {
  canCalculate.value = selectedIds.value.length > 0
}, { deep: true })

async function loadIngredients() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/api/ingredients')
    ingredients.value = data
  } catch (e) {
    error.value = e?.response?.data?.error || e.message
  } finally {
    loading.value = false
  }
}

async function calculate() {
  if (!canCalculate.value) return
  submitting.value = true
  error.value = ''
  try {
    const payload = { target: target.value, available_ingredients: selectedIds.value }
    const { data } = await api.post('/api/calculate', payload)
    result.value = data
  } catch (e) {
    error.value = e?.response?.data?.error || e.message
  } finally {
    submitting.value = false
  }
}

onMounted(loadIngredients)
</script>

<style scoped>
.container { max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }
.card { background: #fff; border: 1px solid #eee; border-radius: 14px; padding: 1rem 1.25rem; margin-bottom: 1rem; }
.actions { display: flex; gap: .75rem; align-items: center; margin-bottom: .5rem; }
.primary { background: #2563eb; color: #fff; border: 0; border-radius: 10px; padding: .6rem 1rem; cursor: pointer; }
.primary:disabled { opacity: .6; cursor: not-allowed; }
.error { color: #dc2626; }
</style>