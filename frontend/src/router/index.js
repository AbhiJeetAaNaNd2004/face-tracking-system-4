import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/components/Login.vue'
import DashboardLayout from '@/components/DashboardLayout.vue'
import EmployeeManager from '@/components/EmployeeManager.vue'
import AttendanceViewer from '@/components/AttendanceViewer.vue'
import LiveStream from '@/components/LiveStream.vue'

const routes = [
  { path: '/', component: Login },
  {
    path: '/dashboard',
    component: DashboardLayout,
    children: [
      { path: '', redirect: 'employees' },  // Default child route
      { path: 'employees', component: EmployeeManager },
      { path: 'attendance', component: AttendanceViewer },
      { path: 'stream', component: LiveStream }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Route Protection
router.beforeEach((to, from, next) => {
  const publicPages = ['/']
  const authRequired = !publicPages.includes(to.path)
  const token = localStorage.getItem('token')

  if (authRequired && !token) {
    return next('/')
  }
  next()
})

export default router
