export default {
    namespaced: true,
    state: {
        toasts: [],
        loading: false,
        sidebarOpen: false
    },

    getters: {
        toasts: state => state.toasts,
        loading: state => state.loading,
        sidebarOpen: state => state.sidebarOpen
    },

    mutations: {
        ADD_TOAST(state, toast) {
            state.toasts.push(toast)
        },

        REMOVE_TOAST(state, id) {
            state.toasts = state.toasts.filter(toast => toast.id !== id)
        },

        SET_LOADING(state, loading) {
            state.loading = loading
        },

        TOGGLE_SIDEBAR(state) {
            state.sidebarOpen = !state.sidebarOpen
        }
    },

    actions: {
        showToast({ commit }, toast) {
            const toastId = Date.now()
            const toastWithId = {
                id: toastId,
                ...toast
            }
            
            commit('ADD_TOAST', toastWithId)

            // Auto remove after 5 seconds
            setTimeout(() => {
                commit('REMOVE_TOAST', toastId)
            }, 5000)
        },

        dismissToast({ commit }, toastId) {
            commit('REMOVE_TOAST', toastId)
        }
    }
}