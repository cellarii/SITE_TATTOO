import LoginPage from '@/pages/LoginPage.vue'
import MainPage from '@/pages/MainPage.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  linkActiveClass: "active",
  linkActiveClass: "active-exact",
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: MainPage
    },
    {
      path: "/login",
      component: LoginPage
    }
  ],
})

export default router
