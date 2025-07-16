import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/components/Login.vue'
import EmployeeDashboard from '@/components/EmployeeDashboard.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import DashboardLayout from '@/components/DashboardLayout.vue'
import EmployeeManager from '@/components/EmployeeManager.vue'
import AttendanceViewer from '@/components/AttendanceViewer.vue'
import LiveStream from '@/components/LiveStream.vue'

const routes = [
  { 
    path: '/', 
    name: 'Login',
    component: Login 
  },
  {
    path: '/employee-dashboard',
    name: 'EmployeeDashboard',
    component: EmployeeDashboard,
    meta: { requiresAuth: true, role: 'employee' }
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  // Legacy routes for backward compatibility
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: 'employees' },
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

// Enhanced Route Protection
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('role')
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!token) {
      // No token, redirect to login
      return next('/')
    }
    
    // Check role-based access
    if (to.meta.role && to.meta.role !== userRole) {
      // Wrong role, redirect to appropriate dashboard
      if (userRole === 'admin') {
        return next('/admin-dashboard')
      } else {
        return next('/employee-dashboard')
      }
    }
  }
  
  // If user is logged in and tries to access login page, redirect to dashboard
  if (to.path === '/' && token) {
    if (userRole === 'admin') {
      return next('/admin-dashboard')
    } else {
      return next('/employee-dashboard')
    }
  }
  
  next()
})

export default router
