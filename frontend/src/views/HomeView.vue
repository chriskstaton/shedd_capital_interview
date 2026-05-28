<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-md flex flex-col">

      <!-- Content -->
      <div class="flex-1">
        <CafeOrderForm v-show="activeTab === 'form'" @submitted="onSubmitted" />

        <template v-if="activeTab === 'list'">
          <div class="p-6 flex items-center justify-between border-b border-gray-100">
            <h2 class="text-2xl font-bold text-gray-800">Observations</h2>
            <button @click="fetchObservations" :disabled="loading" class="text-sm text-blue-600 hover:text-blue-800 disabled:opacity-40 font-medium">
              {{ loading ? 'Loading…' : 'Refresh' }}
            </button>
          </div>
          <div v-if="error" class="px-6 py-4 bg-red-50 text-red-700 text-sm">{{ error }}</div>
          <div v-else-if="loading && !observations.length" class="px-6 py-10 text-center text-gray-400 text-sm">Loading…</div>
          <ObservationsList v-else :observations="observations" />
        </template>

        <template v-if="activeTab === 'charts'">
          <div class="p-6 flex items-center justify-between border-b border-gray-100">
            <h2 class="text-2xl font-bold text-gray-800">Visualizations</h2>
            <button @click="fetchObservations" :disabled="loading" class="text-sm text-blue-600 hover:text-blue-800 disabled:opacity-40 font-medium">
              {{ loading ? 'Loading…' : 'Refresh' }}
            </button>
          </div>
          <div v-if="loading && !observations.length" class="px-6 py-10 text-center text-gray-400 text-sm">Loading…</div>
          <ChartsPanel v-else :observations="observations" />
        </template>
      </div>

      <!-- Footer tabs -->
      <div class="flex border-t border-gray-100 sticky bottom-0 bg-white rounded-b-2xl z-10">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="switchTab(tab.id)"
          :class="activeTab === tab.id
            ? 'text-blue-600 border-t-2 border-blue-600 -mt-px bg-white'
            : 'text-gray-400 hover:text-gray-600'"
          class="flex-1 py-3 text-sm font-medium transition-colors"
        >
          {{ tab.label }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import CafeOrderForm from '@/components/CafeOrderForm.vue'
import ObservationsList from '@/components/ObservationsList.vue'
import ChartsPanel from '@/components/ChartsPanel.vue'

const tabs = [
  { id: 'form',   label: 'New Entry' },
  { id: 'list',   label: 'Observations' },
  { id: 'charts', label: 'Visualizations' },
]

const activeTab = ref('form')
const observations = ref([])
const loading = ref(false)
const error = ref('')

async function fetchObservations() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await axios.get('/api/observations/')
    observations.value = data
  } catch {
    error.value = 'Failed to load observations.'
  } finally {
    loading.value = false
  }
}

function switchTab(id) {
  activeTab.value = id
  if ((id === 'list' || id === 'charts') && !observations.value.length) fetchObservations()
}

function onSubmitted() {
  fetchObservations()
}
</script>
