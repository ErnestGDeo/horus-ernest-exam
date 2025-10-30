<template>
  <div class="overflow-x-auto">
    <table class="table w-full">
      <thead>
        <tr class="bg-base-200 text-base font-semibold text-gray-700">
          <th>ID</th>
          <th>Username</th>
          <th>Nama Lengkap</th>
          <th>Email</th>
          <th class="text-center">Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" class="hover:bg-base-200 transition">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.nama }}</td>
          <td>{{ user.email }}</td>
          <td class="text-center space-x-2">
            <button @click="$emit('openUpdate', user.id)" class="btn btn-warning btn-sm text-white">
              Ubah
            </button>
            <button @click="$emit('deleteUser', user.id)" class="btn btn-error btn-sm text-white">
              Hapus
            </button>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="5" class="text-center text-gray-500 py-6">
            Tidak ada data pengguna ditemukan 😔
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'UserTable',
  props: ['users'],
}
</script>
