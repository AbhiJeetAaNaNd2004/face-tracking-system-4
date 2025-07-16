<template>
  <div>
    <h2>Attendance Records</h2>
    <button @click="fetchAttendance">🔄 Refresh</button>
    <p v-if="error" style="color:red">{{ error }}</p>
    <table border="1">
      <tr>
        <th>Employee ID</th>
        <th>Timestamp</th>
        <th>Camera</th>
        <th>Event</th>
      </tr>
      <tr v-for="record in attendance" :key="record.id">
        <td>{{ record.employee_id }}</td>
        <td>{{ record.timestamp }}</td>
        <td>{{ record.camera_id }}</td>
        <td>{{ record.event_type }}</td>
      </tr>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const attendance = ref([])
const error = ref('')

async function fetchAttendance() {
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = "Please login."
    return
  }

  try {
    const res = await fetch('http://localhost:8000/attendance/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (!res.ok) throw new Error("Failed to fetch attendance.")
    attendance.value = await res.json()
  } catch (e) {
    error.value = e.message
  }
}
</script>
