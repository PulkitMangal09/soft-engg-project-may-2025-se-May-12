import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import './style.css'

const app = createApp(App)

// Configure axios
app.use(VueAxios, axios)
axios.defaults.baseURL = 'http://localhost:8000' // Update this if your backend is on a different URL

// Global axios interceptor for authentication
axios.interceptors.request.use(
  (config) => {
    // Get token from localStorage or store
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Global axios interceptor for error handling
axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      store.dispatch('auth/logout')
      router.push('/')
    }
    return Promise.reject(error)
  }
)

// Configure toast
app.config.globalProperties.$toast = toast

app.use(store)
app.use(router)

app.mount('#app')