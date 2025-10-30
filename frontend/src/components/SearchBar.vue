<template>
  <div class="flex items-center mb-4">
    <input
      v-model="query"
      type="text"
      placeholder="Cari pengguna..."
      class="border border-gray-300 rounded-l-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-green-400"
    />
    <button
      @click="handleSearch"
      class="bg-green-500 text-white px-4 py-2 rounded-r-md hover:bg-green-600"
    >
      Cari
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const emit = defineEmits(['search'])

const handleSearch = () => {
  const keyword = query.value.trim()

  if (!keyword) {
    emit('search', '')
  } else {
    emit('search', keyword)
  }
}
</script>
