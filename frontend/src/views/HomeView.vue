<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(JSON.parse(localStorage.getItem('auth_user') || 'null'))

async function handleLogout() {
  const token = localStorage.getItem('auth_token')
  await fetch('/api/auth/logout/', {
    method: 'POST',
    headers: { Authorization: `Token ${token}` },
  })
  localStorage.removeItem('auth_token')
  localStorage.removeItem('auth_user')
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-2xl mx-auto">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-semibold text-gray-800">Home</h1>
          <p v-if="user" class="text-sm text-gray-500 mt-1">
            Signed in as <span class="font-medium">{{ user.first_name }} {{ user.last_name }}</span>
            <span v-if="user.is_staff" class="ml-2 text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">Manager</span>
          </p>
        </div>
        <button
          @click="handleLogout"
          class="text-sm text-gray-500 hover:text-gray-800 border border-gray-300 rounded-lg px-3 py-1.5 transition-colors"
        >
          Sign out
        </button>
      </div>

      <p class="text-gray-400 text-sm">Build your expense module here.</p>
    </div>
  </div>
</template>
