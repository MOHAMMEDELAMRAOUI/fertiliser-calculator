<template>
  <div class="targets">
    <div v-for="nut in nutrients" :key="nut.key" class="field">
      <label :for="nut.key">{{ nut.label }}</label>
      <input :id="nut.key" type="number" step="0.01" min="0" v-model.number="innerTarget[nut.key]" />
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  target: {
    type: Object,
    default: () => ({ n: 10, p2o5: 10, k2o: 10, s: 5 })
  }
})
const emit = defineEmits(['update:target'])

const innerTarget = reactive({ ...props.target })

watch(innerTarget, (v) => emit('update:target', v), { deep: true })

const nutrients = [
  { key: 'n', label: 'N' },
  { key: 'p2o5', label: 'P₂O₅' },
  { key: 'k2o', label: 'K₂O' },
  { key: 's', label: 'S' },
]
</script>

<style scoped>
.targets { display: grid; grid-template-columns: repeat(4, minmax(120px, 1fr)); gap: .75rem; margin-bottom: .75rem; }
.field { display: flex; flex-direction: column; gap: .25rem; }
.field input { padding: .5rem .6rem; border: 1px solid #ddd; border-radius: 8px; }
</style>