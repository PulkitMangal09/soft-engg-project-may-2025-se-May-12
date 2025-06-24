export default {
    namespaced: true,
    state: {
        user: null,
        token: localStorage.getItem('token'),
        isAuthenticated: false,
        role: localStorage.getItem('userRole') || null
    },

    getters: {
        isAuthenticated: state => state.isAuthenticated,
        userRole: state => state.role,
        currentUser: state => state.user
    },

    mutations: {
        SET_USER(state, user) {
            state.user = user
            state.isAuthenticated = !!user
        },

        SET_TOKEN(state, token) {
            state.token = token
            if (token) {
                localStorage.setItem('token', token)
            } else {
                localStorage.removeItem('token')
            }
        },

        SET_ROLE(state, role) {
            state.role = role
            if (role) {
                localStorage.setItem('userRole', role)
            } else {
                localStorage.removeItem('userRole')
            }
        },

        LOGOUT(state) {
            state.user = null
            state.token = null
            state.role = null
            state.isAuthenticated = false
            localStorage.removeItem('token')
            localStorage.removeItem('userRole')
        }
    },

    actions: {
        async login({ commit }, { email, password, role }) {
            try {
                // API call here
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, role })
                })

                const data = await response.json()

                if (response.ok) {
                    commit('SET_USER', data.user)
                    commit('SET_TOKEN', data.token)
                    commit('SET_ROLE', role)
                    return { success: true }
                } else {
                    return { success: false, error: data.message }
                }
            } catch (error) {
                return { success: false, error: 'Network error' }
            }
        },

        logout({ commit }) {
            commit('LOGOUT')
        }
    }
}