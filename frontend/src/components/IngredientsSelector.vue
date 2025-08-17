<template>
  <div class="grid" v-if="ingredients?.length">
    <label v-for="ing in ingredients" :key="ing.id" class="chip">
      <input type="checkbox" :value="ing.id" v-model="innerValue" />
      <div class="row">
        <strong>{{ ing.code }}</strong>
        <span class="badge" :class="{ off: !ing.is_available }">{{ ing.is_available ? 'dispo' : 'off' }}</span>
      </div>
      <div class="name">{{ ing.name }}</div>
      <small>
        N {{ ing.nitrogen_percent }}% · P₂O₅ {{ ing.phosphorus_percent }}% · K₂O {{ ing.potassium_percent }}% · S {{ ing.sulfur_percent }}%
      </small>
    </label>
  </div>
  <p v-else class="muted">Aucun ingrédient.</p>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  ingredients: { type: Array, default: () => [] },
  modelValue: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:modelValue'])

const innerValue = computed({
  get: () => props.modelValue,
  set: v => emit('update:modelValue', v),
})
</script>

<style scoped>
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: .5rem; margin-top: .5rem; }
.chip { display: flex; flex-direction: column; gap: .2rem; border: 1px solid #e5e7eb; border-radius: 12px; padding: .6rem .8rem; }
.row { display: flex; align-items: center; gap: .5rem; }
.badge { font-size: .75rem; padding: .05rem .35rem; border: 1px solid #16a34a; border-radius: .5rem; }
.badge.off { border-color: #9ca3af; color: #6b7280; }
.name { color: #374151; }
.muted { color: #6b7280; }
</style>