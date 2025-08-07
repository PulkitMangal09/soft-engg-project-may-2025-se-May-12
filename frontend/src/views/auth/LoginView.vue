<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <div
          :class="[
            'w-16 h-16 rounded-2xl flex items-center justify-center text-2xl text-white mx-auto mb-4',
            roleConfig.bgClass
          ]"
        >
          {{ roleConfig.icon }}
        </div>
        <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ roleConfig.title }}</h1>
        <p class="text-gray-600">{{ roleConfig.subtitle }}</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
          <input
            v-model="form.username"
            type="email"
            required
            class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your email"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your password"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          <span v-if="loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          Don't have an account?
          <router-link :to="`/signup/${role}`" class="text-blue-500 hover:underline">Sign Up</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { supabase } from '@/supabaseClient'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export default {
  name: 'LoginView',
  props: {
    role: {
      type: String,
      default: 'student'
    }
  },

  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      loading: false
    }
  },

  computed: {
    roleConfig() {
      const configs = {
        student: {
          title: 'Student Login',
          subtitle: "Welcome back! Let's continue learning",
          icon: '👨‍🎓',
          bgClass: 'bg-gradient-to-br from-blue-500 to-blue-600'
        },
        teacher: {
          title: 'Teacher Login',
          subtitle: 'Welcome back, educator!',
          icon: '👨‍🏫',
          bgClass: 'bg-gradient-to-br from-orange-500 to-orange-600'
        },
        parent: {
          title: 'Parent Login',
          subtitle: "Stay connected with your child's progress",
          icon: '👨‍👩‍👧‍👦',
          bgClass: 'bg-gradient-to-br from-purple-500 to-purple-600'
        }
      }
      return configs[this.role] || configs.student
    }
  },

  methods: {
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        toast.error('Please enter both email and password')
        return
      }

      this.loading = true

      try {
        // 1) Exchange credentials for a JWT
        const formData = new URLSearchParams()
        formData.append('username',    this.form.username)
        formData.append('password',    this.form.password)
        formData.append('grant_type',  'password')
        formData.append('client_id',   'web-app')
        formData.append('client_secret','dummy-secret')

        const { data: tokenResp } = await axios.post(
          'http://localhost:8000/auth/token',
          formData,
          { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        )
        console.log('🔥 auth/token response:', tokenResp)

        const { access_token, token_type, role } = tokenResp
        const bearer = `${token_type} ${access_token}`

        // 2) Call supabase.auth.getUser() with the **raw** token
        const { data: userObj, error: getUserErr } = await supabase.auth.getUser(access_token)
        if (getUserErr || !userObj?.user) {
          throw getUserErr || new Error('Could not fetch user profile')
        }

        // 3) Dispatch real credentials into Vuex
        await this.$store.dispatch('auth/login', {
          token: bearer,
          id:    userObj.user.id,
          email: this.form.username,
          role
        })

        toast.success('Login successful!')
        this.$router.push(`/${role}`)
      } catch (err) {
        console.error('Login error:', err)
        toast.error(err.message || 'Login failed')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
