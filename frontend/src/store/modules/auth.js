import { profileService } from '@/services/profileService'

export default {
    namespaced: true,
    state: {
        user: null,
        token: localStorage.getItem('token'),
        isAuthenticated: false,
        role: localStorage.getItem('userRole') || null,
        hasProfile: false,
        profileCompleted: false
    },

    getters: {
        isAuthenticated: state => state.isAuthenticated,
        token: state => state.token,
        userRole: state => state.role,
        currentUser: state => state.user,
        hasProfile: state => state.hasProfile,
        profileCompleted: state => state.profileCompleted
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

        SET_PROFILE_STATUS(state, { hasProfile, profileCompleted }) {
            state.hasProfile = hasProfile
            state.profileCompleted = profileCompleted
        },

        LOGOUT(state) {
            state.user = null
            state.token = null
            state.role = null
            state.isAuthenticated = false
            state.hasProfile = false
            state.profileCompleted = false
            localStorage.removeItem('token')
            localStorage.removeItem('userRole')
        }
    },

    actions: {
        async login({ commit }, { email, password, role }) {
            try {
                // Always use real authentication
                const formData = new URLSearchParams();
                formData.append('username', email);
                formData.append('password', password);
                formData.append('grant_type', 'password');

                const response = await fetch('http://localhost:8000/auth/token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    // Create user object from response data
                    const user = {
                        id: data.user_id || Date.now(),
                        name: email.split('@')[0], // Use email prefix as name
                        email: email,
                        role: data.role
                    };
                    
                    commit('SET_USER', user);
                    
                    // Store the actual access token
                    const token = data.access_token;
                    commit('SET_TOKEN', token);
                    commit('SET_ROLE', data.role);
                    
                    // Set profile status from response
                    commit('SET_PROFILE_STATUS', { 
                        hasProfile: data.has_profile || false, 
                        profileCompleted: data.has_profile || false 
                    });
                    
                    return { success: true };
                } else {
                    return { success: false, error: data.detail || data.message || 'Login failed' };
                }
            } catch (error) {
                console.error('Login error:', error);
                return { success: false, error: 'Network error. Please check your connection.' };
            }
        },

        async signup({ commit }, { email, password, full_name, role }) {
            try {
                const response = await fetch('http://localhost:8000/auth/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email,
                        password,
                        confirm_password: password,
                        full_name,
                        role,
                        terms_agreed: true
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    return { success: true, message: 'Account created successfully' };
                } else {
                    return { success: false, error: data.detail || data.message || 'Signup failed' };
                }
            } catch (error) {
                console.error('Signup error:', error);
                return { success: false, error: 'Network error. Please check your connection.' };
            }
        },

        async checkProfileStatus({ commit, state }) {
            try {
                const token = state.token
                if (!token) return

                const profileStatus = await profileService.checkProfileStatus(token)
                commit('SET_PROFILE_STATUS', {
                    hasProfile: profileStatus.has_profile,
                    profileCompleted: profileStatus.is_completed
                })
            } catch (error) {
                console.error('Error checking profile status:', error)
                commit('SET_PROFILE_STATUS', { hasProfile: false, profileCompleted: false })
            }
        },

        async createProfile({ commit, state }, profileData) {
            try {
                const token = state.token
                const role = state.role
                
                let response
                if (role === 'student') {
                    response = await profileService.createStudentProfile(profileData, token)
                } else if (role === 'teacher') {
                    response = await profileService.createTeacherProfile(profileData, token)
                } else if (role === 'parent') {
                    response = await profileService.createParentProfile(profileData, token)
                }

                commit('SET_PROFILE_STATUS', { hasProfile: true, profileCompleted: true })
                return { success: true, data: response }
            } catch (error) {
                return { success: false, error: error.message }
            }
        },

        async validateToken({ commit, state }) {
            try {
                const token = state.token
                if (!token) {
                    commit('LOGOUT')
                    return false
                }

                // Try to check profile status as a way to validate the token
                await this.dispatch('auth/checkProfileStatus')
                return true
            } catch (error) {
                console.error('Token validation failed:', error)
                commit('LOGOUT')
                return false
            }
        },

        logout({ commit }) {
            commit('LOGOUT')
        }
    }
}
