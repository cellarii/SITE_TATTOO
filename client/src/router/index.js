import AppointmentPage from '@/pages/AppointmentPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import MainPage from '@/pages/MainPage.vue'
import PortfolioPage from '@/pages/PortfolioPage.vue'
import ReviewPage from '@/pages/ReviewPage.vue'
import ServicePage from '@/pages/ServicePage.vue'
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
    },
    {
      path: "/service",
      component: ServicePage
    },
    {
      path: "/appointment",
      component: AppointmentPage
    },
    {
      path: "/review",
      component: ReviewPage
    },
    {
      path: "/portfolio",
      component: PortfolioPage
    }
  ],
})

export default router
