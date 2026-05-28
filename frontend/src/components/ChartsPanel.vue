<template>
  <div>
    <div class="p-6 border-b border-gray-100">
      <h2 class="text-2xl font-bold text-gray-800">Charts</h2>
    </div>

    <div v-if="!observations.length" class="px-6 py-10 text-center text-gray-400 text-sm">
      No observations recorded yet.
    </div>

    <template v-else>
      <!-- Avg wait time -->
      <div class="px-6 py-5 border-b border-gray-100">
        <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-4">Avg Wait Time by Item</h3>
        <div class="space-y-3">
          <div v-for="item in avgWaitByItem" :key="item.label" class="flex items-center gap-3">
            <span class="w-14 text-sm capitalize text-gray-600 shrink-0">{{ item.label }}</span>
            <div class="flex-1 bg-gray-100 rounded-full h-4 overflow-hidden">
              <div
                class="h-4 rounded-full transition-all duration-500"
                :class="item.bgColor"
                :style="{ width: item.pct + '%' }"
              />
            </div>
            <span class="w-16 text-right text-sm text-gray-500 shrink-0 font-mono">{{ item.display }}</span>
          </div>
        </div>
      </div>

      <!-- Drink tendencies by occupation -->
      <div class="px-6 py-5 border-b border-gray-100">
        <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Drink Tendencies by Occupation</h3>
        <div class="flex gap-4 mb-4">
          <span v-for="item in ITEMS" :key="item.label" class="flex items-center gap-1.5 text-xs text-gray-500">
            <span class="inline-block w-2.5 h-2.5 rounded-sm" :class="item.bgColor" />
            {{ item.label }}
          </span>
        </div>
        <div class="space-y-3">
          <div v-for="row in drinksByOccupation" :key="row.occupation" class="flex items-center gap-3">
            <span class="w-24 text-sm capitalize text-gray-600 shrink-0">{{ row.occupation }}</span>
            <div class="flex-1 flex h-5 rounded-full overflow-hidden bg-gray-100">
              <div
                v-for="seg in row.segments"
                :key="seg.label"
                :class="seg.bgColor"
                :style="{ width: seg.pct + '%' }"
                :title="`${seg.label}: ${seg.count} (${Math.round(seg.pct)}%)`"
                class="transition-all duration-500"
              />
            </div>
            <span class="w-16 text-right text-xs text-gray-400 shrink-0">{{ row.total }} orders</span>
          </div>
        </div>
      </div>

      <!-- Scatter: wait time vs satisfaction -->
      <div class="px-6 py-5">
        <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Wait Time vs. Satisfaction</h3>
        <div class="flex gap-4 mb-3">
          <span v-for="item in ITEMS" :key="item.label" class="flex items-center gap-1.5 text-xs text-gray-500">
            <span class="inline-block w-2.5 h-2.5 rounded-full" :class="item.bgColor" />
            {{ item.label }}
          </span>
        </div>
        <svg
          :viewBox="`0 0 ${SVG_W} ${SVG_H}`"
          class="w-full"
          @mouseleave="tooltip = null"
        >
          <line v-for="tick in yTicks" :key="'gy'+tick.val" :x1="ML" :y1="tick.y" :x2="SVG_W-MR" :y2="tick.y" stroke="#f3f4f6" stroke-width="1" />
          <line v-for="tick in xTicks" :key="'gx'+tick.val" :x1="tick.x" :y1="MT" :x2="tick.x" :y2="SVG_H-MB" stroke="#f3f4f6" stroke-width="1" />
          <line :x1="ML" :y1="MT" :x2="ML" :y2="SVG_H-MB" stroke="#e5e7eb" stroke-width="1" />
          <line :x1="ML" :y1="SVG_H-MB" :x2="SVG_W-MR" :y2="SVG_H-MB" stroke="#e5e7eb" stroke-width="1" />
          <text v-for="tick in yTicks" :key="'ly'+tick.val" :x="ML-8" :y="tick.y+4" text-anchor="end" font-size="10" fill="#9ca3af">{{ tick.val }}</text>
          <text v-for="tick in xTicks" :key="'lx'+tick.val" :x="tick.x" :y="SVG_H-MB+14" text-anchor="middle" font-size="10" fill="#9ca3af">{{ tick.label }}</text>
          <text :x="ML + plotW/2" :y="SVG_H-2" text-anchor="middle" font-size="10" fill="#6b7280">Wait time (seconds)</text>
          <text :x="10" :y="MT + plotH/2" text-anchor="middle" font-size="10" fill="#6b7280" :transform="`rotate(-90,10,${MT+plotH/2})`">Rating</text>
          <circle
            v-for="(pt, i) in scatterPoints" :key="i"
            :cx="pt.cx" :cy="pt.cy" r="5"
            :fill="pt.fill" fill-opacity="0.8"
            stroke="white" stroke-width="1"
            class="cursor-pointer"
            @mouseenter="tooltip = pt"
          />
          <g v-if="tooltip">
            <rect :x="tb.x" :y="tb.y" :width="tb.w" height="52" rx="4" fill="white" stroke="#e5e7eb" stroke-width="1" filter="url(#shad)" />
            <text :x="tb.x+8" :y="tb.y+15" font-size="11" font-weight="600" fill="#1f2937">{{ tooltip.name }}</text>
            <text :x="tb.x+8" :y="tb.y+29" font-size="10" fill="#6b7280">Wait: {{ tooltip.waitLabel }}</text>
            <text :x="tb.x+8" :y="tb.y+42" font-size="10" fill="#6b7280">Rating: {{ tooltip.rating }}/10 · {{ tooltip.item }}</text>
            <defs>
              <filter id="shad" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#00000018" />
              </filter>
            </defs>
          </g>
        </svg>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({ observations: { type: Array, default: () => [] } })

