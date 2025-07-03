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

        // New action to bypass authentication for development
        async loginWithoutValidation({ commit }, { role }) {
            // Create a mock user object
            const mockUser = {
                id: 1,
                name: `${role.charAt(0).toUpperCase() + role.slice(1)} User`,
                email: `${role}@example.com`,
                role: role
            }
            
            // Set authentication state without backend validation
            commit('SET_USER', mockUser)
            commit('SET_TOKEN', 'mock-token-' + Date.now())
            commit('SET_ROLE', role)
            
            return { success: true }
        },

        logout({ commit }) {
            commit('LOGOUT')
        }
    }
}