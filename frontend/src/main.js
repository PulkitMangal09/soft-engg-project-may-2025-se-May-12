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

// Configure toast
app.config.globalProperties.$toast = toast

app.use(store)
app.use(router)

app.mount('#app')