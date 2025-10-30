<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 via-blue-300 to-blue-500 p-4"
  >
    <div class="bg-white shadow-2xl rounded-2xl w-full max-w-md p-8 animate-fadeIn">
      <h1 class="text-2xl font-bold text-center text-gray-800 mb-6">Registrasi Akun</h1>

      <form @submit.prevent="registerUser" class="space-y-4">
        <div>
          <label class="block text-gray-700 font-semibold mb-1">Nama Lengkap</label>
          <input
            v-model="nama"
            type="text"
            placeholder="Masukkan nama lengkap"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-400 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-gray-700 font-semibold mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Masukkan email"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-400 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-gray-700 font-semibold mb-1">Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Masukkan username"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-400 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-gray-700 font-semibold mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="Masukkan password"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-400 focus:outline-none"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-green-500 text-white font-semibold py-2 rounded-lg hover:bg-green-600 transition duration-200"
        >
          Registrasi
        </button>

        <button
          type="button"
          class="w-full bg-red-500 text-white font-semibold py-2 rounded-lg hover:bg-red-600 transition duration-200"
          @click="goBack"
        >
          Kembali
        </button>

        <p v-if="message" class="text-center text-red-600 font-medium mt-2">
          {{ message }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import Swal from 'sweetalert2'

const router = useRouter()

const nama = ref('')
const email = ref('')
const username = ref('')
const password = ref('')
const message = ref('')

const registerUser = async () => {
  try {
    const res = await api.post('/users/register', {
      nama: nama.value,
      email: email.value,
      username: username.value,
      password: password.value,
    })

    await Swal.fire({
      title: 'Berhasil!',
      text: res.data.message || 'Registrasi berhasil!',
      icon: 'success',
      timer: 2000,
      showConfirmButton: false,
    })

    router.push('/')
  } catch (err) {
    console.error(err)
    Swal.fire({
      title: 'Gagal!',
      text: err.response?.data?.message || 'Registrasi gagal.',
      icon: 'error',
      confirmButtonColor: '#d33',
    })
  }
}

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.6s ease-in-out;
}
</style>
