export default {
    namespaced: true,
    state: {
        toasts: [],
        loading: false,
        sidebarOpen: false
    },

    mutations: {
        ADD_TOAST(state, toast) {
            state.toasts.push({
                id: Date.now(),
                ...toast
            })
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
            commit('ADD_TOAST', toast)

            // Auto remove after 5 seconds
            setTimeout(() => {
                commit('REMOVE_TOAST', toast.id)
            }, 5000)
        }
    }
}