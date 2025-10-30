<template>
  <div class="flex flex-col items-center justify-center w-full animate-fade-in-up">
    <form
      @submit.prevent="updateUser"
      class="w-full max-w-md bg-base-100 shadow-lg rounded-2xl p-6 border border-base-content/10"
    >
      <!-- Judul -->

      <div class="form-control mb-3">
        <label class="label">
          <span class="label-text font-semibold">Nama Lengkap</span>
        </label>
        <input
          v-model="nama"
          type="text"
          placeholder="Masukkan nama lengkap"
          class="input input-bordered w-full focus:ring-2 focus:ring-primary transition-all duration-200"
          required
        />
      </div>

      <div class="form-control mb-3">
        <label class="label">
          <span class="label-text font-semibold">Email</span>
        </label>
        <input
          v-model="email"
          type="email"
          placeholder="contoh@email.com"
          class="input input-bordered w-full focus:ring-2 focus:ring-primary transition-all duration-200"
          required
        />
      </div>
      <div class="form-control mb-3">
        <label class="label">
          <span class="label-text font-semibold">Username</span>
        </label>
        <input
          v-model="username"
          type="text"
          placeholder="Masukkan username"
          class="input input-bordered w-full focus:ring-2 focus:ring-primary transition-all duration-200"
          required
        />
      </div>
      <div class="flex justify-center mt-6">
        <button
          type="submit"
          class="btn btn-primary w-1/2 font-semibold tracking-wide hover:scale-105 transition-transform duration-200"
        >
          Simpan Perubahan
        </button>
      </div>

      <!-- Pesan -->
      <p v-if="message" class="text-center mt-4 text-sm text-gray-500">
        {{ message }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const props = defineProps({
  userId: { type: Number, required: true },
})
const emit = defineEmits(['updated'])

const username = ref('')
const email = ref('')
const nama = ref('')
const message = ref('')

const loadUser = async () => {
  try {
    const res = await api.get('/users')
    const user = res.data.find((u) => u.id === props.userId)
    if (user) {
      username.value = user.username
      email.value = user.email
      nama.value = user.nama
    } else {
      message.value = '⚠️ User tidak ditemukan.'
    }
  } catch (err) {
    console.error('Gagal memuat user:', err)
    message.value = '❌ Terjadi kesalahan saat memuat data.'
  }
}

onMounted(loadUser)

const updateUser = async () => {
  try {
    await api.put(`/users/${props.userId}`, {
      username: username.value,
      email: email.value,
      nama: nama.value,
    })
    message.value = '✅ Data berhasil diperbarui!'
    emit('updated')
    setTimeout(() => (message.value = ''), 2500)
  } catch (err) {
    console.error(err)
    message.value = err.response?.data?.message || '❌ Gagal memperbarui data.'
  }
}
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-up {
  animation: fade-in-up 0.5s ease-out;
}
</style>
