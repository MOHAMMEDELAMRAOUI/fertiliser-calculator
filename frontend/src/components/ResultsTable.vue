<template>
  <table class="table" v-if="result?.ingredients?.length">
    <thead>
      <tr>
        <th>Code</th>
        <th>%</th>
        <th>N</th>
        <th>P₂O₅</th>
        <th>K₂O</th>
        <th>S</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in result.ingredients" :key="row.id">
        <td>{{ row.code }}</td>
        <td>{{ row.percentage }}</td>
        <td>{{ row.contribution.n }}</td>
        <td>{{ row.contribution.p2o5 }}</td>
        <td>{{ row.contribution.k2o }}</td>
        <td>{{ row.contribution.s }}</td>
      </tr>
    </tbody>
  </table>
  <p v-else class="muted">Aucun résultat à afficher.</p>

  <div class="summary" v-if="result">
    <div>
      <strong>Total contrib.</strong>
      <ul>
        <li>N : {{ result.total_contribution?.n ?? 0 }}% (cible {{ target.n }}%)</li>
        <li>P₂O₅ : {{ result.total_contribution?.p2o5 ?? 0 }}% (cible {{ target.p2o5 }}%)</li>
        <li>K₂O : {{ result.total_contribution?.k2o ?? 0 }}% (cible {{ target.k2o }}%)</li>
        <li>S : {{ result.total_contribution?.s ?? 0 }}% (cible {{ target.s }}%)</li>
      </ul>
    </div>
    <div>
      <strong>Écarts</strong>
      <ul>
        <li>N : {{ result.variance?.n ?? 0 }}%</li>
        <li>P₂O₅ : {{ result.variance?.p2o5 ?? 0 }}%</li>
        <li>K₂O : {{ result.variance?.k2o ?? 0 }}%</li>
        <li>S : {{ result.variance?.s ?? 0 }}%</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  result: { type: Object, default: null },
  target: { type: Object, default: () => ({ n:0, p2o5:0, k2o:0, s:0 }) }
})
</script>

<style scoped>
.table { width: 100%; border-collapse: collapse; margin-bottom: .5rem; }
.table th, .table td { border-bottom: 1px solid #eee; padding: .5rem .4rem; text-align: left; }
.muted { color: #6b7280; }
.summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: .75rem; }
</style>