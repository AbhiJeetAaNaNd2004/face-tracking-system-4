<template>
  <div>
    <h2>Employee Manager</h2>
    <button @click="fetchEmployees">🔄 Refresh</button>
    <p v-if="error" style="color:red">{{ error }}</p>
    <ul>
      <li v-for="emp in employees" :key="emp.employee_id">
        {{ emp.name }} ({{ emp.designation || 'N/A' }}) - {{ emp.email || 'No Email' }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const employees = ref([])
const error = ref('')

async function fetchEmployees() {
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = "No token found. Please login."
    return
  }

  try {
    const res = await fetch('http://localhost:8000/employees/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (!res.ok) throw new Error("Failed to fetch employees.")
    employees.value = await res.json()
  } catch (e) {
    error.value = e.message
  }
}
</script>
