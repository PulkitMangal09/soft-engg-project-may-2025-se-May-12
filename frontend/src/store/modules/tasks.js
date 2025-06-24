export default {
    namespaced: true,
    state: {
        tasks: [],
        loading: false
    },

    mutations: {
        SET_TASKS(state, tasks) {
            state.tasks = tasks
        },
        SET_LOADING(state, loading) {
            state.loading = loading
        }
    },

    actions: {
        async fetchTasks({ commit }) {
            commit('SET_LOADING', true)
            try {
                // API call here
                const tasks = []
                commit('SET_TASKS', tasks)
            } catch (error) {
                console.error('Error fetching tasks:', error)
            } finally {
                commit('SET_LOADING', false)
            }
        }
    }
}