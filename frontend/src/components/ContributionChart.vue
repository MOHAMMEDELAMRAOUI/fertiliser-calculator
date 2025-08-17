<template>
  <canvas ref="chartEl" height="120"></canvas>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { Chart } from 'chart.js/auto'

const props = defineProps({
  target: { type: Object, required: true },
  result: { type: Object, required: true },
})

const chartEl = ref(null)
let chartInstance = null

function draw() {
  if (!chartEl.value || !props.result) return
  const labels = ['N','P₂O₅','K₂O','S']
  const targetData = [props.target.n, props.target.p2o5, props.target.k2o, props.target.s].map(Number)
  const r = props.result
  const actualData = [r.total_contribution?.n, r.total_contribution?.p2o5, r.total_contribution?.k2o, r.total_contribution?.s].map(v => Number(v || 0))

  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(chartEl.value.getContext('2d'), {
    type: 'bar',
    data: { labels, datasets: [ { label: 'Cible (%)', data: targetData }, { label: 'Obtenu (%)', data: actualData } ] },
    options: { responsive: true, plugins: { legend: { position: 'top' }, title: { display: true, text: 'Cible vs Contribution totale' } }, scales: { y: { beginAtZero: true } } }
  })
}

onMounted(draw)
watch(() => props.result, draw, { deep: true })
watch(() => props.target, draw, { deep: true })

onBeforeUnmount(() => { if (chartInstance) chartInstance.destroy() })
</script>