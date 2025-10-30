<template>
  <div
    class="relative min-h-screen bg-gradient-to-br from-blue-400 via-blue-300 to-blue-400 flex flex-col items-center justify-center p-8"
  >
    <!-- Tombol Logout -->
    <button
      @click="logout"
      class="fixed top-5 right-6 px-5 py-2 rounded-lg font-semibold bg-gradient-to-r from-red-500 to-red-600 text-white shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300"
    >
      Logout
    </button>

    <!-- Header -->
    <div class="text-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-800 drop-shadow-sm tracking-tight">
        Dashboard Pengguna
      </h1>
    </div>

    <!-- Search Bar -->
    <div class="flex justify-center mb-4 w-full">
      <SearchBar @search="filterUsers" class="w-full max-w-md" />
    </div>

    <!-- User Table -->
    <div
      class="card bg-white shadow-2xl border border-gray-200 w-full max-w-5xl mx-auto rounded-2xl overflow-hidden"
    >
      <div class="card-body overflow-x-auto px-6 py-4">
        <UserTable :users="filteredUsers" @openUpdate="openUpdateModal" @deleteUser="deleteUser" />
      </div>
    </div>

    <!-- Modal Update -->
    <transition name="fade">
      <div
        v-if="isUpdateModalVisible"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 relative animate-fade-in-up"
        >
          <button
            @click="closeUpdateModal"
            class="absolute right-4 top-3 text-gray-500 hover:text-gray-800 text-2xl transition"
          >
            ✕
          </button>
          <h3 class="text-2xl font-semibold text-center text-emerald-600 mb-5">
            ✏️ Edit Data Pengguna
          </h3>
          <UpdateUser :userId="selectedUserId" @updated="handleUserUpdated" />
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import api from '../services/api'
import UpdateUser from './UpdateUser.vue'
import UserTable from './UserTable.vue'
import SearchBar from '../components/SearchBar.vue'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

export default {
  name: 'DashboardPage',
  components: { UpdateUser, UserTable, SearchBar },
  data() {
    return {
      users: [],
      filteredUsers: [],
      isUpdateModalVisible: false,
      selectedUserId: null,
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        const res = await api.get('/users')
        this.users = res.data
        this.filteredUsers = res.data
      } catch (err) {
        console.error('Gagal memuat data:', err)
      }
    },
    async deleteUser(id) {
      const user = this.users.find((u) => u.id === id)
      const result = await Swal.fire({
        title: 'Are you sure?',
        text: `User "${user.nama}" akan dihapus dan tidak bisa dikembalikan!`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Batal',
        reverseButtons: true,
      })

      if (result.isConfirmed) {
        try {
          await api.delete(`/users/${id}`)
          await Swal.fire({
            title: 'Deleted!',
            text: `User "${user.nama}" berhasil dihapus.`,
            icon: 'success',
            timer: 2000,
            showConfirmButton: false,
          })
          this.fetchUsers()
        } catch (err) {
          Swal.fire({
            title: 'Gagal!',
            text: 'User gagal dihapus.',
            icon: 'error',
          })
          console.error(err)
        }
      }
    },
    openUpdateModal(userId) {
      this.selectedUserId = userId
      this.isUpdateModalVisible = true
    },
    closeUpdateModal() {
      this.isUpdateModalVisible = false
      this.selectedUserId = null
    },
    handleUserUpdated() {
      this.fetchUsers()
      this.closeUpdateModal()
      Swal.fire({
        title: 'Berhasil!',
        text: 'Data pengguna berhasil diperbarui!',
        icon: 'success',
        timer: 2000,
        showConfirmButton: false,
      })
    },
    filterUsers(query) {
      if (!query) {
        this.filteredUsers = this.users
      } else {
        const lower = query.toLowerCase()
        this.filteredUsers = this.users.filter(
          (u) =>
            u.username.toLowerCase().includes(lower) ||
            u.nama.toLowerCase().includes(lower) ||
            u.email.toLowerCase().includes(lower),
        )
      }
    },
    async logout() {
      const result = await Swal.fire({
        title: 'Logout?',
        text: 'Apakah Anda yakin ingin logout?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ya, Logout',
        cancelButtonText: 'Batal',
      })

      if (result.isConfirmed) {
        try {
          await api.post('/users/logout')
        } catch (error) {
          console.warn('Logout API error:', error)
        } finally {
          localStorage.removeItem('token')
          this.router.push('/')
        }
      }
    },
  },
}
</script>
