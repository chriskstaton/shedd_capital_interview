<template>
  <div class="max-w-lg mx-auto bg-white rounded-2xl shadow-md overflow-hidden">
    <div class="p-8">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Cafe Order Entry</h2>

    <form @submit.prevent="handleSubmit" class="space-y-5">
      <!-- Customer Name -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Customer Name</label>
        <input
          v-model="form.customerName"
          type="text"
          placeholder="Enter customer name"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Occupation -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
        <select
          v-model="form.occupation"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="" disabled>Select occupation</option>
          <option value="professional">Professional</option>
          <option value="student">Student</option>
          <option value="unemployed">Unemployed</option>
        </select>
      </div>

      <!-- Ordered Item -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Ordered Item</label>
        <select
          v-model="form.orderedItem"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="" disabled>Select item</option>
          <option value="coffee">Coffee</option>
          <option value="tea">Tea</option>
          <option value="juice">Juice</option>
        </select>
      </div>

      <!-- Time Order Placed -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Time Order Placed <span class="text-gray-400 font-normal">(HHMMSS)</span>
        </label>
        <input
          v-model="form.timePlaced"
          type="text"
          placeholder="e.g. 143022"
          maxlength="6"
          pattern="\d{6}"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Time Order Received -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Time Order Received <span class="text-gray-400 font-normal">(HHMMSS)</span>
        </label>
        <input
          v-model="form.timeReceived"
          type="text"
          placeholder="e.g. 143512"
          maxlength="6"
          pattern="\d{6}"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Rating -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Service Rating (1–10)</label>
        <input
          v-model.number="form.rating"
          type="number"
          min="1"
          max="10"
          placeholder="Enter a rating"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        type="submit"
        :disabled="submitting"
        class="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold py-2 rounded-lg transition-colors"
      >
        {{ submitting ? 'Submitting…' : 'Submit' }}
      </button>
    </form>
    </div>

    <footer
      v-if="submitStatus"
      :class="submitStatus === 'success' ? 'bg-green-600' : 'bg-red-600'"
      class="px-8 py-4 text-white text-sm font-medium text-center"
    >
      {{ submitStatus === 'success' ? 'Observation saved successfully.' : statusMessage }}
    </footer>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'

const form = reactive({
  customerName: '',
  occupation: '',
  orderedItem: '',
  timePlaced: '',
  timeReceived: '',
  rating: null,
})

const submitting = ref(false)
const submitStatus = ref('')   // 'success' | 'error' | ''
const statusMessage = ref('')

async function handleSubmit() {
  submitting.value = true
  submitStatus.value = ''
  statusMessage.value = ''

  const payload = {
    customer_name: form.customerName,
    occupation: form.occupation,
    ordered_item: form.orderedItem,
    time_order_placed: Number(form.timePlaced),
    time_order_received: Number(form.timeReceived),
    rating: form.rating,
  }

  console.log(payload)

  try {
    await axios.post('/api/observations/create/', payload)
    submitStatus.value = 'success'
    Object.assign(form, { customerName: '', occupation: '', orderedItem: '', timePlaced: '', timeReceived: '', rating: null })
  } catch (err) {
    submitStatus.value = 'error'
    statusMessage.value = err.response?.data
      ? JSON.stringify(err.response.data)
      : 'Submission failed. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>
