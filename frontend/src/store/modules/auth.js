// src/store/modules/auth.js

import { supabase } from '@/supabaseClient'

export default {
  namespaced: true,

  state: () => ({
    user:            null,                    // { id, email, role }
    token:           localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
    role:            localStorage.getItem('userRole') || null
  }),

  getters: {
    isAuthenticated: s => s.isAuthenticated,
    userRole:        s => s.role,
    currentUser:     s => s.user
  },

  mutations: {
    SET_USER(state, user) {
      state.user            = user
      state.isAuthenticated = true
    },
    SET_TOKEN(state, token) {
      state.token = token
      token
        ? localStorage.setItem('token', token)
        : localStorage.removeItem('token')
    },
    SET_ROLE(state, role) {
      state.role = role
      role
        ? localStorage.setItem('userRole', role)
        : localStorage.removeItem('userRole')
    },
    LOGOUT(state) {
      state.user            = null
      state.token           = null
      state.role            = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
    }
  },

  actions: {
    async login({ commit }, payload) {
      // 1) If caller already passed a real bearer token, use it directly:
      if (payload.token) {
        commit('SET_USER', {
          id:    payload.id,    // you must pass payload.id from LoginView
          email: payload.email,
          role:  payload.role
        })
        commit('SET_TOKEN', payload.token)
        commit('SET_ROLE', payload.role)
        return { success: true }
      }

      // 2) Otherwise do the username/password flow:
      try {
        const form = new URLSearchParams()
        form.append('username',     payload.email)
        form.append('password',     payload.password)
        form.append('grant_type',   'password')
        form.append('client_id',    'web-app')
        form.append('client_secret','dummy-secret')

        const res  = await fetch('http://localhost:8000/auth/token', {
          method:  'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body:    form
        })
        const data = await res.json()

        if (!res.ok) {
          return { success: false, error: data.detail || data.message }
        }

        // build the bearer
        const bearer = `${data.token_type} ${data.access_token}`

        // fetch supabase user profile to get their ID
        const { data: userObj, error } = await supabase.auth.getUser(bearer)
        if (error || !userObj?.user) {
          throw new Error('Could not fetch user profile')
        }

        const user = {
          id:    userObj.user.id,
          email: payload.email,
          role:  payload.role
        }

        // commit real creds
        commit('SET_USER', user)
        commit('SET_TOKEN', bearer)
        commit('SET_ROLE', payload.role)
        return { success: true }

      } catch (err) {
        return { success: false, error: err.message }
      }
    },

    logout({ commit }) {
      commit('LOGOUT')
    }
  }
}
