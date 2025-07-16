<template>
  <div class="employee-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1>Employee Dashboard</h1>
        <p>Welcome back, {{ username }}!</p>
      </div>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <h3>{{ attendanceRecords.length }}</h3>
          <p>Attendance Records</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-info">
          <h3>{{ embeddings.length }}</h3>
          <p>Face Embeddings</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <h3>{{ activeEmployees }}</h3>
          <p>Active Employees</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <h3>{{ workingStatus }}</h3>
          <p>Current Status</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- My Attendance Section -->
      <div class="content-section">
        <div class="section-header">
          <h2>My Attendance Records</h2>
          <button @click="refreshAttendance" class="refresh-btn">
            <span class="icon">🔄</span>
            Refresh
          </button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Camera</th>
                <th>Event</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in attendanceRecords" :key="record.id">
                <td>{{ formatDate(record.timestamp) }}</td>
                <td>{{ formatTime(record.timestamp) }}</td>
                <td>Camera {{ record.camera_id }}</td>
                <td>
                  <span :class="'event-' + record.event_type">
                    {{ record.event_type }}
                  </span>
                </td>
                <td>{{ record.work_status }}</td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="attendanceRecords.length === 0" class="empty-state">
            <p>No attendance records found</p>
          </div>
        </div>
      </div>

      <!-- My Embeddings Section -->
      <div class="content-section">
        <div class="section-header">
          <h2>My Face Embeddings</h2>
          <span class="readonly-badge">Read Only</span>
        </div>
        
        <div class="embeddings-grid">
          <div v-for="embedding in embeddings" :key="embedding.id" class="embedding-card">
            <div class="embedding-info">
              <h3>Embedding #{{ embedding.id }}</h3>
              <p>Created: {{ formatDate(embedding.created_at) }}</p>
              <p>Quality: {{ embedding.quality_score?.toFixed(2) || 'N/A' }}</p>
              <p>Type: {{ embedding.embedding_type }}</p>
            </div>
            <div class="embedding-status">
              <span :class="embedding.is_active ? 'status-active' : 'status-inactive'">
                {{ embedding.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
          </div>
        </div>
        
        <div v-if="embeddings.length === 0" class="empty-state">
          <p>No face embeddings found</p>
        </div>
      </div>

      <!-- All Employees Status Section -->
      <div class="content-section">
        <div class="section-header">
          <h2>All Employees Status</h2>
          <button @click="refreshEmployees" class="refresh-btn">
            <span class="icon">🔄</span>
            Refresh
          </button>
        </div>
        
        <div class="employees-grid">
          <div v-for="employee in employees" :key="employee.employee_id" class="employee-card">
            <div class="employee-avatar">
              {{ employee.name.charAt(0).toUpperCase() }}
            </div>
            <div class="employee-info">
              <h3>{{ employee.name }}</h3>
              <p>{{ employee.designation || 'No designation' }}</p>
              <p>{{ employee.department || 'No department' }}</p>
            </div>
            <div class="employee-status">
              <span :class="employee.is_active ? 'status-active' : 'status-inactive'">
                {{ employee.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
          </div>
        </div>
        
        <div v-if="employees.length === 0" class="empty-state">
          <p>No employees found</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref(localStorage.getItem('username') || 'User')
const attendanceRecords = ref([])
const embeddings = ref([])
const employees = ref([])
const loading = ref(false)

const activeEmployees = computed(() => {
  return employees.value.filter(emp => emp.is_active).length
})

const workingStatus = computed(() => {
  // Get the latest attendance record to determine current status
  if (attendanceRecords.value.length > 0) {
    const latest = attendanceRecords.value[0]
    return latest.work_status || 'Unknown'
  }
  return 'Unknown'
})

async function fetchAttendance() {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:8000/attendance/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      const data = await response.json()
      attendanceRecords.value = data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    }
  } catch (error) {
    console.error('Error fetching attendance:', error)
  }
}

async function fetchEmbeddings() {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:8000/embeddings/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      const data = await response.json()
      embeddings.value = data
    }
  } catch (error) {
    console.error('Error fetching embeddings:', error)
  }
}

async function fetchEmployees() {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:8000/employees/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      const data = await response.json()
      employees.value = data
    }
  } catch (error) {
    console.error('Error fetching employees:', error)
  }
}

function refreshAttendance() {
  fetchAttendance()
}

function refreshEmployees() {
  fetchEmployees()
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleDateString()
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString()
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('username')
  router.push('/')
}

onMounted(() => {
  fetchAttendance()
  fetchEmbeddings()
  fetchEmployees()
})
</script>

<style scoped>
.employee-dashboard {
  min-height: 100vh;
  background: #f8fafc;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.header-content h1 {
  color: #2d3748;
  margin: 0 0 4px 0;
  font-size: 28px;
  font-weight: 700;
}

.header-content p {
  color: #718096;
  margin: 0;
  font-size: 16px;
}

.logout-btn {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #c53030;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 32px;
  background: #f7fafc;
  padding: 16px;
  border-radius: 12px;
}

.stat-info h3 {
  color: #2d3748;
  margin: 0 0 4px 0;
  font-size: 24px;
  font-weight: 700;
}

.stat-info p {
  color: #718096;
  margin: 0;
  font-size: 14px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.content-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.section-header h2 {
  color: #2d3748;
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.refresh-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: #5a67d8;
}

.readonly-badge {
  background: #fed7d7;
  color: #e53e3e;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px 24px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #2d3748;
}

.event-entry {
  background: #c6f6d5;
  color: #22543d;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.event-exit {
  background: #fed7d7;
  color: #742a2a;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.embeddings-grid,
.employees-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  padding: 24px;
}

.embedding-card,
.employee-card {
  background: #f8fafc;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.employee-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.employee-avatar {
  width: 48px;
  height: 48px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
}

.employee-info h3 {
  color: #2d3748;
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
}

.employee-info p {
  color: #718096;
  margin: 0;
  font-size: 14px;
}

.status-active {
  background: #c6f6d5;
  color: #22543d;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-inactive {
  background: #fed7d7;
  color: #742a2a;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: #718096;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
}
</style>