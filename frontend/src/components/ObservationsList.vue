<template>
  <div>
    <div v-if="!observations.length" class="px-6 py-10 text-center text-gray-400 text-sm">
      No observations recorded yet.
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm text-left">
        <thead class="bg-gray-50 text-gray-500 uppercase text-xs tracking-wide">
          <tr>
            <th class="px-4 py-3">Customer</th>
            <th class="px-4 py-3">Occupation</th>
            <th class="px-4 py-3">Item</th>
            <th class="px-4 py-3">Placed</th>
            <th class="px-4 py-3">Received</th>
            <th class="px-4 py-3">Wait</th>
            <th class="px-4 py-3">Rating</th>
            <th class="px-4 py-3">Recorded</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="obs in observations" :key="obs.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-800">{{ obs.customer_name }}</td>
            <td class="px-4 py-3 capitalize text-gray-600">{{ obs.occupation }}</td>
            <td class="px-4 py-3 capitalize text-gray-600">{{ obs.ordered_item }}</td>
            <td class="px-4 py-3 text-gray-600 font-mono">{{ formatTime(obs.time_order_placed) }}</td>
            <td class="px-4 py-3 text-gray-600 font-mono">{{ formatTime(obs.time_order_received) }}</td>
            <td class="px-4 py-3 text-gray-600">{{ formatWait(obs.time_order_placed, obs.time_order_received) }}</td>
            <td class="px-4 py-3">
              <span
                :class="ratingColor(obs.rating)"
                class="inline-block px-2 py-0.5 rounded-full text-xs font-semibold"
              >{{ obs.rating }}/10</span>
            </td>
            <td class="px-4 py-3 text-gray-400">{{ formatDate(obs.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({ observations: { type: Array, default: () => [] } })

function toSeconds(t) {
  const s = String(t).padStart(6, '0')
  return parseInt(s.slice(0, 2)) * 3600 + parseInt(s.slice(2, 4)) * 60 + parseInt(s.slice(4, 6))
}
function formatWait(placed, received) {
  const diff = toSeconds(received) - toSeconds(placed)
  if (diff < 0) return '—'
  const m = Math.floor(diff / 60), s = Math.round(diff % 60)
  return m > 0 ? `${m}m ${s}s` : `${s}s`
}
function formatTime(t) {
  const s = String(t).padStart(6, '0')
  return `${s.slice(0,2)}:${s.slice(2,4)}:${s.slice(4,6)}`
}
function ratingColor(r) {
  if (r >= 8) return 'bg-green-100 text-green-700'
  if (r >= 5) return 'bg-yellow-100 text-yellow-700'
  return 'bg-red-100 text-red-700'
}
function formatDate(iso) {
  return new Date(iso).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>
