<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1>Admin Dashboard</h1>
        <p>System Administration Panel</p>
      </div>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <!-- Stats Overview -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <h3>{{ employees.length }}</h3>
          <p>Total Employees</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📹</div>
        <div class="stat-info">
          <h3>{{ cameras.length }}</h3>
          <p>Active Cameras</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <h3>{{ attendanceLogs.length }}</h3>
          <p>Attendance Logs</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔧</div>
        <div class="stat-info">
          <h3>{{ systemLogs.length }}</h3>
          <p>System Logs</p>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tab-navigation">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        {{ tab.name }}
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Camera Feeds Tab -->
      <div v-if="activeTab === 'cameras'" class="content-section">
        <div class="section-header">
          <h2>Live Camera Feeds</h2>
          <button @click="refreshCameras" class="refresh-btn">
            <span class="icon">🔄</span>
            Refresh
          </button>
        </div>
        
        <div class="cameras-grid">
          <div v-for="camera in cameras" :key="camera.id" class="camera-card">
            <div class="camera-header">
              <h3>{{ camera.name }}</h3>
              <span :class="camera.is_active ? 'status-active' : 'status-inactive'">
                {{ camera.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
            <div class="camera-feed">
              <img 
                :src="`http://localhost:8000/stream/${camera.id}`" 
                :alt="`Camera ${camera.id}`"
                class="camera-image"
                @error="handleImageError"
              />
            </div>
            <div class="camera-info">
              <p>Type: {{ camera.camera_type }}</p>
              <p>Resolution: {{ camera.resolution_width }}x{{ camera.resolution_height }}</p>
              <p>FPS: {{ camera.fps }}</p>
            </div>
          </div>
        </div>
        
        <div v-if="cameras.length === 0" class="empty-state">
          <p>No cameras available</p>
        </div>
      </div>

      <!-- Employee Management Tab -->
      <div v-if="activeTab === 'employees'" class="content-section">
        <div class="section-header">
          <h2>Employee Management</h2>
          <button @click="showAddEmployeeModal = true" class="add-btn">
            <span class="icon">➕</span>
            Add Employee
          </button>
        </div>
        
        <div class="employees-table">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Department</th>
                <th>Designation</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="employee in employees" :key="employee.employee_id">
                <td>{{ employee.employee_id }}</td>
                <td>{{ employee.name }}</td>
                <td>{{ employee.department || 'N/A' }}</td>
                <td>{{ employee.designation || 'N/A' }}</td>
                <td>
                  <span :class="employee.is_active ? 'status-active' : 'status-inactive'">
                    {{ employee.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button @click="editEmployee(employee)" class="edit-btn">Edit</button>
                    <button @click="deleteEmployee(employee)" class="delete-btn">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="employees.length === 0" class="empty-state">
            <p>No employees found</p>
          </div>
        </div>
      </div>

      <!-- Attendance Logs Tab -->
      <div v-if="activeTab === 'logs'" class="content-section">
        <div class="section-header">
          <h2>Attendance Logs</h2>
          <button @click="refreshLogs" class="refresh-btn">
            <span class="icon">🔄</span>
            Refresh
          </button>
        </div>
        
        <div class="logs-table">
          <table class="data-table">
            <thead>
              <tr>
                <th>Employee</th>
                <th>Date</th>
                <th>Time</th>
                <th>Camera</th>
                <th>Event</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in attendanceLogs" :key="log.id">
                <td>{{ log.employee_id }}</td>
                <td>{{ formatDate(log.timestamp) }}</td>
                <td>{{ formatTime(log.timestamp) }}</td>
                <td>Camera {{ log.camera_id }}</td>
                <td>
                  <span :class="'event-' + log.event_type">
                    {{ log.event_type }}
                  </span>
                </td>
                <td>{{ log.work_status }}</td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="attendanceLogs.length === 0" class="empty-state">
            <p>No attendance logs found</p>
          </div>
        </div>
      </div>

      <!-- System Logs Tab -->
      <div v-if="activeTab === 'system'" class="content-section">
        <div class="section-header">
          <h2>System Logs</h2>
          <button @click="refreshSystemLogs" class="refresh-btn">
            <span class="icon">🔄</span>
            Refresh
          </button>
        </div>
        
        <div class="system-logs">
          <div v-for="log in systemLogs" :key="log.id" class="log-entry">
            <div class="log-header">
              <span :class="'log-level-' + log.log_level.toLowerCase()">
                {{ log.log_level }}
              </span>
              <span class="log-time">{{ formatDateTime(log.timestamp) }}</span>
            </div>
            <div class="log-message">{{ log.message }}</div>
            <div v-if="log.component" class="log-component">{{ log.component }}</div>
          </div>
          
          <div v-if="systemLogs.length === 0" class="empty-state">
            <p>No system logs found</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Employee Modal -->
    <div v-if="showAddEmployeeModal" class="modal-overlay" @click="showAddEmployeeModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Add New Employee</h3>
          <button @click="showAddEmployeeModal = false" class="modal-close">×</button>
        </div>
        
        <form @submit.prevent="addEmployee" class="employee-form">
          <div class="form-group">
            <label>Employee ID</label>
            <input v-model="newEmployee.employee_id" type="text" required>
          </div>
          
          <div class="form-group">
            <label>Name</label>
            <input v-model="newEmployee.name" type="text" required>
          </div>
          
          <div class="form-group">
            <label>Department</label>
            <input v-model="newEmployee.department" type="text">
          </div>
          
          <div class="form-group">
            <label>Designation</label>
            <input v-model="newEmployee.designation" type="text">
          </div>
          
          <div class="form-group">
            <label>Email</label>
            <input v-model="newEmployee.email" type="email">
          </div>
          
          <div class="form-group">
            <label>Phone</label>
            <input v-model="newEmployee.phone" type="tel">
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showAddEmployeeModal = false" class="cancel-btn">
              Cancel
            </button>
            <button type="submit" class="submit-btn">
              Add Employee
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeTab = ref('cameras')
const employees = ref([])
const cameras = ref([])
const attendanceLogs = ref([])
const systemLogs = ref([])
const showAddEmployeeModal = ref(false)

const newEmployee = ref({
  employee_id: '',
  name: '',
  department: '',
  designation: '',
  email: '',
  phone: ''
})

const tabs = [
  { id: 'cameras', name: 'Camera Feeds', icon: '📹' },
  { id: 'employees', name: 'Employee Management', icon: '👥' },
  { id: 'logs', name: 'Attendance Logs', icon: '📊' },
  { id: 'system', name: 'System Logs', icon: '🔧' }
]

// Mock camera data since we don't have real cameras
const mockCameras = [
  { id: 0, name: 'Main Entrance', is_active: true, camera_type: 'entry', resolution_width: 1920, resolution_height: 1080, fps: 30 },
  { id: 1, name: 'Office Floor', is_active: true, camera_type: 'monitoring', resolution_width: 1920, resolution_height: 1080, fps: 30 },
  { id: 2, name: 'Exit Door', is_active: false, camera_type: 'exit', resolution_width: 1280, resolution_height: 720, fps: 24 }
]

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

async function fetchAttendanceLogs() {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:8000/attendance/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      const data = await response.json()
      attendanceLogs.value = data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    }
  } catch (error) {
    console.error('Error fetching attendance logs:', error)
  }
}

async function fetchSystemLogs() {
  // Mock system logs since we don't have real system logs endpoint
  systemLogs.value = [
    { id: 1, log_level: 'INFO', message: 'System started successfully', component: 'Main', timestamp: new Date().toISOString() },
    { id: 2, log_level: 'WARNING', message: 'Camera 2 connection unstable', component: 'Camera', timestamp: new Date().toISOString() },
    { id: 3, log_level: 'ERROR', message: 'Failed to process face recognition', component: 'FaceRecognition', timestamp: new Date().toISOString() }
  ]
}

async function addEmployee() {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:8000/employees/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newEmployee.value)
    })
    if (response.ok) {
      showAddEmployeeModal.value = false
      resetNewEmployee()
      fetchEmployees()
    }
  } catch (error) {
    console.error('Error adding employee:', error)
  }
}

