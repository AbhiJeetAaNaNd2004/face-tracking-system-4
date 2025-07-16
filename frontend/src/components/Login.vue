<template>
  <div class="login-page">
    <h2>Company Login</h2>
    <input v-model="username" placeholder="Username">
    <input type="password" v-model="password" placeholder="Password">
    <button @click="login">Login</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function login() {
  try {
    const response = await fetch('http://localhost:8000/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    if (!response.ok) throw new Error('Login failed')

    const data = await response.json()
    localStorage.setItem('token', data.access_token)
    router.push('/dashboard')
  } catch (e) {
    error.value = 'Invalid username or password.'
  }
}
</script>

<style scoped>
.login-page {
  max-width: 300px;
  margin: 100px auto;
  display: flex;
  flex-direction: column;
}
input {
  margin: 5px 0;
  padding: 8px;
}
button {
  padding: 10px;
}
</style>
