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
            // If password is missing or undefined, bypass backend and set user directly
            if (!password) {
                const mockUser = {
                    id: 1,
                    name: `${role.charAt(0).toUpperCase() + role.slice(1)} User`,
                    email: email || `${role}@example.com`,
                    role: role
                };
                commit('SET_USER', mockUser);
                commit('SET_TOKEN', 'mock-token-' + Date.now());
                commit('SET_ROLE', role);
                return { success: true };
            }
            try {
                // FastAPI expects x-www-form-urlencoded with username, password, grant_type, etc.
                const formData = new URLSearchParams();
                formData.append('username', email);
                formData.append('password', password);
                formData.append('grant_type', 'password');
                formData.append('client_id', 'web-app');
                formData.append('client_secret', 'dummy-secret');

                const response = await fetch('http://localhost:8000/auth/token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    // If backend returns user info, use it; else create minimal user
                    const user = data.user || { email, role };
                    commit('SET_USER', user);
                    // FastAPI returns access_token and token_type
                    const token = data.access_token ? `${data.token_type} ${data.access_token}` : data.token;
                    commit('SET_TOKEN', token);
                    // Use role from response if available, else from input
                    commit('SET_ROLE', user.role || role);
                    return { success: true };
                } else {
                    return { success: false, error: data.detail || data.message };
                }
            } catch (error) {
                return { success: false, error: 'Network error' };
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