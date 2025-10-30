<template>
  <div class="login-page">
    <!-- BAGIAN KIRI: GAMBAR -->
    <div class="login-image">
      <img src="@/assets/Select player-cuate.svg" alt="Login Illustration" />
    </div>

    <!-- BAGIAN KANAN: FORM -->
    <div class="login-container">
      <div class="login-form">
        <h1 class="title">Selamat Datang</h1>
        <p class="subtitle">Silakan login untuk melanjutkan</p>

        <form @submit.prevent="loginUser" class="space-y-4">
          <div class="form-group">
            <label>Username</label>
            <input v-model="username" type="text" placeholder="Masukkan username" required />
          </div>

          <div class="form-group">
            <label>Password</label>
            <input v-model="password" type="password" placeholder="Masukkan password" required />
          </div>

          <div class="button-group">
            <button type="submit" class="btn btn-login">Login</button>
            <button type="button" class="btn btn-register" @click="goRegister">Registrasi</button>
          </div>

          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import Swal from 'sweetalert2'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const loginUser = async () => {
  try {
    const response = await api.post('/users/login', {
      username: username.value,
      password: password.value,
    })

    if (response.data.token) {
      localStorage.setItem('token', response.data.token)
    }

    Swal.fire({
      title: response.data.message || 'Login berhasil!',
      icon: 'success',
      draggable: true,
    })

    router.push('/dashboard')
  } catch (error) {
    console.error(error)
    errorMessage.value = error.response?.data?.message || 'Login gagal, coba lagi.'

    Swal.fire({
      title: errorMessage.value,
      icon: 'error',
      draggable: true,
    })
  }
}

const goRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-page {
  display: flex;
  height: 100vh;
  background: linear-gradient(to right, #f5f7fa, #e4f0f6);
}

/* BAGIAN KIRI */
.login-image {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #007bff;
}

.login-image img {
  width: 75%;
  max-width: 480px;
  animation: float 4s ease-in-out infinite;
}

/* ANIMASI RINGAN */
@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

/* BAGIAN FORM */
.login-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
}

.login-form {
  width: 100%;
  max-width: 380px;
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-align: center;
  color: #333;
}

.subtitle {
  text-align: center;
  margin-bottom: 2rem;
  color: #777;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: #555;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  transition:
    border 0.3s ease,
    box-shadow 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 6px rgba(66, 185, 131, 0.3);
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 1rem;
}

.btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-login {
  background-color: #42b983;
}

.btn-login:hover {
  background-color: #36a172;
}

.btn-register {
  background-color: #007bff;
}

.btn-register:hover {
  background-color: #0066d6;
}

.error {
  margin-top: 1rem;
  color: #e63946;
  text-align: center;
  font-weight: 500;
}

/* RESPONSIVE */
@media (max-width: 900px) {
  .login-page {
    flex-direction: column;
  }

  .login-image {
    display: none;
  }

  .login-container {
    flex: unset;
    height: 100vh;
    justify-content: center;
    background: linear-gradient(to bottom, #f5f7fa, #e4f0f6);
  }

  .login-form {
    width: 90%;
    max-width: 400px;
    box-shadow: none;
    border: 1px solid #eee;
  }
}
</style>