const tooltip = ref(null)

const ITEMS = [
  { label: 'coffee', bgColor: 'bg-amber-400',  fill: '#fbbf24' },
  { label: 'tea',    bgColor: 'bg-emerald-400', fill: '#34d399' },
  { label: 'juice',  bgColor: 'bg-orange-400',  fill: '#fb923c' },
]
const ITEM_FILL = Object.fromEntries(ITEMS.map(i => [i.label, i.fill]))
const OCCUPATIONS = ['professional', 'student', 'unemployed']

const SVG_W = 560, SVG_H = 260
const ML = 44, MR = 20, MT = 16, MB = 36
const plotW = SVG_W - ML - MR
const plotH = SVG_H - MT - MB

function toSeconds(t) {
  const s = String(t).padStart(6, '0')
  return parseInt(s.slice(0, 2)) * 3600 + parseInt(s.slice(2, 4)) * 60 + parseInt(s.slice(4, 6))
}
function waitSecs(placed, received) {
  const d = toSeconds(received) - toSeconds(placed)
  return d >= 0 ? d : null
}
function fmtSecs(secs) {
  const m = Math.floor(secs / 60), s = Math.round(secs % 60)
  return m > 0 ? `${m}m ${s}s` : `${s}s`
}

const avgWaitByItem = computed(() => {
  const totals = {}
  for (const o of props.observations) {
    const w = waitSecs(o.time_order_placed, o.time_order_received)
    if (w === null) continue
    if (!totals[o.ordered_item]) totals[o.ordered_item] = { sum: 0, count: 0 }
    totals[o.ordered_item].sum += w
    totals[o.ordered_item].count++
  }
  const avgs = ITEMS.map(({ label, bgColor }) => {
    const e = totals[label]
    return { label, bgColor, avg: e ? e.sum / e.count : 0 }
  })
  const max = Math.max(...avgs.map(a => a.avg), 1)
  return avgs.map(a => ({ ...a, pct: (a.avg / max) * 100, display: a.avg ? fmtSecs(a.avg) : '—' }))
})

const drinksByOccupation = computed(() =>
  OCCUPATIONS.map(occupation => {
    const sub = props.observations.filter(o => o.occupation === occupation)
    const total = sub.length
    const segments = ITEMS.map(({ label, bgColor }) => {
      const count = sub.filter(o => o.ordered_item === label).length
      return { label, bgColor, count, pct: total ? (count / total) * 100 : 0 }
    })
    return { occupation, total, segments }
  })
)

const scatterPoints = computed(() => {
  const pts = props.observations.flatMap(o => {
    const w = waitSecs(o.time_order_placed, o.time_order_received)
    return w === null ? [] : [{ wait: w, rating: o.rating, name: o.customer_name, item: o.ordered_item }]
  })
  const maxWait = Math.max(...pts.map(p => p.wait), 1)
  return pts.map(pt => ({
    ...pt,
    cx: ML + (pt.wait / maxWait) * plotW,
    cy: MT + plotH - ((pt.rating - 1) / 9) * plotH,
    fill: ITEM_FILL[pt.item] ?? '#94a3b8',
    waitLabel: fmtSecs(pt.wait),
  }))
})

const yTicks = computed(() =>
  [1, 3, 5, 7, 9, 10].map(val => ({ val, y: MT + plotH - ((val - 1) / 9) * plotH }))
)
const xTicks = computed(() => {
  const maxWait = Math.max(...scatterPoints.value.map(p => p.wait), 1)
  const step = Math.ceil(maxWait / 5 / 30) * 30
  const ticks = []
  for (let s = 0; s <= maxWait; s += step)
    ticks.push({ val: s, label: s >= 60 ? `${Math.floor(s/60)}m` : `${s}s`, x: ML + (s / maxWait) * plotW })
  return ticks
})
const tb = computed(() => {
  if (!tooltip.value) return {}
  const w = 150, h = 52, pad = 8
  let x = tooltip.value.cx + pad, y = tooltip.value.cy - h / 2
  if (x + w > SVG_W - MR) x = tooltip.value.cx - w - pad
  if (y < MT) y = MT
  if (y + h > SVG_H - MB) y = SVG_H - MB - h
  return { x, y, w }
})
</script>
