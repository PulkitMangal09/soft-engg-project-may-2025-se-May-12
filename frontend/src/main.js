import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// import components from './components'
import './style.css'

const app = createApp(App)

app.use(store)
app.use(router)
// app.use(components) // Register global components

app.mount('#app')