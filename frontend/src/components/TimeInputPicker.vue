<template>
  <div>
    <!-- Text input row -->
    <div class="flex items-center gap-2">
      <input
        :value="modelValue"
        @input="onTextInput"
        type="text"
        :placeholder="placeholder"
        maxlength="6"
        pattern="\d{6}"
        class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="button"
        @click="showPicker = !showPicker"
        :class="showPicker ? 'bg-blue-600 text-white border-blue-600' : 'text-gray-400 border-gray-300 hover:text-gray-600 hover:border-gray-400'"
        class="shrink-0 border rounded-lg px-3 py-2 text-xs font-medium transition-colors"
      >
        picker
      </button>
    </div>

    <!-- Spinner picker -->
    <div v-if="showPicker" class="mt-2 flex gap-1 items-center select-none">
      <template v-for="(seg, i) in segments" :key="seg.label">
        <div class="flex flex-col items-center gap-0.5">
          <button
            type="button"
            @click="increment(i)"
            class="w-12 h-8 flex items-center justify-center rounded-md bg-gray-100 hover:bg-gray-200 active:bg-gray-300 text-gray-600 text-base transition-colors"
          >▲</button>
          <div class="w-12 h-9 flex items-center justify-center bg-white border border-gray-200 rounded-md text-lg font-mono font-semibold text-gray-800">
            {{ String(seg.value).padStart(2, '0') }}
          </div>
          <button
            type="button"
            @click="decrement(i)"
            class="w-12 h-8 flex items-center justify-center rounded-md bg-gray-100 hover:bg-gray-200 active:bg-gray-300 text-gray-600 text-base transition-colors"
          >▼</button>
        </div>
        <span v-if="i < 2" class="text-gray-300 font-bold text-xl mb-0.5">:</span>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'e.g. 143022' },
})
const emit = defineEmits(['update:modelValue'])

const showPicker = ref(false)

onMounted(() => {
  if (window.matchMedia('(pointer: coarse)').matches) showPicker.value = true
})

const segments = reactive([
  { label: 'HH', value: 0, max: 23 },
  { label: 'MM', value: 0, max: 59 },
  { label: 'SS', value: 0, max: 59 },
])

function toHHMMSS() {
  return segments.map(s => String(s.value).padStart(2, '0')).join('')
}

function parseIntoSegments(raw) {
  const s = String(raw ?? '').padStart(6, '0')
  if (!/^\d{6}$/.test(s)) return
  segments[0].value = Math.min(parseInt(s.slice(0, 2)), 23)
  segments[1].value = Math.min(parseInt(s.slice(2, 4)), 59)
  segments[2].value = Math.min(parseInt(s.slice(4, 6)), 59)
}

function increment(i) {
  segments[i].value = segments[i].value >= segments[i].max ? 0 : segments[i].value + 1
  emit('update:modelValue', toHHMMSS())
}

function decrement(i) {
  segments[i].value = segments[i].value <= 0 ? segments[i].max : segments[i].value - 1
  emit('update:modelValue', toHHMMSS())
}

function onTextInput(e) {
  const val = e.target.value
  emit('update:modelValue', val)
  if (/^\d{6}$/.test(val)) parseIntoSegments(val)
}

// Keep spinner in sync when the text field changes externally (e.g. form reset)
watch(() => props.modelValue, (val) => {
  if (/^\d{6}$/.test(val)) parseIntoSegments(val)
})
</script>
