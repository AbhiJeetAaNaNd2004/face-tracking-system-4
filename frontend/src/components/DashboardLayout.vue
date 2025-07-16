<template>
  <div>
    <header style="background:#2c3e50; color:white; padding:10px;">
      <h1>Face Tracking Dashboard</h1>
      <nav style="margin:10px 0;">
        <button @click="goTo('employees')">Employees</button>
        <button @click="goTo('attendance')">Attendance</button>
        <button @click="goTo('stream')">Live Stream</button>
        <button @click="logout">Logout</button>
      </nav>
    </header>

    <main style="padding:20px;">
      <router-view />  <!-- Child routes render here -->
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goTo(page) {
  router.push(`/dashboard/${page}`)
}

function logout() {
  localStorage.removeItem('token')
  router.push('/')
}
</script>
