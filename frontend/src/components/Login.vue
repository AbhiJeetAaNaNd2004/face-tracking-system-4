<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Employee Monitoring System</h1>
        <p>Please sign in to continue</p>
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            id="username"
            v-model="username" 
            type="text"
            placeholder="Enter your username"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password"
            v-model="password" 
            type="password"
            placeholder="Enter your password"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="role">Role</label>
          <select id="role" v-model="role" required>
            <option value="">Select your role</option>
            <option value="employee">Employee</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        
        <button type="submit" class="login-btn" :disabled="loading">
          <span v-if="loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const role = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function login() {
  loading.value = true
  error.value = ''
  
  try {
    const response = await fetch('http://localhost:8000/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        username: username.value, 
        password: password.value 
      })
    })
    
    if (!response.ok) throw new Error('Login failed')

    const data = await response.json()
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('role', role.value)
    localStorage.setItem('username', username.value)
    
    // Route based on role
    if (role.value === 'admin') {
      router.push('/admin-dashboard')
    } else {
      router.push('/employee-dashboard')
    }
    
  } catch (e) {
    error.value = 'Invalid credentials. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #2d3748;
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.login-header p {
  color: #718096;
  font-size: 14px;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #2d3748;
  font-weight: 500;
  font-size: 14px;
}

.form-group input,
.form-group select {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.login-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #e53e3e;
  background: #fed7d7;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
}
</style>