async function deleteEmployee(employee) {
  if (confirm(`Are you sure you want to delete employee ${employee.name}?`)) {
    const token = localStorage.getItem('token')
    try {
      const response = await fetch(`http://localhost:8000/employees/${employee.employee_id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (response.ok) {
        fetchEmployees()
      }
    } catch (error) {
      console.error('Error deleting employee:', error)
    }
  }
}

function editEmployee(employee) {
  // Implementation for editing employee
  console.log('Edit employee:', employee)
}

function refreshCameras() {
  cameras.value = mockCameras
}

function refreshLogs() {
  fetchAttendanceLogs()
}

function refreshSystemLogs() {
  fetchSystemLogs()
}

function handleImageError(event) {
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIwIiBoZWlnaHQ9IjI0MCIgdmlld0JveD0iMCAwIDMyMCAyNDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMjAiIGhlaWdodD0iMjQwIiBmaWxsPSIjRjdGQUZDIi8+CjxyZWN0IHg9IjEzMCIgeT0iMTAwIiB3aWR0aD0iNjAiIGhlaWdodD0iNDAiIGZpbGw9IiNFMkU4RjAiLz4KPHN2ZyB4PSIxNDUiIHk9IjExMCIgd2lkdGg9IjMwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjQTBBREJBIj4KPC9zdmc+Cjx0ZXh0IHg9IjE2MCIgeT0iMTcwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjNzE4MDk2IiBmb250LXNpemU9IjEyIj5DYW1lcmEgT2ZmbGluZTwvdGV4dD4KPC9zdmc+'
}

function resetNewEmployee() {
  newEmployee.value = {
    employee_id: '',
    name: '',
    department: '',
    designation: '',
    email: '',
    phone: ''
  }
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleDateString()
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString()
}

function formatDateTime(timestamp) {
  return new Date(timestamp).toLocaleString()
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('username')
  router.push('/')
}

onMounted(() => {
  fetchEmployees()
  fetchAttendanceLogs()
  fetchSystemLogs()
  refreshCameras()
})
</script>

<style scoped>
.admin-dashboard {
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

.tab-navigation {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  background: white;
  padding: 4px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 500;
}

.tab-btn:hover {
  background: #f7fafc;
}

.tab-btn.active {
  background: #667eea;
  color: white;
}

.tab-icon {
  font-size: 18px;
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

.refresh-btn,
.add-btn {
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

.refresh-btn:hover,
.add-btn:hover {
  background: #5a67d8;
}

.add-btn {
  background: #38a169;
}

.add-btn:hover {
  background: #2f855a;
}

.cameras-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  padding: 24px;
}

.camera-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.camera-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 16px;
  font-weight: 600;
}

.camera-feed {
  height: 180px;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-info {
  padding: 16px;
}

.camera-info p {
  margin: 4px 0;
  color: #718096;
  font-size: 14px;
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

.action-buttons {
  display: flex;
  gap: 8px;
}

.edit-btn {
  background: #3182ce;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.delete-btn {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
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

.system-logs {
  max-height: 500px;
  overflow-y: auto;
  padding: 24px;
}

.log-entry {
  padding: 12px;
  margin-bottom: 8px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #e2e8f0;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.log-level-info {
  background: #bee3f8;
  color: #2b6cb0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.log-level-warning {
  background: #fbd38d;
  color: #c05621;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.log-level-error {
  background: #fed7d7;
  color: #c53030;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.log-time {
  color: #718096;
  font-size: 12px;
}

.log-message {
  color: #2d3748;
  font-size: 14px;
  margin-bottom: 4px;
}

.log-component {
  color: #718096;
  font-size: 12px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 18px;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #718096;
}

.employee-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  color: #2d3748;
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.cancel-btn {
  background: #e2e8f0;
  color: #2d3748;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}

.submit-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
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