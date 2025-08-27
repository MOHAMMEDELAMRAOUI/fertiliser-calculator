<template>
  <div class="flex gap-2">
    <Button
      v-for="option in options"
      :key="option"
      :label="option"
      :class="{'p-button-raised': option === modelValue}"
      @click="$emit('update:modelValue', option)"
    />
  </div>
</template>

<script setup>
defineProps({ options: Array, modelValue: String })
defineEmits(['update:modelValue'])
</script>
