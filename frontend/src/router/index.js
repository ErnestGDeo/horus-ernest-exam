import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import DashboardPage from '../views/Dashboard.vue'
import UpdateUser from '../views/UpdateUser.vue'
import RegisterPage from '../views/RegisterPage.vue'

const routes = [
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/', name: 'LoginPage', component: LoginPage },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/update-user/:id',
    name: 'UpdateUser',
    component: UpdateUser,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'LoginPage' })
  } else if (to.name === 'LoginPage' && token) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
